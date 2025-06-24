import json

def test_get_all_users(test_client, admin_headers):
    """Test getting all users (admin only)"""
    response = test_client.get('/api/users', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_single_user(test_client, auth_headers):
    """Test getting a single user by ID"""
    # First, get the current user's ID
    me_response = test_client.get('/api/auth/me', headers=auth_headers)
    user_id = json.loads(me_response.data)['id']
    
    # Then get the user by ID
    response = test_client.get(f'/api/users/{user_id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == user_id
    assert 'username' in data

def test_update_user(test_client, auth_headers):
    """Test updating user information"""
    # Get the current user's ID
    me_response = test_client.get('/api/auth/me', headers=auth_headers)
    user_id = json.loads(me_response.data)['id']
    
    update_data = {
        'first_name': 'Updated',
        'last_name': 'Name',
        'email': 'updated@gmail.com'
    }
    
    response = test_client.put(f'/api/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['first_name'] == 'Updated'
    assert data['user']['last_name'] == 'Name'
    assert data['user']['email'] == 'updated@gmail.com'

def test_promote_to_admin(test_client, admin_headers):
    """Test promoting a user to admin (admin only)"""
    # First, get a non-admin user
    users_response = test_client.get('/api/users', headers=admin_headers)
    users = json.loads(users_response.data)
    non_admin = next((u for u in users if u['username'] == 'user1'), None)
    
    # Promote the user
    response = test_client.post(f"/api/users/{non_admin['id']}/promote",
                              headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user']['is_admin'] is True

def test_delete_user(test_client, admin_headers):
    """Test deactivating a user"""
    # First, create a test user to delete
    user_data = {
        'username': 'todelete',
        'email': 'delete@gmail.com',
        'password': 'delete123',
        'first_name': 'To',
        'last_name': 'Delete'
    }
    
    create_response = test_client.post('/api/auth/register',
                                     data=json.dumps(user_data),
                                     content_type='application/json')
    user_id = json.loads(create_response.data)['user']['id']
    
    # Now delete the user
    response = test_client.delete(f'/api/users/{user_id}',
                                headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    
    # Verify the user is deactivated
    get_response = test_client.get(f'/api/users/{user_id}',
                                 headers=admin_headers)
    user_data = json.loads(get_response.data)
    assert user_data['is_active'] is False
