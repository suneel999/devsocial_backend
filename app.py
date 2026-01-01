from flask import Flask
from config import Config
from extensions import db, bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://13.60.170.40"])

db.init_app(app)
bcrypt.init_app(app)

# Import models so they are registered with SQLAlchemy
from models import User, ConnectionRequest
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.requests import request_bp
from routes.user import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(request_bp)
app.register_blueprint(user_bp)

@app.route('/')
def hello():
    return 'Hello, DevTinder Flask!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")

    app.run(debug=True, port=5001)

