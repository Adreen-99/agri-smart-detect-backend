# app.py
from flask import Flask, jsonify, request, make_response
from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key_change_me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///agri_smart.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db

# Initialize extensions
db.init_app(app)       # ✅ db now exists
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)

# Import models 
from models.user import User
from models.crop import Crop
from models.disease import Disease, DiseaseTreatment
from models.treatment import Treatment
from models.report import Report

# Home Route
@app.route('/')
def home():
    return '<h1>Agri-Smart Detect Backend Running!</h1>'

# REPORT CRUD ROUTES
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'GET':
        try:
            reports = Report.query.limit(20).all()
            return jsonify([report.to_dict() for report in reports]), 200
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'image_data' not in data:
            return make_response(
                jsonify({'errors': ['Missing required image data or crop selection']}), 400
            )

        simulated_disease_id = 1
        simulated_confidence = 0.925

        try:
            new_report = Report(
                user_id=data.get('user_id', 1),
                crop_id=data['crop_id'],
                disease_id=simulated_disease_id,
                image_url='http://simulated-image-url.com',
                confidence_score=simulated_confidence,
            )
            db.session.add(new_report)
            db.session.commit()
            return make_response(jsonify(new_report.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [f'Could not process report: {str(e)}']}), 500)

# REPORT DETAIL ROUTE
@app.route('/reports/<int:report_id>', methods=['GET', 'PATCH', 'DELETE'])
def report_by_id(report_id):
    report = Report.query.get(report_id)
    if not report:
        return make_response(jsonify({'error': 'Report not found'}), 404)

    if request.method == 'GET':
        return jsonify(report.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        if 'is_accurate' in data:
            try:
                if not isinstance(data['is_accurate'], bool):
                    return make_response(jsonify({'error': 'is_accurate must be a boolean'}), 400)
                report.is_accurate = data['is_accurate']
                db.session.commit()
                return jsonify(report.to_dict()), 200
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({'errors': [str(e)]}), 500)
        else:
            return make_response(jsonify({'error': 'No valid update field provided'}), 400)

    elif request.method == 'DELETE':
        try:
            db.session.delete(report)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

# USER REGISTRATION PLACEHOLDER
@app.route('/users', methods=['POST'])
def create_user():
    """Placeholder for user registration"""
    # TODO: Implement user registration using bcrypt hashing
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(port=port, debug=True)
