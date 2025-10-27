from . import db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

class Disease(db.Model, SerializerMixin):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.String)
    cause = db.Column(db.String)
    ai_model_accuracy = db.Column(db.Float)

    treatments = db.relationship(
        'DiseaseTreatment',
        backref=db.backref('disease', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    serialize_rules = ('-treatments.disease',)

    def __repr__(self):
        return f'<Disease {self.name}>'

class DiseaseTreatment(db.Model, SerializerMixin):
    __tablename__ = 'disease_treatments'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=False)
    priority_rank = db.Column(db.Integer)

    serialize_rules = ('-disease.treatments', '-treatment.disease_treatments',)

    def __repr__(self):
        return f'<DiseaseTreatment Disease:{self.disease_id} Treatment:{self.treatment_id}>'
