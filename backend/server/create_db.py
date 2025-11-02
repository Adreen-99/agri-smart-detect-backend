import os
os.environ['FLASK_ENV'] = 'development'  # Force development mode

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print('✅ Database created successfully!')
        print('✅ Tables initialized!')
        
        # Verify the database file was created
        import os
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            print(f'✅ Database file exists: {db_path}')
            file_size = os.path.getsize(db_path)
            print(f'✅ Database file size: {file_size} bytes')
        else:
            print(f'❌ Database file not found: {db_path}')
            
    except Exception as e:
        print(f'❌ Database creation failed: {e}')
