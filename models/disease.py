# models/disease.py

from app import db
from sqlalchemy_serializer import SerializerMixin

class DiseaseTreatment(db.Model, SerializerMixin):
    __tablename__ = 'disease_treatment'

    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), primary_key=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), primary_key=True)
    priority_rank = db.Column(db.Integer, default=1, nullable=False)

    disease = db.relationship('Disease', back_populates='treatments_link')
    treatment = db.relationship('Treatment', back_populates='diseases_link')

    def __repr__(self):
        return f'<DiseaseTreatment disease_id={self.disease_id} treatment_id={self.treatment_id}>'


class Disease(db.Model, SerializerMixin):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    symptoms = db.Column(db.Text)
    cause = db.Column(db.String(255))
    ai_model_accuracy = db.Column(db.Float)

    # Relationships
    treatments_link = db.relationship(
        'DiseaseTreatment',
        back_populates='disease',
        cascade='all, delete-orphan'
    )
    treatments = db.relationship(
        'Treatment',
        secondary='disease_treatment',
        viewonly=True
    )
    reports = db.relationship(
        'Report',
        backref=db.backref('disease', lazy='joined'),
        lazy='dynamic'
    )

    # Serialization Rules
    serialize_rules = ('-reports', '-treatments_link',)

    def __repr__(self):
        return f'<Disease {self.name}>'
