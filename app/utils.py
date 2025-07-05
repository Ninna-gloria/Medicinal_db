def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

def check_password(hashed_password, password):
    from werkzeug.security import check_password_hash
    return check_password_hash(hashed_password, password)

def log_action(user_id, action):
    from datetime import datetime
    from app.models import AuthLog
    from app import db

    log_entry = AuthLog(user_id=user_id, action=action, timestamp=datetime.utcnow())
    db.session.add(log_entry)
    db.session.commit()

def sanitize_input(input_string):
    from werkzeug.utils import escape
    return escape(input_string)

def generate_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return generate_csrf()