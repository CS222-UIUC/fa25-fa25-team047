"""Tests for authentication endpoints."""
import pytest
from models import User, db

class TestRegistration:
    """Tests for user registration."""

    def test_successful_registration(self, client):
        """Test successful user registration."""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'securepassword123'
        })

        assert response.status_code == 201
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'newuser@example.com'
        assert data['message'] == 'User registered successfully'

    def test_registration_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email."""
        response = client.post('/auth/register', json={
            'email': 'test@example.com',
            'password': 'anotherpassword123'
        })

        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()

    def test_registration_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post('/auth/register', json={
            'email': 'invalidemail',
            'password': 'password123'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_registration_short_password(self, client):
        """Test registration with password that's too short."""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'short'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert '8 characters' in data['error']

    def test_registration_missing_email(self, client):
        """Test registration with missing email."""
        response = client.post('/auth/register', json={
            'password': 'password123'
        })

        assert response.status_code == 400

    def test_registration_missing_password(self, client):
        """Test registration with missing password."""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com'
        })

        assert response.status_code == 400


class TestLogin:
    """Tests for user login."""

    def test_successful_login(self, client, sample_user):
        """Test successful login."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
        assert data['message'] == 'Login successful'

    def test_login_wrong_password(self, client, sample_user):
        """Test login with incorrect password."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'invalid' in data['error'].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post('/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_case_insensitive_email(self, client, sample_user):
        """Test that email is case-insensitive."""
        response = client.post('/auth/login', json={
            'email': 'TEST@EXAMPLE.COM',
            'password': 'testpassword123'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['email'] == 'test@example.com'

    def test_login_missing_email(self, client):
        """Test login with missing email."""
        response = client.post('/auth/login', json={
            'password': 'password123'
        })

        assert response.status_code == 400

    def test_login_missing_password(self, client):
        """Test login with missing password."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com'
        })

        assert response.status_code == 400


class TestGetCurrentUser:
    """Tests for getting current user information."""

    def test_get_current_user_success(self, client, sample_user, auth_token):
        """Test getting current user with valid token."""
        response = client.get(
            '/auth/me',
            headers={'Authorization': f'Bearer {auth_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get('/auth/me')

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            '/auth/me',
            headers={'Authorization': 'Bearer invalidtoken123'}
        )

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


class TestPasswordHashing:
    """Tests for password security."""

    def test_password_is_hashed(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(email='hashtest@example.com')
            user.set_password('mypassword123')
            db.session.add(user)
            db.session.commit()

            # Password should be hashed, not stored as plain text
            assert user.password_hash != 'mypassword123'
            assert len(user.password_hash) > 20  # Bcrypt hashes are long

    def test_password_verification(self, app):
        """Test password verification."""
        with app.app_context():
            user = User(email='verifytest@example.com')
            user.set_password('correctpassword')
            db.session.add(user)
            db.session.commit()

            assert user.check_password('correctpassword') is True
            assert user.check_password('wrongpassword') is False
