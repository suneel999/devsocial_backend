import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_jwt_secret_key'
    
    # Format: mysql+pymysql://username:password@host/dbname
    # DEVELOPMENT: Use SQLite for easy testing without DB server
    # PRODUCTION: Use Environment Variable for MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
