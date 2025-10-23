#!/usr/bin/env python3
"""
Seed script to populate the Agri-Smart Detect database with mock data.
"""

from app import app, db, bcrypt
from models.user import User
from models.crop import Crop
from models.disease import Disease, DiseaseTreatment
from models.treatment import Treatment
from models.report import Report
from datetime import datetime, timedelta
import random

# ------------------- Seed Functions ------------------- #

def seed_users():
    print("Seeding users...")
    users_data = [
        {'username': 'john_farmer', 'password': 'password123', 'phone_number': '+254712345678', 'county': 'Kiambu', 'is_extension_agent': False},
        {'username': 'mary_farmer', 'password': 'password123', 'phone_number': '+254723456789', 'county': 'Nakuru', 'is_extension_agent': False},
        {'username': 'agent_smith', 'password': 'password123', 'phone_number': '+254734567890', 'county': 'Nairobi', 'is_extension_agent': True},
        {'username': 'sarah_wanjiku', 'password': 'password123', 'phone_number': '+254745678901', 'county': 'Muranga', 'is_extension_agent': False},
        {'username': 'agent_johnson', 'password': 'password123', 'phone_number': '+254756789012', 'county': 'Kisumu', 'is_extension_agent': True},
        {'username': 'peter_kamau', 'password': 'password123', 'phone_number': '+254767890123', 'county': 'Meru', 'is_extension_agent': False}
    ]

    for data in users_data:
        if User.query.filter_by(username=data['username']).first():
            continue
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            username=data['username'],
            password_hash=password_hash,
            phone_number=data['phone_number'],
            county=data['county'],
            is_extension_agent=data['is_extension_agent']
        )
        db.session.add(user)
    db.session.commit()
    print(f"✅ Created {len(users_data)} users")

def seed_crops():
    print("Seeding crops...")
    crops_data = [
        {'name': 'Maize', 'scientific_name': 'Zea mays', 'base_region': 'Rift Valley, Western Kenya'},
        {'name': 'Beans', 'scientific_name': 'Phaseolus vulgaris', 'base_region': 'Central Kenya, Eastern Kenya'},
        {'name': 'Potatoes', 'scientific_name': 'Solanum tuberosum', 'base_region': 'Central Kenya, Rift Valley'},
        {'name': 'Tomatoes', 'scientific_name': 'Solanum lycopersicum', 'base_region': 'Central Kenya, Coast Region'},
        {'name': 'Cabbage', 'scientific_name': 'Brassica oleracea', 'base_region': 'Central Kenya, Nairobi'},
        {'name': 'Kale', 'scientific_name': 'Brassica oleracea var. acephala', 'base_region': 'Central Kenya, Rift Valley'},
        {'name': 'Rice', 'scientific_name': 'Oryza sativa', 'base_region': 'Nyanza, Coast Region'},
        {'name': 'Wheat', 'scientific_name': 'Triticum aestivum', 'base_region': 'Rift Valley, North Eastern'}
    ]
    for data in crops_data:
        if Crop.query.filter_by(name=data['name']).first():
            continue
        db.session.add(Crop(**data))
    db.session.commit()
    print(f"✅ Created {len(crops_data)} crops")

def seed_diseases():
    print("Seeding diseases...")
    diseases_data = [
        {'name': 'Maize Streak Virus', 'symptoms': 'Yellow streaks on leaves', 'cause': 'Maize streak virus transmitted by leafhoppers', 'ai_model_accuracy': 0.92},
        {'name': 'Late Blight', 'symptoms': 'Dark lesions on leaves', 'cause': 'Phytophthora infestans fungus', 'ai_model_accuracy': 0.88},
        {'name': 'Bean Rust', 'symptoms': 'Orange-brown pustules on leaves', 'cause': 'Uromyces appendiculatus fungus', 'ai_model_accuracy': 0.85},
        {'name': 'Bacterial Wilt', 'symptoms': 'Wilting of plants', 'cause': 'Ralstonia solanacearum bacteria', 'ai_model_accuracy': 0.90},
        {'name': 'Diamondback Moth', 'symptoms': 'Holes in leaves', 'cause': 'Plutella xylostella insect pest', 'ai_model_accuracy': 0.87},
        {'name': 'Anthracnose', 'symptoms': 'Dark sunken lesions on pods', 'cause': 'Colletotrichum lindemuthianum fungus', 'ai_model_accuracy': 0.83},
        {'name': 'Rice Blast', 'symptoms': 'Diamond-shaped lesions', 'cause': 'Magnaporthe oryzae fungus', 'ai_model_accuracy': 0.89},
        {'name': 'Wheat Stem Rust', 'symptoms': 'Reddish-brown pustules', 'cause': 'Puccinia graminis fungus', 'ai_model_accuracy': 0.91}
    ]
    for data in diseases_data:
        if Disease.query.filter_by(name=data['name']).first():
            continue
        db.session.add(Disease(**data))
    db.session.commit()
    print(f"✅ Created {len(diseases_data)} diseases")

def seed_treatments():
    print("Seeding treatments...")
    treatments_data = [
        {'name': 'Copper-based Fungicide', 'description': 'Chemical fungicide', 'organic_status': False, 'cost_estimate': 'KES 800-1200 per litre'},
        {'name': 'Neem Oil Spray', 'description': 'Organic pesticide', 'organic_status': True, 'cost_estimate': 'KES 600-900 per litre'},
        {'name': 'Bacillus subtilis', 'description': 'Biological control agent', 'organic_status': True, 'cost_estimate': 'KES 1500-2000 per kg'},
        {'name': 'Mancozeb Fungicide', 'description': 'Broad-spectrum chemical fungicide', 'organic_status': False, 'cost_estimate': 'KES 1000-1500 per kg'},
        {'name': 'Compost Tea', 'description': 'Organic fertilizer', 'organic_status': True, 'cost_estimate': 'KES 200-400 per litre'},
        {'name': 'Pyrethrin-based Insecticide', 'description': 'Natural insecticide', 'organic_status': True, 'cost_estimate': 'KES 1200-1800 per litre'},
        {'name': 'Trichoderma harzianum', 'description': 'Beneficial fungus', 'organic_status': True, 'cost_estimate': 'KES 800-1200 per kg'},
        {'name': 'Systemic Insecticide', 'description': 'Chemical insecticide', 'organic_status': False, 'cost_estimate': 'KES 2000-3000 per litre'},
        {'name': 'Plant Growth Promoters', 'description': 'Organic compounds', 'organic_status': True, 'cost_estimate': 'KES 500-800 per litre'},
        {'name': 'Sulfur-based Fungicide', 'description': 'Chemical fungicide', 'organic_status': False, 'cost_estimate': 'KES 400-600 per kg'}
    ]
    for data in treatments_data:
        if Treatment.query.filter_by(name=data['name']).first():
            continue
        db.session.add(Treatment(**data))
    db.session.commit()
    print(f"✅ Created {len(treatments_data)} treatments")

def seed_disease_treatments():
    print("Seeding disease-treatment relationships...")
    mapping = {
        'Maize Streak Virus': ['Neem Oil Spray', 'Plant Growth Promoters'],
        'Late Blight': ['Copper-based Fungicide', 'Mancozeb Fungicide', 'Bacillus subtilis'],
        'Bean Rust': ['Sulfur-based Fungicide', 'Copper-based Fungicide', 'Trichoderma harzianum'],
        'Bacterial Wilt': ['Bacillus subtilis', 'Trichoderma harzianum', 'Compost Tea'],
        'Diamondback Moth': ['Neem Oil Spray', 'Pyrethrin-based Insecticide', 'Systemic Insecticide'],
        'Anthracnose': ['Copper-based Fungicide', 'Mancozeb Fungicide', 'Bacillus subtilis'],
        'Rice Blast': ['Trichoderma harzianum', 'Copper-based Fungicide', 'Sulfur-based Fungicide'],
        'Wheat Stem Rust': ['Mancozeb Fungicide', 'Copper-based Fungicide', 'Plant Growth Promoters']
    }

    for disease_name, treatment_names in mapping.items():
        disease = Disease.query.filter_by(name=disease_name).first()
        if not disease:
            continue
        for i, treatment_name in enumerate(treatment_names, 1):
            treatment = Treatment.query.filter_by(name=treatment_name).first()
            if not treatment:
                continue
            if not DiseaseTreatment.query.filter_by(disease_id=disease.id, treatment_id=treatment.id).first():
                db.session.add(DiseaseTreatment(disease_id=disease.id, treatment_id=treatment.id, priority_rank=i))
    db.session.commit()
    print("✅ Disease-treatment relationships seeded")

# ------------------- Main Seeder ------------------- #
def main():
    print("🌱 Starting database seeding...")
    with app.app_context():
        seed_users()
        seed_crops()
        seed_diseases()
        seed_treatments()
        seed_disease_treatments()
        print("✅ Database seeding completed successfully!")

if __name__ == '__main__':
    main()
