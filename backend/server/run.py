import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import User, Crop, Disease, Treatment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Crop': Crop,
        'Disease': Disease,
        'Treatment': Treatment
    }

def init_sample_data():
    """Initialize sample data matching frontend"""
    with app.app_context():
        # Create sample crops matching frontend
        crops = [
            Crop(name='Maize', scientific_name='Zea mays', common_names='Corn,Maize'),
            Crop(name='Cassava', scientific_name='Manihot esculenta', common_names='Cassava,Manioc'),
            Crop(name='Tomato', scientific_name='Solanum lycopersicum', common_names='Tomato'),
            Crop(name='Bean', scientific_name='Phaseolus vulgaris', common_names='Bean,Common Bean')
        ]
        
        for crop in crops:
            if not Crop.query.filter_by(name=crop.name).first():
                db.session.add(crop)
        
        db.session.commit()
        print("✅ Agri Smart Detect Backend initialized successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()

    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    print(f"🚀 Agri Smart Detect Backend running on port {port} (debug={debug_mode})")

    # Use gunicorn in production, Flask dev server in development
    if os.environ.get('FLASK_ENV') == 'production':
        from gunicorn.app.wsgiapp import WSGIApplication
        WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
    else:
        app.run(host='0.0.0.0', port=port, debug=debug_mode)