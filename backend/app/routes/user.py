from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint('user', __name__)

@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = db.session.get(User, user_id) or db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Users can only update their own profile unless they're an admin
    current_user = db.session.get(User, int(current_user_id))
    if int(current_user_id) != int(user_id) and not (current_user and current_user.is_admin):
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = db.session.get(User, user_id) or db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    
    # Update user fields if they exist in the request
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        user.email = data['email']
    current_user = db.session.get(User, int(current_user_id))
    if 'is_active' in data and current_user and current_user.is_admin:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, int(current_user_id))
    
    # Only allow admins or the user themselves to delete an account
    if int(current_user_id) != int(user_id) and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = db.session.get(User, user_id) or db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # For safety, we'll deactivate the account instead of deleting it
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'User deactivated successfully'}), 200

@user_bp.route('/<int:user_id>/promote', methods=['POST'])
@jwt_required()
def promote_to_admin(user_id):
    # Get current user making the request
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, int(current_user_id))
    
    # Only allow existing admins to promote users
    if not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Find the user to promote
    user_to_promote = db.session.get(User, user_id) or db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if not user_to_promote:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user is already an admin
    if user_to_promote.is_admin:
        return jsonify({'message': 'User is already an admin'}), 400
    
    try:
        # Promote the user
        user_to_promote.is_admin = True
        db.session.commit()
        
        return jsonify({
            'message': 'User promoted to admin successfully',
            'user': user_to_promote.to_dict()
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to promote user', 'error': str(e)}), 500
