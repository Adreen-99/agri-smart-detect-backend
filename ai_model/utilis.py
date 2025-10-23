# utils/seed.py
from flask import jsonify, make_response
from app import db

def seed_database():
    """
    Populates the database with essential starting data (Crops, Diseases, Treatments).
    Call this after `flask db upgrade`.
    """
    from models.crop import Crop
    from models.disease import Disease, DiseaseTreatment
    from models.treatment import Treatment
    from models.user import User
    from models.report import Report  

    print("--- Starting Database Seeding ---")

    # Clear existing data to prevent conflicts
    db.session.query(DiseaseTreatment).delete()
    db.session.query(Report).delete()
    db.session.query(Disease).delete()
    db.session.query(Treatment).delete()
    db.session.query(Crop).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("Old data cleared.")

    # 1. Crops
    crops = [
        Crop(name='Tomato', scientific_name='Solanum lycopersicum', base_region='Highlands'),
        Crop(name='Maize', scientific_name='Zea mays', base_region='All Regions'),
        Crop(name='Potato', scientific_name='Solanum tuberosum', base_region='Highlands'),
    ]
    db.session.add_all(crops)
    db.session.commit()
    print(f"Added {len(crops)} crops.")

    # 2. Diseases
    diseases = [
        Disease(name='Tomato Leaf Spot', symptoms='Small, dark spots on leaves.', cause='Fungus', ai_model_accuracy=0.95),
        Disease(name='Maize Lethal Necrosis', symptoms='Yellowing from lower leaves up.', cause='Virus', ai_model_accuracy=0.88),
        Disease(name='Healthy Plant', symptoms='No observable symptoms.', cause='N/A', ai_model_accuracy=1.0),
    ]
    db.session.add_all(diseases)
    db.session.commit()
    print(f"Added {len(diseases)} diseases.")

    # 3. Treatments
    treatments = [
        Treatment(name='Copper Fungicide', description='Apply copper-based fungicide weekly.', organic_status=True, cost_estimate='Low'),
        Treatment(name='Remove Infected Leaves', description='Prune and destroy infected leaves immediately.', organic_status=True, cost_estimate='Very Low'),
        Treatment(name='Chlorothalonil Spray', description='Apply broad-spectrum chemical spray (non-organic).', organic_status=False, cost_estimate='Medium'),
    ]
    db.session.add_all(treatments)
    db.session.commit()
    print(f"Added {len(treatments)} treatments.")

    # 4. Disease-Treatment Links
    tomato_spot = Disease.query.filter_by(name='Tomato Leaf Spot').first()
    if tomato_spot:
        links = [
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[1].id, priority_rank=1),
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[0].id, priority_rank=2),
            DiseaseTreatment(disease_id=tomato_spot.id, treatment_id=treatments[2].id, priority_rank=3),
        ]
        db.session.add_all(links)
        db.session.commit()
        print("Disease-Treatment links created.")

    print("--- Database Seeding Complete ---")


# --- JSON Response Helper ---
def make_json_response(data=None, status_code=200, errors=None):
    """
    Standardizes JSON responses for Flask APIs.
    """
    payload = {
        'success': status_code < 400,
        'data': data if data is not None else [],
        'errors': errors if errors is not None else []
    }
    return make_response(jsonify(payload), status_code)
