# models/crop.py

from app import db
from sqlalchemy_serializer import SerializerMixin

class Crop(db.Model, SerializerMixin):
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    scientific_name = db.Column(db.String(100))
    base_region = db.Column(db.String(100))

    # Relationships
    reports = db.relationship(
        'Report',
        backref=db.backref('crop', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Serialization Rules
    serialize_rules = ('-reports',)

    def __repr__(self):
        return f'<Crop {self.name}>'
