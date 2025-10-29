import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(basedir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agri-smart-detect-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(project_root, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-agri-smart-detect'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS Configuration - Updated with your frontend URL
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://agri-smart-detect.onrender.com",
        "https://agri-smart-detect-frontend.onrender.com"
    ]
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # SendGrid Configuration
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@agri-smart-detect.com')
    APP_NAME = 'Agri Smart Detect'
    
    # Plant.id API Configuration
    PLANT_ID_API_KEY = os.environ.get('PLANT_ID_API_KEY', '8VY7pHmuqNXEt7WlEclcIazuj24GUivdJbSXxJXviDYGTuixpg')
    PLANT_ID_API_URL = 'https://api.plant.id/v2/identify'
    
    # Frontend URL for email links
    FRONTEND_URL = 'https://agri-smart-detect.onrender.com'