#  Agri-Smart Detect Backend

### Empowering Farmers with AI-Powered Crop Disease Detection

---

**Agri-Smart Detect** solves this by letting farmers upload a photo of a sick plant to instantly get an AI-powered diagnosis and treatment recommendation — all in one simple web app.

---

##  How Agri-Smart Detect Works

1. Farmers take or upload a picture of the affected crop leaf.  
2. The system uses an AI model to detect the disease, shows the confidence level, and provides localized treatment tips (both organic and chemical options).  
3. Each diagnosis is saved so the farmer can track history and progress.

---

##  Tech Stack

**Backend:** Python · Flask · SQLAlchemy  
**Database:** PostgreSQL  
**AI Integration:** TensorFlow / PyTorch (for image classification)  
**Other Tools:**  
- Marshmallow (serialization & validation)  
- Flask-Migrate (database migrations)  
- Flask-CORS (API access)  
- dotenv (environment management)

---

##  Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Adreen-99/agri-smart-detect-backend.git
cd agri-smart-detect-backend
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/agri_smart_detect
SECRET_KEY=<your_secret_key>
```

### 5. Run Database Migrations
```bash
flask db upgrade
```

### 6. Start the Server
```bash
flask run
```
 
---


##  Project Structure

```
agri-smart-detect-backend/
├── app.py
├── models/
│   ├── __init__.py
│   └── ...
├── routes/
│   ├── detect_routes.py
│   ├── auth_routes.py
│   └── ...
├── migrations/
├── static/
├── templates/
└── requirements.txt
```

---

##  Contributing

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/your-feature`)  
3. Commit your changes (`git commit -m "Add feature"`)  
4. Push to the branch (`git push origin feature/your-feature`)  
5. Open a Pull Request

---

###  Licence 
MIT License

Copyright (c) 2025 Adreen Nyawira G.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

