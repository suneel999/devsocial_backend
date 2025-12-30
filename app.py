from flask import Flask
from config import Config
from extensions import db, bcrypt
from flask_cors import CORS

# NODEJS: equivalent to const app = express();
app = Flask(__name__)
app.config.from_object(Config)

# NODEJS: app.use(cors({ origin: "http://localhost:5173", credentials: true }));
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# NODEJS: Initialize plugins
db.init_app(app)
bcrypt.init_app(app)

# Import models so they are registered with SQLAlchemy
from models import User, ConnectionRequest
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.requests import request_bp
from routes.user import user_bp

# NODEJS: app.use("/", authRouter);
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(request_bp)
app.register_blueprint(user_bp)

@app.route('/')
def hello():
    # NODEJS: res.send('Hello World')
    return 'Hello, DevTinder Flask!'

if __name__ == '__main__':
    with app.app_context():
        # NODEJS: sequelize.sync()
        db.create_all()
        print("Database initialized!")

    # NODEJS: app.listen(5000)
    app.run(debug=True, port=5001)

