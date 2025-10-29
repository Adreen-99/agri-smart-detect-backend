from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.email_service import EmailService
import uuid
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# In-memory store for reset tokens (use Redis in production)
reset_tokens = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'farm_name', 'farm_size', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            farm_name=data['farm_name'],
            farm_size=float(data['farm_size']),
            location=data['location']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        # Send welcome email
        try:
            email_service = EmailService()
            email_service.send_welcome_email(user.email, user.name)
        except Exception as e:
            print(f"Failed to send welcome email: {e}")
            # Don't fail registration if email fails
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset token
            reset_token = str(uuid.uuid4())
            reset_tokens[reset_token] = {
                'user_id': user.id,
                'expires': datetime.utcnow() + timedelta(hours=1)
            }
            
            # Send password reset email
            email_service = EmailService()
            email_service.send_password_reset(user.email, reset_token)
        
        # Always return success to prevent email enumeration
        return jsonify({
            'message': 'If an account with that email exists, a password reset link has been sent.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        # Validate token
        token_data = reset_tokens.get(token)
        if not token_data:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        if datetime.utcnow() > token_data['expires']:
            del reset_tokens[token]
            return jsonify({'error': 'Reset token has expired'}), 400
        
        # Update user password
        user = User.query.get(token_data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.set_password(new_password)
        db.session.commit()
        
        # Clean up used token
        del reset_tokens[token]
        
        return jsonify({
            'message': 'Password reset successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500