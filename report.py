# models/report.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Define the base (shared declarative base for migrations and model registration)
Base = declarative_base()

class Report(Base, SerializerMixin):
    __tablename__ = 'reports'

    # --- Columns ---
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    disease_id = Column(Integer, ForeignKey('diseases.id'), nullable=True)  # Linked predicted disease

    image_url = Column(String, nullable=False)  # Image path or URL
    confidence_score = Column(Float)
    is_accurate = Column(Boolean, default=False)
    submission_date = Column(DateTime, default=datetime.utcnow)

    # --- Serialization Rules ---
    (
        '-user.reports',
        '-crop.reports',
        'disease.treatments',
        'disease.treatments_link',
    )

    def __repr__(self):
        return f'<Report ID:{self.id} User:{self.user_id} Crop:{self.crop_id}>'
