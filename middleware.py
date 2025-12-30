from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from models import User

# NODEJS: const userAuth = async (req, res, next) => { ... }
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # NODEJS: const { token } = req.cookies;
        token = request.cookies.get('token')
        
        # Fallback to header if needed (optional, keeping for flexibility)
        if not token and 'Authorization' in request.headers:
             auth_header = request.headers['Authorization']
             try:
                token = auth_header.split(" ")[1]
             except IndexError:
                pass
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # NODEJS: const decodedObj = await jwt.verify(token, process.env.SECRET_KEY);
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            # NODEJS: const user = await User.findById(_id);
            current_user = User.query.get(data['user_id'])
            if not current_user:
                 return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        # NODEJS: req.user = user; next();
        # In Flask, we pass the user to the route function or use 'g' global
        return f(current_user, *args, **kwargs)
        
    return decorated
