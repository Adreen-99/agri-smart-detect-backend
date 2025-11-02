import os
os.environ['FLASK_ENV'] = 'development'  # Force development mode

from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Agri Smart Detect Backend running on port {port} (debug={debug_mode})")
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
