import os
import random

class DiseaseModel:
    def __init__(self):
        self.model = None
        self.labels = ['Healthy', 'Leaf Rust', 'Powdery Mildew', 'Blight', 'Leaf Spot']
    
    def load_model(self, model_path):
        """Mock model loading - replace with actual model"""
        print(f"Loading model from {model_path}")
        return True
    
    def predict(self, image_path):
        """Mock prediction - replace with actual ML model"""
        # This matches the frontend mock data structure
        diseases = [
            {'disease': 'Leaf Rust', 'confidence': 0.87, 'isHealthy': False},
            {'disease': 'Powdery Mildew', 'confidence': 0.72, 'isHealthy': False},
            {'disease': 'Blight', 'confidence': 0.78, 'isHealthy': False},
            {'disease': 'Healthy', 'confidence': 0.95, 'isHealthy': True}
        ]
        
        return random.choice(diseases)

# Global model instance
disease_model = DiseaseModel()