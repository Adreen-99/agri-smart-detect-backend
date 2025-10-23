# models/report.py

from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class Report(db.Model, SerializerMixin):
    __tablename__ = 'reports'

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), nullable=True)  # Linked predicted disease

    image_url = db.Column(db.String, nullable=False)  # Image path or URL
    confidence_score = db.Column(db.Float)
    is_accurate = db.Column(db.Boolean, default=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Relationships ---
    user = db.relationship('User', backref=db.backref('reports', lazy='dynamic', cascade='all, delete-orphan'))
    crop = db.relationship('Crop', backref=db.backref('reports', lazy='dynamic', cascade='all, delete-orphan'))
    disease = db.relationship('Disease', backref=db.backref('reports', lazy='dynamic'))

    # --- Serialization Rules ---
    serialize_rules = (
        '-user.reports',
        '-crop.reports',
        'disease.treatments',
        'disease.treatments_link'
    )

    def __repr__(self):
        return f'<Report ID:{self.id} User:{self.user_id} Crop:{self.crop_id}>'
