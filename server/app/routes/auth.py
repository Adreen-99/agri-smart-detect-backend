from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from app.models.user import User
from app import bcrypt, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Your registration logic
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    # Your login logic
    pass