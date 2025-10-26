from . import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String(20))
    county = Column(String(50))
    is_extension_agent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    reports = relationship('Report', backref='user_reports', lazy='dynamic', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-reports.user', '-password_hash')

    def __repr__(self):
        return f'<User {self.username}>'
