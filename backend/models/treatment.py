from . import db
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy_serializer import SerializerMixin

class Treatment(db.Model, SerializerMixin):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    organic_status = db.Column(db.Boolean)
    cost_estimate = db.Column(db.String)

    disease_treatments = db.relationship(
        'DiseaseTreatment',
        backref=db.backref('treatment', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    serialize_rules = ('-disease_treatments.treatment',)

    def __repr__(self):
        return f'<Treatment {self.name}>'
