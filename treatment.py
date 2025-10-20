from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

# Define the base
Base = declarative_base()

class Treatment(Base, SerializerMixin):
    __tablename__ = 'treatments'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    organic_status = Column(Boolean, default=False)  # True for organic, False for chemical/other
    cost_estimate = Column(String(50))

    # Relationships
    # diseases_link points back to the association table
    diseases_link = relationship(
        'DiseaseTreatment',
        back_populates='treatment',
        cascade='all, delete-orphan'
    )

    # Serialization Rules
    serialize_rules = ('-diseases_link',)

    def __repr__(self):
        return f'<Treatment {self.name}>'
