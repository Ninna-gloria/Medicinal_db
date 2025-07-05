import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Database URI loaded from environment variable only
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_PERMANENT = False
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB


    # Optionally, raise an error if critical variables are missing
    if not SECRET_KEY or not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SECRET_KEY and DATABASE_URL must be set in environment variables or .env file.")
    # Optional: Configure logging
    import logging
    logging.basicConfig(level=LOGGING_LEVEL,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])