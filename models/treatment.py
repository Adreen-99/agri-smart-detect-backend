from app import db
from sqlalchemy_serializer import SerializerMixin

class Treatment(db.Model, SerializerMixin):
    __tablename__ = 'treatments'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    organic_status = db.Column(db.Boolean, default=False)  # True for organic, False for chemical/other
    cost_estimate = db.Column(db.String(50))

    # Relationships
    diseases_link = db.relationship(
        'DiseaseTreatment',
        back_populates='treatment',
        cascade='all, delete-orphan'
    )

    # Serialization rules
    serialize_rules = ('-diseases_link',)

    def __repr__(self):
        return f'<Treatment {self.name}>'
