from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User
from middleware import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validation logic here (like validateSignUpData)
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing arguments'}), 400
        
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400
        
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        firstName=data.get('firstName'),
        lastName=data.get('lastName'),
        email=data['email'],
        password=hashed_password,
        age=data.get('age'),
        gender=data.get('gender')
    )
    
    db.session.add(new_user)
    db.session.commit()
    token = new_user.get_jwt_token()
    response = jsonify({'message': 'User created successfully!', 'data': new_user.to_dict()})
    response.set_cookie('token', token, httponly=True, samesite='Lax')
    return response , 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Could not verify'}), 401
        
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = user.get_jwt_token()
        
        response = jsonify({'message': 'Login successful!', 'data': user.to_dict()})
        # set_cookie(key, value, httponly=True, secure=True (in prod), samesite='Lax')
        response.set_cookie('token', token, httponly=True, samesite='Lax')
        return response
        
    return jsonify({'message': 'Invalid credentials!'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logout successful!'})
    response.set_cookie('token', '', expires=0)
    return response

