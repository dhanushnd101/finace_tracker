import json
from datetime import datetime, timedelta, timezone
from app.utils.datetime_utils import format_iso8601

def test_create_transaction(test_client, auth_headers):
    """Test creating a new transaction"""
    transaction_data = {
        'amount': 150.75,
        'description': 'Grocery shopping',
        'category': 'Food',
        'transaction_type': 'expense',
        'transaction_date': '2025-06-22T12:00:00Z'
    }
    
    response = test_client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['amount'] == 150.75
    assert data['transaction_type'] == 'expense'

def test_get_transactions(test_client, auth_headers):
    """Test getting all transactions"""
    response = test_client.get('/api/transactions', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'amount' in data[0]
    assert 'transaction_type' in data[0]

def test_get_single_transaction(test_client, auth_headers):
    """Test getting a single transaction"""
    # First get all transactions to get an ID
    response = test_client.get('/api/transactions', headers=auth_headers)
    transactions = json.loads(response.data)
    transaction_id = transactions[0]['id']
    
    response = test_client.get(f'/api/transactions/{transaction_id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == transaction_id

def test_update_transaction(test_client, auth_headers):
    """Test updating a transaction"""
    # First get a transaction to update
    response = test_client.get('/api/transactions', headers=auth_headers)
    transaction = json.loads(response.data)[0]
    
    update_data = {
        'amount': 200.00,
        'description': 'Updated description',
        'category': 'Updated Category'
    }
    
    response = test_client.put(
        f'/api/transactions/{transaction["id"]}',
        data=json.dumps(update_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['amount'] == 200.00
    assert data['description'] == 'Updated description'
    assert data['category'] == 'Updated Category'

def test_delete_transaction(test_client, auth_headers):
    """Test deleting a transaction"""
    # First create a transaction to delete
    transaction_data = {
        'amount': 50.00,
        'description': 'Test transaction to delete',
        'category': 'Test',
        'transaction_type': 'expense'
    }
    
    response = test_client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json',
        headers=auth_headers
    )
    transaction = json.loads(response.data)
    
    # Now delete it
    response = test_client.delete(
        f'/api/transactions/{transaction["id"]}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # Verify it's gone
    response = test_client.get(
        f'/api/transactions/{transaction["id"]}',
        headers=auth_headers
    )
    assert response.status_code == 404

def test_transaction_authorization(test_client, auth_headers, admin_headers):
    """Test that users can only access their own transactions"""
    # Create a transaction with regular user
    transaction_data = {
        'amount': 100.00,
        'description': 'Private transaction',
        'category': 'Private',
        'transaction_type': 'expense'
    }
    
    response = test_client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json',
        headers=auth_headers
    )
    transaction = json.loads(response.data)
    
    # Try to access it with admin (should fail)
    response = test_client.get(
        f'/api/transactions/{transaction["id"]}',
        headers=admin_headers
    )
    assert response.status_code == 403
