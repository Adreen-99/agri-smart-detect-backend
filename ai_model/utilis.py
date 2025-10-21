from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify, make_response
import os

# 1. Centralized Base Definition
# All models (User, Crop, Disease, etc.) should import this Base
Base = declarative_base()

# --- Database Seeding Function ---

def seed_database(db):
    """
    Populates the database with essential starting data (Crops, Diseases, Treatments).
    This function should be called once after flask db upgrade.
    
    :param db: The SQLAlchemy instance (db = SQLAlchemy(app)).
    """
    # Import models locally to avoid circular dependencies with db/Base setup
    from models.crop import Crop
    from models.disease import Disease, DiseaseTreatment
    from models.treatment import Treatment
    from models.user import User
    
    print("--- Starting Database Seeding ---")

    # Clear existing data to prevent primary key conflicts on re-run
    db.session.query(Crop).delete()
    db.session.query(DiseaseTreatment).delete()
    db.session.query(Disease).delete()
    db.session.query(Treatment).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("Old data cleared.")

    # 1. Create Crops
    crops = [
        Crop(name='Tomato', scientific_name='Solanum lycopersicum', base_region='Highlands'),
        Crop(name='Maize', scientific_name='Zea mays', base_region='All Regions'),
        Crop(name='Potato', scientific_name='Solanum tuberosum', base_region='Highlands'),
    ]
    db.session.add_all(crops)
    db.session.commit()
    print(f"Added {len(crops)} crops.")

    # 2. Create Diseases
    diseases = [
        Disease(name='Tomato Leaf Spot', symptoms='Small, dark spots on leaves.', cause='Fungus', ai_model_accuracy=0.95),
        Disease(name='Maize Lethal Necrosis', symptoms='Yellowing from lower leaves up.', cause='Virus', ai_model_accuracy=0.88),
        Disease(name='Healthy Plant', symptoms='No observable symptoms.', cause='N/A', ai_model_accuracy=1.0),
    ]
    db.session.add_all(diseases)
    db.session.commit()
    print(f"Added {len(diseases)} diseases.")
    
    # Get IDs for linking
    tomato_spot = Disease.query.filter_by(name='Tomato Leaf Spot').first()
    
    # 3. Create Treatments
    treatments = [
        # Organic
        Treatment(name='Copper Fungicide', description='Apply copper-based fungicide weekly.', organic_status=True, cost_estimate='Low'),
        Treatment(name='Remove Infected Leaves', description='Prune and destroy infected leaves immediately.', organic_status=True, cost_estimate='Very Low'),
        # Chemical
        Treatment(name='Chlorothalonil Spray', description='Apply broad-spectrum chemical spray (non-organic).', organic_status=False, cost_estimate='Medium'),
    ]
    db.session.add_all(treatments)
    db.session.commit()
    print(f"Added {len(treatments)} treatments.")
    
    # 4. Create Disease-Treatment Links (Many-to-Many)
    # Link Tomato Leaf Spot to all three treatments with priority
    if tomato_spot:
        links = [
            # Highest priority: Remove leaves
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[1].id, priority_rank=1), 
            # Organic fungicide
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[0].id, priority_rank=2),
            # Chemical fungicide
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[2].id, priority_rank=3),
        ]
        db.session.add_all(links)
        db.session.commit()
        print("Disease-Treatment links created.")

    print("--- Database Seeding Complete ---")

# --- API Response Helper ---

def make_json_response(data, status_code=200, errors=None):
    """
    Standardizes JSON responses for Flask API.
    
    :param data: The primary data payload (e.g., a list of serialized objects).
    :param status_code: HTTP status code.
    :param errors: List of error messages, if any.
    :return: A Flask Response object.
    """
    response_payload = {
        'success': status_code < 400,
        'data': data if data is not None else [],
        'errors': errors if errors is not None else []
    }
    return make_response(jsonify(response_payload), status_code)
