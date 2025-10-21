from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin


Base = declarative_base()

class Crop(Base, SerializerMixin):
    __tablename__ = 'crops'

    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    scientific_name = Column(String(100))
    base_region = Column(String(100))

    # Relationships
    reports = relationship('Report', backref='crop', lazy='dynamic')
    
    # Serialization Rules
    serialize_rules = ('-reports',)

    def __repr__(self):
        return f'<Crop {self.name}>'
