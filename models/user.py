from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    
    password_hash = Column(String, nullable=False) 
    phone_number = Column(String(20))
    county = Column(String(50))
    is_extension_agent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    reports = relationship('Report', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    
    serialize_rules = ('-reports.user', '-password_hash')

    def __repr__(self):
        return f'<User {self.username}>'
