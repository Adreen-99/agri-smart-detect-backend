#!/usr/bin/env python3
"""
Seed script to populate the Agri-Smart Detect database with mock data.
This script creates realistic sample data for testing and development purposes.
"""

from app import app, db
from models.user import User
from models.crop import Crop
from disease import Disease, DiseaseTreatment
from treatment import Treatment
from report import Report
from datetime import datetime, timedelta
import random
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def seed_users():
    """Create sample users (farmers and extension agents)"""
    print("Seeding users...")

    users_data = [
        {
            'username': 'john_farmer',
            'password': 'password123',
            'phone_number': '+254712345678',
            'county': 'Kiambu',
            'is_extension_agent': False
        },
        {
            'username': 'mary_farmer',
            'password': 'password123',
            'phone_number': '+254723456789',
            'county': 'Nakuru',
            'is_extension_agent': False
        },
        {
            'username': 'agent_smith',
            'password': 'password123',
            'phone_number': '+254734567890',
            'county': 'Nairobi',
            'is_extension_agent': True
        },
        {
            'username': 'sarah_wanjiku',
            'password': 'password123',
            'phone_number': '+254745678901',
            'county': 'Muranga',
            'is_extension_agent': False
        },
        {
            'username': 'agent_johnson',
            'password': 'password123',
            'phone_number': '+254756789012',
            'county': 'Kisumu',
            'is_extension_agent': True
        },
        {
            'username': 'peter_kamau',
            'password': 'password123',
            'phone_number': '+254767890123',
            'county': 'Meru',
            'is_extension_agent': False
        }
    ]

    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if existing_user:
            continue

        # Hash the password
        password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        user = User(
            username=user_data['username'],
            password_hash=password_hash,
            phone_number=user_data['phone_number'],
            county=user_data['county'],
            is_extension_agent=user_data['is_extension_agent']
        )
        db.session.add(user)

    db.session.commit()
    print(f"Created {len(users_data)} users")

def seed_crops():
    """Create sample crops commonly grown in Kenya"""
    print("Seeding crops...")

    crops_data = [
        {
            'name': 'Maize',
            'scientific_name': 'Zea mays',
            'base_region': 'Rift Valley, Western Kenya'
        },
        {
            'name': 'Beans',
            'scientific_name': 'Phaseolus vulgaris',
            'base_region': 'Central Kenya, Eastern Kenya'
        },
        {
            'name': 'Potatoes',
            'scientific_name': 'Solanum tuberosum',
            'base_region': 'Central Kenya, Rift Valley'
        },
        {
            'name': 'Tomatoes',
            'scientific_name': 'Solanum lycopersicum',
            'base_region': 'Central Kenya, Coast Region'
        },
        {
            'name': 'Cabbage',
            'scientific_name': 'Brassica oleracea',
            'base_region': 'Central Kenya, Nairobi'
        },
        {
            'name': 'Kale',
            'scientific_name': 'Brassica oleracea var. acephala',
            'base_region': 'Central Kenya, Rift Valley'
        },
        {
            'name': 'Rice',
            'scientific_name': 'Oryza sativa',
            'base_region': 'Nyanza, Coast Region'
        },
        {
            'name': 'Wheat',
            'scientific_name': 'Triticum aestivum',
            'base_region': 'Rift Valley, North Eastern'
        }
    ]

    for crop_data in crops_data:
        # Check if crop already exists
        existing_crop = Crop.query.filter_by(name=crop_data['name']).first()
        if existing_crop:
            continue

        crop = Crop(
            name=crop_data['name'],
            scientific_name=crop_data['scientific_name'],
            base_region=crop_data['base_region']
        )
        db.session.add(crop)

    db.session.commit()
    print(f"Created {len(crops_data)} crops")

def seed_diseases():
    """Create sample crop diseases"""
    print("Seeding diseases...")

    diseases_data = [
        {
            'name': 'Maize Streak Virus',
            'symptoms': 'Yellow streaks on leaves, stunted growth, reduced yield',
            'cause': 'Maize streak virus transmitted by leafhoppers',
            'ai_model_accuracy': 0.92
        },
        {
            'name': 'Late Blight',
            'symptoms': 'Dark lesions on leaves and stems, white mold on undersides',
            'cause': 'Phytophthora infestans fungus',
            'ai_model_accuracy': 0.88
        },
        {
            'name': 'Bean Rust',
            'symptoms': 'Orange-brown pustules on leaves, premature defoliation',
            'cause': 'Uromyces appendiculatus fungus',
            'ai_model_accuracy': 0.85
        },
        {
            'name': 'Bacterial Wilt',
            'symptoms': 'Wilting of plants, yellowing leaves, vascular discoloration',
            'cause': 'Ralstonia solanacearum bacteria',
            'ai_model_accuracy': 0.90
        },
        {
            'name': 'Diamondback Moth',
            'symptoms': 'Holes in leaves, larvae feeding damage, reduced photosynthesis',
            'cause': 'Plutella xylostella insect pest',
            'ai_model_accuracy': 0.87
        },
        {
            'name': 'Anthracnose',
            'symptoms': 'Dark sunken lesions on pods and stems, seed discoloration',
            'cause': 'Colletotrichum lindemuthianum fungus',
            'ai_model_accuracy': 0.83
        },
        {
            'name': 'Rice Blast',
            'symptoms': 'Diamond-shaped lesions with gray centers and brown borders',
            'cause': 'Magnaporthe oryzae fungus',
            'ai_model_accuracy': 0.89
        },
        {
            'name': 'Wheat Stem Rust',
            'symptoms': 'Reddish-brown pustules on stems and leaves',
            'cause': 'Puccinia graminis fungus',
            'ai_model_accuracy': 0.91
        }
    ]

    for disease_data in diseases_data:
        # Check if disease already exists
        existing_disease = Disease.query.filter_by(name=disease_data['name']).first()
        if existing_disease:
            continue

        disease = Disease(
            name=disease_data['name'],
            symptoms=disease_data['symptoms'],
            cause=disease_data['cause'],
            ai_model_accuracy=disease_data['ai_model_accuracy']
        )
        db.session.add(disease)

    db.session.commit()
    print(f"Created {len(diseases_data)} diseases")

def seed_treatments():
    """Create sample treatments (both organic and chemical)"""
    print("Seeding treatments...")

    treatments_data = [
        {
            'name': 'Copper-based Fungicide',
            'description': 'Chemical fungicide containing copper oxychloride for controlling fungal diseases',
            'organic_status': False,
            'cost_estimate': 'KES 800-1200 per litre'
        },
        {
            'name': 'Neem Oil Spray',
            'description': 'Organic pesticide made from neem tree seeds, effective against various pests',
            'organic_status': True,
            'cost_estimate': 'KES 600-900 per litre'
        },
        {
            'name': 'Bacillus subtilis',
            'description': 'Biological control agent that colonizes plant roots and prevents disease',
            'organic_status': True,
            'cost_estimate': 'KES 1500-2000 per kg'
        },
        {
            'name': 'Mancozeb Fungicide',
            'description': 'Broad-spectrum chemical fungicide for controlling various fungal diseases',
            'organic_status': False,
            'cost_estimate': 'KES 1000-1500 per kg'
        },
        {
            'name': 'Compost Tea',
            'description': 'Organic fertilizer and disease suppressant made from composted materials',
            'organic_status': True,
            'cost_estimate': 'KES 200-400 per litre'
        },
        {
            'name': 'Pyrethrin-based Insecticide',
            'description': 'Natural insecticide derived from pyrethrum flowers',
            'organic_status': True,
            'cost_estimate': 'KES 1200-1800 per litre'
        },
        {
            'name': 'Trichoderma harzianum',
            'description': 'Beneficial fungus that controls soil-borne diseases',
            'organic_status': True,
            'cost_estimate': 'KES 800-1200 per kg'
        },
        {
            'name': 'Systemic Insecticide',
            'description': 'Chemical insecticide absorbed by plants to control sucking insects',
            'organic_status': False,
            'cost_estimate': 'KES 2000-3000 per litre'
        },
        {
            'name': 'Plant Growth Promoters',
            'description': 'Organic compounds that enhance plant resistance to diseases',
            'organic_status': True,
            'cost_estimate': 'KES 500-800 per litre'
        },
        {
            'name': 'Sulfur-based Fungicide',
            'description': 'Chemical fungicide using elemental sulfur for powdery mildew control',
            'organic_status': False,
            'cost_estimate': 'KES 400-600 per kg'
        }
    ]

    for treatment_data in treatments_data:
        # Check if treatment already exists
        existing_treatment = Treatment.query.filter_by(name=treatment_data['name']).first()
        if existing_treatment:
            continue

        treatment = Treatment(
            name=treatment_data['name'],
            description=treatment_data['description'],
            organic_status=treatment_data['organic_status'],
            cost_estimate=treatment_data['cost_estimate']
        )
        db.session.add(treatment)

    db.session.commit()
    print(f"Created {len(treatments_data)} treatments")

def seed_disease_treatments():
    """Create relationships between diseases and treatments"""
    print("Seeding disease-treatment relationships...")

    # Get all diseases and treatments
    diseases = Disease.query.all()
    treatments = Treatment.query.all()

    if not diseases or not treatments:
        print("No diseases or treatments found. Skipping disease-treatment relationships.")
        return

    # Define which treatments work for which diseases
    disease_treatment_mapping = {
        'Maize Streak Virus': ['Neem Oil Spray', 'Plant Growth Promoters'],
        'Late Blight': ['Copper-based Fungicide', 'Mancozeb Fungicide', 'Bacillus subtilis'],
        'Bean Rust': ['Sulfur-based Fungicide', 'Copper-based Fungicide', 'Trichoderma harzianum'],
        'Bacterial Wilt': ['Bacillus subtilis', 'Trichoderma harzianum', 'Compost Tea'],
        'Diamondback Moth': ['Neem Oil Spray', 'Pyrethrin-based Insecticide', 'Systemic Insecticide'],
        'Anthracnose': ['Copper-based Fungicide', 'Mancozeb Fungicide', 'Bacillus subtilis'],
        'Rice Blast': ['Trichoderma harzianum', 'Copper-based Fungicide', 'Sulfur-based Fungicide'],
        'Wheat Stem Rust': ['Mancozeb Fungicide', 'Copper-based Fungicide', 'Plant Growth Promoters']
    }

    priority_counter = 1
    for disease_name, treatment_names in disease_treatment_mapping.items():
        disease = next((d for d in diseases if d.name == disease_name), None)
        if not disease:
            continue

        for i, treatment_name in enumerate(treatment_names):
            treatment = next((t for t in treatments if t.name == treatment_name), None)
            if not treatment:
                continue

            # Check if relationship already exists
            existing_relationship = DiseaseTreatment.query.filter_by(
                disease_id=disease.id,
                treatment_id=treatment.id
            ).first()

            if not existing_relationship:
                disease_treatment = DiseaseTreatment(
                    disease_id=disease.id,
                    treatment_id=treatment.id,
                    priority_rank=priority_counter
                )
                db.session.add(disease_treatment)
                priority_counter += 1

    db.session.commit()
    relationships_created = DiseaseTreatment.query.count()
    print(f"Created {relationships_created} disease-treatment relationships")

def seed_reports():
    """Create sample reports linking users, crops, and diseases"""
    print("Seeding reports...")

    # Get all users, crops, and diseases
    users = User.query.all()
    crops = Crop.query.all()
    diseases = Disease.query.all()

    if not users or not crops or not diseases:
        print("No users, crops, or diseases found. Skipping reports.")
        return

    # Sample image URLs (placeholder URLs for demo)
    image_urls = [
        'https://example.com/images/maize_streak_001.jpg',
        'https://example.com/images/late_blight_002.jpg',
        'https://example.com/images/bean_rust_003.jpg',
        'https://example.com/images/bacterial_wilt_004.jpg',
        'https://example.com/images/diamondback_moth_005.jpg',
        'https://example.com/images/anthracnose_006.jpg',
        'https://example.com/images/rice_blast_007.jpg',
        'https://example.com/images/wheat_rust_008.jpg'
    ]

    reports_data = []

    # Create 15-20 sample reports with varied data
    for i in range(18):
        user = random.choice(users)
        crop = random.choice(crops)
        disease = random.choice(diseases)

        # Generate random date within the last 30 days
        days_ago = random.randint(1, 30)
        submission_date = datetime.utcnow() - timedelta(days=days_ago)

        # Generate realistic confidence score based on disease AI accuracy
        base_accuracy = disease.ai_model_accuracy or 0.85
        confidence_score = round(random.uniform(base_accuracy - 0.15, min(base_accuracy + 0.1, 0.98)), 3)

        # 70% of reports are marked as accurate (verified by extension agents)
        is_accurate = random.choices([True, False], weights=[70, 30])[0]

        report = Report(
            user_id=user.id,
            crop_id=crop.id,
            disease_id=disease.id,
            image_url=random.choice(image_urls),
            confidence_score=confidence_score,
            is_accurate=is_accurate,
            submission_date=submission_date
        )
        reports_data.append(report)

    # Add all reports to session
    for report in reports_data:
        db.session.add(report)

    db.session.commit()
    print(f"Created {len(reports_data)} reports")

def main():
    """Main function to run all seeding operations"""
    print("🌱 Starting database seeding...")

    with app.app_context():
        try:
            # Clear existing data (optional - comment out if you want to keep existing data)
            # db.drop_all()
            # db.create_all()

            # Seed data in order (respecting foreign key constraints)
            seed_users()
            seed_crops()
            seed_diseases()
            seed_treatments()
            seed_disease_treatments()
            seed_reports()

            print("✅ Database seeding completed successfully!")
            print("\n📊 Summary of seeded data:")

            with app.app_context():
                print(f"   • Users: {User.query.count()}")
                print(f"   • Crops: {Crop.query.count()}")
                print(f"   • Diseases: {Disease.query.count()}")
                print(f"   • Treatments: {Treatment.query.count()}")
                print(f"   • Disease-Treatment Relationships: {DiseaseTreatment.query.count()}")
                print(f"   • Reports: {Report.query.count()}")

        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()