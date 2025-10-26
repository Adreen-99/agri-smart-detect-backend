# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models 
from .crop import Crop
from .disease import Disease, DiseaseTreatment
from .treatment import Treatment
from .report import Report
from .user import User

