from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from middleware import token_required

# NODEJS: const profileRouter = express.Router();
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/view', methods=['GET'])
@token_required
def view_profile(current_user):
    # NODEJS: res.send(data)
    return jsonify(current_user.to_dict())

@profile_bp.route('/profile/edit', methods=['PATCH'])
@token_required
def edit_profile(current_user):
    # NODEJS: const loggedInUser = req.data;
    data = request.get_json()
    
    # Validation logic here (like validateEditProfileData)
    # Validation logic here (like validateEditProfileData)
    allowed_fields = ['firstName', 'lastName', 'age', 'gender', 'skills', 'about', 'photoUrl'] # Add fields as needed
    
    try:
        updated = False
        for key in data:
            if key in allowed_fields:
               # NODEJS: loggedInUser[key] = req.body[key];
               if key == 'photoUrl':
                   current_user.photo_url = data[key]
               else:
                   setattr(current_user, key, data[key])
               updated = True
        
        if updated:
            # NODEJS: await loggedInUser.save();
            db.session.commit()
            
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@profile_bp.route('/profile/password', methods=['PATCH'])
@token_required
def update_password(current_user):
    # NODEJS: const isverified = await bcrypt.compare(req.body.oldPassword,req.data.password)
    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('password') # or newPassword depending on frontend
    
    try:
        if not old_password or not new_password:
             raise Exception("Please provide old and new password")

        if not bcrypt.check_password_hash(current_user.password, old_password):
            raise Exception("Invalid old password")
            
        # NODEJS: const newHashedPassword = await bcrypt.hash(req.body.password, 10);
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password = hashed_password
        
        # NODEJS: await loggedInUser.save();
        db.session.commit()
        
        return jsonify({'message': 'Password updated successfully'})

    except Exception as e:
        return jsonify({'message': str(e)}), 400
