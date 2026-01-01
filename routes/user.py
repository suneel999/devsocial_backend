from flask import Blueprint, request, jsonify
from extensions import db
from models import User, ConnectionRequest
from middleware import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/connections/received', methods=['GET'])
@token_required
@token_required
def get_received_requests(current_user):
    try:
        requests = ConnectionRequest.query.filter_by(
            to_user_id=current_user.id,
            status="interested"
        ).all()
        
        # Populate logic: We want sender details
        data = []
        for req in requests:
            # SQLAlchemy relationships handle 'populate'
            sender = req.from_user
            if sender:
                user_dict = sender.to_dict()
                # Include request ID if needed or restructure response
                user_dict['requestId'] = req.id 
                data.append(user_dict)
                
        return jsonify({'message': 'Data fetched successfully', 'data': data})
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_bp.route('/user/connections', methods=['GET'])
@token_required
@token_required
def get_connections(current_user):
    try:
        connections = ConnectionRequest.query.filter(
            (ConnectionRequest.status == 'accepted') &
            ((ConnectionRequest.from_user_id == current_user.id) | (ConnectionRequest.to_user_id == current_user.id))
        ).all()
        
        data = []
        for conn in connections:
            if conn.from_user_id == current_user.id:
                data.append(conn.to_user.to_dict())
            else:
                data.append(conn.from_user.to_dict())
                
        return jsonify({'message': 'Connections fetched', 'data': data})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_bp.route('/feed', methods=['GET'])
@token_required
def get_feed(current_user):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        
        # 1. Find all connection requests (any status) related to user
        my_connections = ConnectionRequest.query.filter(
            (ConnectionRequest.from_user_id == current_user.id) |
            (ConnectionRequest.to_user_id == current_user.id)
        ).all()
        
        hide_users = set()
        for conn in my_connections:
            hide_users.add(conn.from_user_id)
            hide_users.add(conn.to_user_id)
            
        hide_users.add(current_user.id) # Hide self
        
        # 2. Find users NOT in hide_users
        users = User.query.filter(User.id.notin_(hide_users)).offset(skip).limit(limit).all()
        
        data = [user.to_dict() for user in users]
        
        return jsonify({'data': data})
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400
