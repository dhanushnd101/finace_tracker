from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.transaction import Transaction
from app.utils.datetime_utils import now_utc, parse_iso8601, format_iso8601
from sqlalchemy import select

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions():
    # Get current user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    category = request.args.get('category')
    transaction_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    stmt = select(Transaction).where(Transaction.user_id == user_id)
    
    if category:
        stmt = stmt.where(Transaction.category == category)
    if transaction_type:
        stmt = stmt.where(Transaction.transaction_type == transaction_type)
    if start_date:
        stmt = stmt.where(Transaction.transaction_date >= parse_iso8601(start_date))
    if end_date:
        stmt = stmt.where(Transaction.transaction_date <= parse_iso8601(end_date))
    
    # Execute query
    transactions = db.session.scalars(stmt.order_by(Transaction.transaction_date.desc())).all()
    
    return jsonify([t.to_dict() for t in transactions]), 200

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = db.session.execute(db.select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()
    
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    
    # Ensure the transaction belongs to the current user
    if int(transaction.user_id) != int(user_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    return jsonify(transaction.to_dict()), 200

@transaction_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['amount', 'transaction_type']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Validate transaction type
    if data['transaction_type'] not in ['income', 'expense', 'saving']:
        return jsonify({'message': "Transaction type must be 'income' or 'expense' or 'saving'"}), 400
    
    # Parse transaction date if provided
    transaction_date = parse_iso8601(data.get('transaction_date'))
    
    # Create new transaction
    transaction = Transaction(
        user_id=user_id,
        amount=data['amount'],
        description=data.get('description'),
        category=data.get('category'),
        transaction_type=data['transaction_type'],
        transaction_date=transaction_date
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 201

@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get the transaction
    transaction = db.session.execute(db.select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    
    # Ensure the transaction belongs to the current user
    if int(transaction.user_id) != int(user_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Update fields
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'description' in data:
        transaction.description = data['description']
    if 'category' in data:
        transaction.category = data['category']
    if 'transaction_type' in data:
        if data['transaction_type'] not in ['income', 'expense', 'saving']:
            return jsonify({'message': "Transaction type must be 'income' or 'expense' or 'saving'"}), 400
        transaction.transaction_type = data['transaction_type']
    if 'transaction_date' in data:
        transaction.transaction_date = parse_iso8601(data['transaction_date'])
    
    transaction.updated_at = now_utc()
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 200

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    
    # Get the transaction
    transaction = db.session.execute(db.select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    
    # Ensure the transaction belongs to the current user
    if int(transaction.user_id) != int(user_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Delete the transaction
    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify({'message': 'Transaction deleted successfully'}), 200
