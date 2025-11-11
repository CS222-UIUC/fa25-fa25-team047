"""Tests for problem endpoints."""
import pytest
from models import Problem, db

class TestGetProblems:
    """Tests for getting all problems."""

    def test_get_problems_authenticated(self, client, sample_user, sample_problem, auth_token):
        """Test getting problems with valid authentication."""
        response = client.get(
            '/problems',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'problems' in data
        assert 'count' in data
        assert len(data['problems']) == 1
        assert data['problems'][0]['title'] == 'Test Problem'

    def test_get_problems_unauthenticated(self, client, sample_problem):
        """Test getting problems without authentication."""
        response = client.get('/problems')

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_problems_filter_by_difficulty(self, app, client, auth_token):
        """Test filtering problems by difficulty."""
        with app.app_context():
            # Create multiple problems with different difficulties
            easy_problem = Problem(
                title='Easy Problem',
                description='Easy test',
                difficulty='easy',
                topic='arrays',
                function_signature='def easy():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=True
            )
            hard_problem = Problem(
                title='Hard Problem',
                description='Hard test',
                difficulty='hard',
                topic='graphs',
                function_signature='def hard():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=True
            )
            db.session.add(easy_problem)
            db.session.add(hard_problem)
            db.session.commit()

        response = client.get(
            '/problems?difficulty=easy',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 1
        assert data['problems'][0]['difficulty'] == 'easy'

    def test_get_problems_filter_by_topic(self, app, client, auth_token):
        """Test filtering problems by topic."""
        with app.app_context():
            # Create problems with different topics
            array_problem = Problem(
                title='Array Problem',
                description='Array test',
                difficulty='easy',
                topic='arrays',
                function_signature='def arr():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=True
            )
            tree_problem = Problem(
                title='Tree Problem',
                description='Tree test',
                difficulty='easy',
                topic='trees',
                function_signature='def tree():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=True
            )
            db.session.add(array_problem)
            db.session.add(tree_problem)
            db.session.commit()

        response = client.get(
            '/problems?topic=trees',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 1
        assert data['problems'][0]['topic'] == 'trees'

    def test_get_problems_only_published(self, app, client, auth_token):
        """Test that only published problems are returned."""
        with app.app_context():
            published = Problem(
                title='Published Problem',
                description='Published',
                difficulty='easy',
                topic='arrays',
                function_signature='def pub():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=True
            )
            unpublished = Problem(
                title='Unpublished Problem',
                description='Unpublished',
                difficulty='easy',
                topic='arrays',
                function_signature='def unpub():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=False
            )
            db.session.add(published)
            db.session.add(unpublished)
            db.session.commit()

        response = client.get(
            '/problems',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        # Should only return published problem
        titles = [p['title'] for p in data['problems']]
        assert 'Published Problem' in titles
        assert 'Unpublished Problem' not in titles


class TestGetProblemById:
    """Tests for getting a specific problem."""

    def test_get_problem_by_id_success(self, client, sample_problem, auth_token):
        """Test getting a problem by ID."""
        response = client.get(
            f'/problems/{sample_problem.id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'problem' in data
        assert data['problem']['title'] == 'Test Problem'
        assert data['problem']['description'] == 'This is a test problem.'
        # Should not include hidden test cases
        assert 'hidden_test_cases' not in data['problem']

    def test_get_problem_by_id_not_found(self, client, auth_token):
        """Test getting a non-existent problem."""
        response = client.get(
            '/problems/99999',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_get_problem_by_id_unpublished(self, app, client, auth_token):
        """Test that unpublished problems return 404."""
        with app.app_context():
            unpublished = Problem(
                title='Unpublished',
                description='Test',
                difficulty='easy',
                topic='arrays',
                function_signature='def test():',
                starter_code='pass',
                sample_test_cases=[{'input': {}, 'expected': True}],
                hidden_test_cases=[{'input': {}, 'expected': True}],
                is_published=False
            )
            db.session.add(unpublished)
            db.session.commit()
            problem_id = unpublished.id

        response = client.get(
            f'/problems/{problem_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 404

    def test_get_problem_by_id_unauthenticated(self, client, sample_problem):
        """Test getting a problem without authentication."""
        response = client.get(f'/problems/{sample_problem.id}')

        assert response.status_code == 401


class TestProblemModel:
    """Tests for the Problem model."""

    def test_problem_to_dict_excludes_hidden(self, app, sample_problem):
        """Test that to_dict excludes hidden test cases by default."""
        with app.app_context():
            problem = Problem.query.first()
            data = problem.to_dict()

            assert 'sample_test_cases' in data
            assert 'hidden_test_cases' not in data
            assert 'solution' not in data

    def test_problem_to_dict_includes_hidden(self, app, sample_problem):
        """Test that to_dict can include hidden test cases."""
        with app.app_context():
            problem = Problem.query.first()
            data = problem.to_dict(include_hidden=True)

            assert 'sample_test_cases' in data
            assert 'hidden_test_cases' in data
            assert 'solution' in data
