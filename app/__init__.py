import os
try:
    from flask import Flask, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_jwt_extended import JWTManager
    from flask_cors import CORS
    from flask_bcrypt import Bcrypt
    from dotenv import load_dotenv
except ImportError as e:
    missing = str(e)
    raise RuntimeError(
        f"Missing dependency: {missing}. Please install the project requirements, for example:\n"
        f"  pip install -r requirements.txt\n"
        f"or install the needed packages manually, e.g.:\n"
        f"  pip install flask flask_sqlalchemy flask_migrate flask_jwt_extended flask_cors flask_bcrypt python-dotenv"
    ) from e

from config import Config, ProductionConfig, DevelopmentConfig, TestingConfig

# Load environment variables
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=None):
    """Application factory pattern with environment-based config selection"""
    if config_class is None:
        # Auto-select config based on FLASK_ENV environment variable
        flask_env = os.environ.get('FLASK_ENV', 'development')
        if flask_env == 'production':
            config_class = ProductionConfig
        elif flask_env == 'testing':
            config_class = TestingConfig
        else:
            config_class = DevelopmentConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS for frontend
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.diagnosis import diagnosis_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(diagnosis_bp, url_prefix='/diagnosis')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Create upload directory (exist_ok=True prevents race condition with multiple workers)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables initialized successfully!")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")

    # Root health check endpoint for deployment verification
    @app.route('/')
    def root():
        return jsonify({
            'status': 'healthy',
            'message': 'Agri Smart Detect Backend API is running',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/auth',
                'diagnosis': '/diagnosis',
                'reports': '/reports'
            }
        }), 200

    @app.route('/health')
    def health():
        """Health check endpoint for monitoring"""
        try:
            # Test database connection
            db.session.execute(db.text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'message': 'All systems operational'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 503

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app