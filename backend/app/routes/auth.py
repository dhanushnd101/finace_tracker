from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Validate email
    try:
        valid = validate_email(data['email'])
        data['email'] = valid.email
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email address'}), 400
    
    # Check if user already exists
    if db.session.execute(db.select(User).filter_by(username=data['username'])).scalar_one_or_none():
        return jsonify({'message': 'Username already exists'}), 400
    
    if db.session.execute(db.select(User).filter_by(email=data['email'])).scalar_one_or_none():
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.password = data['password']  # This will hash the password
    
    db.session.add(user)
    db.session.commit()
    
    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = db.session.execute(db.select(User).filter_by(username=data['username'])).scalar_one_or_none()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Account is deactivated'}), 403
    
    # Convert user.id to string as JWT identity must be a string
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    # Convert the string ID back to integer for the database query
    user = db.session.execute(db.select(User).filter_by(id=int(current_user_id))).scalar_one_or_none()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200
