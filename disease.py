from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()

class DiseaseTreatment(Base, SerializerMixin):
    __tablename__ = 'disease_treatment'

    disease_id = Column(Integer, ForeignKey('diseases.id'), primary_key=True)
    treatment_id = Column(Integer, ForeignKey('treatments.id'), primary_key=True)
    priority_rank = Column(Integer, default=1, nullable=False) 

    disease = relationship("Disease", back_populates="treatments_link")
    treatment = relationship("Treatment", back_populates="diseases_link")

    def __repr__(self):
        return f'<DiseaseTreatment disease_id={self.disease_id} treatment_id={self.treatment_id}>'

# --- Disease Model ---
class Disease(Base, SerializerMixin):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    symptoms = Column(Text)
    cause = Column(String(255))
    ai_model_accuracy = Column(Float)

    treatments_link = relationship(
        'DiseaseTreatment',
        back_populates='disease',
        cascade='all, delete-orphan'
    )

    treatments = relationship(
        'Treatment',
        secondary='disease_treatment',
        viewonly=True
    )

    reports = relationship(
        'Report',
        backref='disease',
        lazy='dynamic'
    )

    serialize_rules = ('-reports', '-treatments_link',)

    def __repr__(self):
        return f'<Disease {self.name}>'
