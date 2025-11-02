from app import db

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    treatment_steps = db.Column(db.Text, nullable=False)
    prevention_tips = db.Column(db.Text)
    organic_remedies = db.Column(db.Text)
    chemical_treatments = db.Column(db.Text)
    urgency_level = db.Column(db.String(20), default='medium')

    def to_dict(self):
        return {
            'id': self.id,
            'disease_id': self.disease_id,
            'treatment_steps': self.treatment_steps,
            'prevention_tips': self.prevention_tips,
            'organic_remedies': self.organic_remedies,
            'chemical_treatments': self.chemical_treatments,
            'urgency_level': self.urgency_level
        }