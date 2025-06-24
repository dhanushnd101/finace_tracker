import json

def test_register_user(test_client):
    """Test user registration"""
    user_data = {
        'username': 'dhanush',
        'email': 'dhanush@gmail.com',
        'password': 'dhanush123',
        'first_name': 'Dhanush',
        'last_name': 'Dinesh'
    }
    
    response = test_client.post('/api/auth/register', 
                              data=json.dumps(user_data),
                              content_type='application/json')
    
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'dhanush'
    assert data['user']['email'] == 'dhanush@gmail.com'

def test_login_user(test_client):
    """Test user login"""
    login_data = {
        'username': 'user1',
        'password': 'user1123'
    }
    
    response = test_client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'user1'

def test_login_with_invalid_credentials(test_client):
    """Test login with invalid credentials"""
    login_data = {
        'username': 'user1',
        'password': 'wrongpassword'
    }
    
    response = test_client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'message' in data

def test_get_current_user(test_client, auth_headers):
    """Test getting current user info"""
    response = test_client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'user1'

def test_invalid_login(test_client):
    """Test login with invalid credentials"""
    login_data = {
        'username': 'nonexistent',
        'password': 'wrongpassword'
    }
    
    response = test_client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'message' in data
