from extensions import db
import jwt
import datetime
from config import Config

class User(db.Model):
    # NODEJS: In Mongoose: const userSchema = new mongoose.Schema({...})
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    about = db.Column(db.String(200), default="I like coding")
    photo_url = db.Column(db.String(500), default="https://geographyandyou.com/images/user-profile.png")
    
    # NODEJS: Mongoose 'methods' (userSchema.methods.getJWT)
    def get_jwt_token(self):
        # Generates a JWT token
        payload = {
            'user_id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    # NODEJS: Mongoose 'methods' (userSchema.methods.validatePassword)
    # We will use bcrypt here directly usually, but can add helper method
    def to_dict(self):
        # Helper to serialize (like .toJSON())
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'about': self.about,
            'photoUrl': self.photo_url
            # Add other fields as needed
        }

class ConnectionRequest(db.Model):
    __tablename__ = 'connection_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False) # ignored, interested, accepted, rejected
    
    # Relationships
    from_user = db.relationship("User", foreign_keys=[from_user_id], backref="sent_requests")
    to_user = db.relationship("User", foreign_keys=[to_user_id], backref="received_requests")

    def to_dict(self):
         return {
            'id': self.id,
            'fromUserId': self.from_user_id, # matching Node response structure often returns keys or populated objects
            'toUserId': self.to_user_id,
            'status': self.status
         }

