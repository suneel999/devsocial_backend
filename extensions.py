from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# NODEJS: Like creating a separate db connection file
db = SQLAlchemy()
bcrypt = Bcrypt()
