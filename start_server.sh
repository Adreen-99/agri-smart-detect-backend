#!/bin/bash
# Start the Agri Smart Detect backend server

# Activate virtual environment
source .venv/bin/activate

# Set PORT if not set
export PORT=${PORT:-8000}

# Run gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 'app:create_app()'
