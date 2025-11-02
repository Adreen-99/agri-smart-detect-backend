from app import db

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    causes = db.Column(db.Text)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    
    # Relationships
    treatments = db.relationship('Treatment', backref='disease', lazy=True)
    reports = db.relationship('Report', backref='disease', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symptoms': self.symptoms,
            'causes': self.causes,
            'crop_id': self.crop_id
        }
