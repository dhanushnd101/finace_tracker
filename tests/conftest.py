import pytest
import os
import pytest
from app import create_app, db
from app.models.user import User
from app.seed import create_test_data

@pytest.fixture(scope='module')
def test_client():
    # Create test app with test config
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'JWT_SECRET_KEY': 'test-jwt-secret-key'
    })
    
    # Create test client
    with app.test_client() as testing_client:
        with app.app_context():
            # Create database tables
            db.create_all()
            # Create test users
            create_test_data()
            yield testing_client
            # Clean up
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers(test_client):
    # Log in a test user and return the auth token
    login_data = {
        'username': 'user1',
        'password': 'user1123'
    }
    response = test_client.post('/api/auth/login', json=login_data)
    token = response.get_json().get('access_token')
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(test_client):
    # Log in as admin and return the auth token
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    response = test_client.post('/api/auth/login', json=login_data)
    token = response.get_json().get('access_token')
    return {'Authorization': f'Bearer {token}'}
