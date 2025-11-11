"""Integration test to verify the complete auth flow."""
import pytest
from models import User, db

class TestIntegrationFlow:
    """Test complete user registration and login flow."""

    def test_complete_auth_flow(self, client, app):
        """Test the complete authentication workflow."""
        # Step 1: Register a new user
        register_response = client.post('/auth/register', json={
            'email': 'integration@example.com',
            'password': 'testpassword123'
        })
        assert register_response.status_code == 201
        register_data = register_response.get_json()
        assert 'token' in register_data
        assert register_data['user']['email'] == 'integration@example.com'

        first_token = register_data['token']

        # Step 2: Verify user exists in database
        with app.app_context():
            user = User.query.filter_by(email='integration@example.com').first()
            assert user is not None
            assert user.password_hash != 'testpassword123'  # Password should be hashed

        # Step 3: Login with the same credentials
        login_response = client.post('/auth/login', json={
            'email': 'integration@example.com',
            'password': 'testpassword123'
        })
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        assert 'token' in login_data

        second_token = login_data['token']

        # Step 4: Use the token to access protected endpoint
        me_response = client.get(
            '/auth/me',
            headers={'Authorization': f'Bearer {second_token}'}
        )
        assert me_response.status_code == 200
        me_data = me_response.get_json()
        assert me_data['user']['email'] == 'integration@example.com'

        # Step 5: Try to access protected endpoint without token
        no_auth_response = client.get('/auth/me')
        assert no_auth_response.status_code == 401

    def test_complete_problem_flow(self, client, sample_user, sample_problem, auth_token):
        """Test the complete problem retrieval workflow."""
        # Step 1: Get all problems
        all_problems_response = client.get(
            '/problems',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert all_problems_response.status_code == 200
        all_problems_data = all_problems_response.get_json()
        assert 'problems' in all_problems_data
        assert len(all_problems_data['problems']) > 0

        # Step 2: Get specific problem
        problem_id = all_problems_data['problems'][0]['id']
        problem_response = client.get(
            f'/problems/{problem_id}',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert problem_response.status_code == 200
        problem_data = problem_response.get_json()
        assert 'problem' in problem_data
        assert 'sample_test_cases' in problem_data['problem']
        # Verify hidden test cases are not exposed
        assert 'hidden_test_cases' not in problem_data['problem']

        # Step 3: Try to access without authentication
        no_auth_response = client.get(f'/problems/{problem_id}')
        assert no_auth_response.status_code == 401

    def test_registration_prevents_duplicates(self, client):
        """Test that duplicate registration is prevented."""
        # Register first user
        first_response = client.post('/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123'
        })
        assert first_response.status_code == 201

        # Try to register with same email
        second_response = client.post('/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'differentpassword'
        })
        assert second_response.status_code == 409
        error_data = second_response.get_json()
        assert 'error' in error_data
        assert 'already exists' in error_data['error'].lower()
