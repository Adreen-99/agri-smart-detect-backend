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

from models import db, User, Crop, Disease, DiseaseTreatment, Treatment, Report

# Initialize extensions
db.init_app(app)       
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)

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

# USER CRUD ROUTES
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        try:
            users = User.query.all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return make_response(
                jsonify({'errors': ['Missing required fields: username and password']}), 400
            )

        try:
            password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(
                username=data['username'],
                password_hash=password_hash,
                phone_number=data.get('phone_number'),
                county=data.get('county'),
                is_extension_agent=data.get('is_extension_agent', False)
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify(new_user.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [f'Could not create user: {str(e)}']}), 500)

@app.route('/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
def user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            if 'username' in data:
                user.username = data['username']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            if 'county' in data:
                user.county = data['county']
            if 'is_extension_agent' in data:
                user.is_extension_agent = data['is_extension_agent']
            if 'password' in data:
                user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(user)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

# CROP CRUD ROUTES
@app.route('/crops', methods=['GET', 'POST'])
def crops():
    if request.method == 'GET':
        try:
            crops = Crop.query.all()
            return jsonify([crop.to_dict() for crop in crops]), 200
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return make_response(
                jsonify({'errors': ['Missing required field: name']}), 400
            )

        try:
            new_crop = Crop(
                name=data['name'],
                scientific_name=data.get('scientific_name'),
                base_region=data.get('base_region')
            )
            db.session.add(new_crop)
            db.session.commit()
            return make_response(jsonify(new_crop.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [f'Could not create crop: {str(e)}']}), 500)

@app.route('/crops/<int:crop_id>', methods=['GET', 'PATCH', 'DELETE'])
def crop_by_id(crop_id):
    crop = Crop.query.get(crop_id)
    if not crop:
        return make_response(jsonify({'error': 'Crop not found'}), 404)

    if request.method == 'GET':
        return jsonify(crop.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            if 'name' in data:
                crop.name = data['name']
            if 'scientific_name' in data:
                crop.scientific_name = data['scientific_name']
            if 'base_region' in data:
                crop.base_region = data['base_region']
            db.session.commit()
            return jsonify(crop.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(crop)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

# DISEASE CRUD ROUTES
@app.route('/diseases', methods=['GET', 'POST'])
def diseases():
    if request.method == 'GET':
        try:
            diseases = Disease.query.all()
            return jsonify([disease.to_dict() for disease in diseases]), 200
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return make_response(
                jsonify({'errors': ['Missing required field: name']}), 400
            )

        try:
            new_disease = Disease(
                name=data['name'],
                symptoms=data.get('symptoms'),
                cause=data.get('cause'),
                ai_model_accuracy=data.get('ai_model_accuracy')
            )
            db.session.add(new_disease)
            db.session.commit()
            return make_response(jsonify(new_disease.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [f'Could not create disease: {str(e)}']}), 500)

@app.route('/diseases/<int:disease_id>', methods=['GET', 'PATCH', 'DELETE'])
def disease_by_id(disease_id):
    disease = Disease.query.get(disease_id)
    if not disease:
        return make_response(jsonify({'error': 'Disease not found'}), 404)

    if request.method == 'GET':
        return jsonify(disease.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            if 'name' in data:
                disease.name = data['name']
            if 'symptoms' in data:
                disease.symptoms = data['symptoms']
            if 'cause' in data:
                disease.cause = data['cause']
            if 'ai_model_accuracy' in data:
                disease.ai_model_accuracy = data['ai_model_accuracy']
            db.session.commit()
            return jsonify(disease.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(disease)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

# TREATMENT CRUD ROUTES
@app.route('/treatments', methods=['GET', 'POST'])
def treatments():
    if request.method == 'GET':
        try:
            treatments = Treatment.query.all()
            return jsonify([treatment.to_dict() for treatment in treatments]), 200
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return make_response(
                jsonify({'errors': ['Missing required field: name']}), 400
            )

        try:
            new_treatment = Treatment(
                name=data['name'],
                description=data.get('description'),
                organic_status=data.get('organic_status'),
                cost_estimate=data.get('cost_estimate')
            )
            db.session.add(new_treatment)
            db.session.commit()
            return make_response(jsonify(new_treatment.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [f'Could not create treatment: {str(e)}']}), 500)

@app.route('/treatments/<int:treatment_id>', methods=['GET', 'PATCH', 'DELETE'])
def treatment_by_id(treatment_id):
    treatment = Treatment.query.get(treatment_id)
    if not treatment:
        return make_response(jsonify({'error': 'Treatment not found'}), 404)

    if request.method == 'GET':
        return jsonify(treatment.to_dict()), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            if 'name' in data:
                treatment.name = data['name']
            if 'description' in data:
                treatment.description = data['description']
            if 'organic_status' in data:
                treatment.organic_status = data['organic_status']
            if 'cost_estimate' in data:
                treatment.cost_estimate = data['cost_estimate']
            db.session.commit()
            return jsonify(treatment.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

    elif request.method == 'DELETE':
        try:
            db.session.delete(treatment)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 500)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(port=port, debug=True)
