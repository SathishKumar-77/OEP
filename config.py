import secrets
import os

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/oep'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Default Password
default_password = '1234'

# Flask Configurations
DEBUG = True

# Generate a secure secret key
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Session Configuration
SESSION_TYPE = 'filesystem'  # You can also use 'redis' or other session types
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour, adjust as needed