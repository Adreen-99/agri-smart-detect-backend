from app import db
from models import Crop


crops = [
    Crop(name='Maize', disease='Leaf blight'),
    Crop(name='Tomato', disease='Early blight'),
    Crop(name='Wheat', disease='Rust')
]

# Push data
with db.session.begin():
    db.session.add_all(crops)

print("✅ Database seeded successfully!")
