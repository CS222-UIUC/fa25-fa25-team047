"""Pytest configuration and fixtures."""
import pytest
from app import create_app
from models import db, User, Problem

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(email='test@example.com')
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def sample_problem(app):
    """Create a sample problem for testing."""
    with app.app_context():
        problem = Problem(
            title='Test Problem',
            description='This is a test problem.',
            difficulty='easy',
            topic='arrays',
            function_signature='def test_function(arr):',
            starter_code='def test_function(arr):\n    pass',
            sample_test_cases=[
                {'input': {'arr': [1, 2, 3]}, 'expected': [1, 2, 3]}
            ],
            hidden_test_cases=[
                {'input': {'arr': [4, 5, 6]}, 'expected': [4, 5, 6]}
            ],
            is_published=True
        )
        db.session.add(problem)
        db.session.commit()
        return problem

@pytest.fixture
def auth_token(client, sample_user):
    """Get an authentication token for testing."""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    data = response.get_json()
    return data['token']
