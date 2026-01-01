from flask import Blueprint, request, jsonify
from extensions import db
from models import User, ConnectionRequest
from middleware import token_required

request_bp = Blueprint('request', __name__)

@request_bp.route('/send/<status>/<to_user_id>', methods=['POST'])
@token_required
def send_connection_request(current_user, status, to_user_id):
    try:
        from_user_id = current_user.id
        
        allowed_status = ["ignored", "interested"]
        if status not in allowed_status:
             print(f"DEBUG: Invalid status type: {status}")
             return jsonify({'message': f"Invalid status type: {status}"}), 400

        # Check if to_user exists
        to_user = User.query.get(to_user_id)
        if not to_user:
            return jsonify({'message': "User not found!"}), 404
            
        # Check existing connection
        existing_request = ConnectionRequest.query.filter(
            ((ConnectionRequest.from_user_id == from_user_id) & (ConnectionRequest.to_user_id == to_user_id)) |
            ((ConnectionRequest.from_user_id == to_user_id) & (ConnectionRequest.to_user_id == from_user_id))
        ).first()

        if existing_request:
             print(f"DEBUG: Connection Request already sent! From: {from_user_id} To: {to_user_id}")
             return jsonify({'message': "Connection Request already sent!"}), 400
             
        new_request = ConnectionRequest(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status=status
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({'message': f"Connection Request {status}!"})

    except Exception as e:
        print(f"DEBUG: Exception in send_connection_request: {e}")
        return jsonify({'message': str(e)}), 400

@request_bp.route('/request/review/<status>/<request_id>', methods=['POST'])
@token_required
def review_connection_request(current_user, status, request_id):
    try:
        logged_in_user_id = current_user.id
        allowed_status = ["accepted", "rejected"]
        if status not in allowed_status:
             return jsonify({'message': f"Invalid status type: {status}"}), 400

        print(f"DEBUG: Reviewing request. LoggedInUser: {logged_in_user_id}, RequestID: {request_id}, Status: {status}")
        
        # Check if request exists at all for debugging
        req_check = ConnectionRequest.query.get(request_id)
        if req_check:
             print(f"DEBUG: Request found in DB. ToUser: {req_check.to_user_id}, Status: {req_check.status}")
        else:
             print(f"DEBUG: Request {request_id} NOT FOUND in DB.")
             
        connection_request = ConnectionRequest.query.filter_by(
            id=request_id,
            to_user_id=logged_in_user_id,
            status="interested"
        ).first()
        
        if not connection_request:
             return jsonify({'message': "Connection Request not found"}), 404
        
        connection_request.status = status
        db.session.commit()
        
        return jsonify({'message': f"Connection Request {status}!"})
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400
