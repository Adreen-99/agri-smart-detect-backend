from app import db

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    scientific_name = db.Column(db.String(100))
    common_names = db.Column(db.Text)
    
    # Relationships
    diseases = db.relationship('Disease', backref='crop', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'common_names': self.common_names.split(',') if self.common_names else []
        }