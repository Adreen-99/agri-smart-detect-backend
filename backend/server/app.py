import os
os.environ['FLASK_ENV'] = 'development'

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# Import the fixed config
import sys
sys.path.append(os.path.dirname(__file__))
from config_fixed import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # Basic routes for testing
    @app.route('/')
    def home():
        return jsonify({"message": "Agri Smart Detect API", "status": "running"})

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})

    return app
