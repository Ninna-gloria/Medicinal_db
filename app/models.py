from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# User model for authentication and authorization
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # <-- Add this line
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # Hash and set the user's password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.password_hash, password)


# Plant model for storing plant information
class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    common_name = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(255))  # ← Add this line
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Use model for storing plant uses
class Use(db.Model):
    __tablename__ = 'uses'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    use_description = db.Column(db.Text, nullable=False)


# AuthLog model for logging authentication events
class AuthLog(db.Model):
    __tablename__ = 'auth_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))


user = User(username="...", email="...")
user.set_password("your_password_here")
# then add and commit user to the database