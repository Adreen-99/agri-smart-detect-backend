import os
import sys
sys.path.append(os.path.dirname(__file__))

os.environ['FLASK_ENV'] = 'development'

from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

with app.app_context():
    print("=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        print(f"{rule.endpoint:50} {methods:20} {rule.rule}")
    print("=========================")
