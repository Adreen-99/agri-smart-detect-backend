# Agri Smart Detect Backend

AI-powered crop disease detection API for African farmers. This Flask-based REST API enables farmers to upload crop images and receive instant disease analysis, treatment recommendations, and prevention tips.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **AI-Powered Disease Detection**: Integrates with Plant.id API for accurate crop disease identification
- **User Authentication**: Secure JWT-based authentication system
- **Email Notifications**: Automated email reports using Resend
- **Disease Database**: Comprehensive database of common African crop diseases
- **Treatment Recommendations**: Personalized treatment plans and prevention tips
- **Report History**: Track and manage scan history for each user
- **RESTful API**: Clean, well-documented API endpoints
- **PostgreSQL Database**: Robust data persistence with SQLAlchemy ORM
- **CORS Support**: Configured for frontend integration

## Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: PostgreSQL (Production), SQLite (Development)
- **ORM**: SQLAlchemy 2.0.44
- **Authentication**: Flask-JWT-Extended
- **Email Service**: Resend
- **Image Processing**: Plant.id API
- **Server**: Gunicorn
- **Python Version**: 3.13.4

## Prerequisites

- Python 3.11+ (3.13.4 recommended)
- PostgreSQL (for production)
- Resend API key (for email functionality)
- Plant.id API key (for disease detection)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agri-smart-detect-backend.git
cd agri-smart-detect-backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=sqlite:///instance/app.db  # For development

# Email Configuration (Resend)
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@yourdomain.com

# Plant.id API Configuration
PLANT_ID_API_KEY=your-plant-id-api-key

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### 5. Initialize Database

```bash
python run.py
```

This will create the database tables and populate sample crop data.

## Configuration

### Environment-Based Configuration

The application uses three configuration classes:

- **DevelopmentConfig**: SQLite database, debug mode enabled
- **ProductionConfig**: PostgreSQL database, security features enabled
- **TestingConfig**: In-memory SQLite, testing mode

Configuration is automatically selected based on the `FLASK_ENV` environment variable.

### API Keys

#### Resend (Email Service)

1. Sign up at [resend.com](https://resend.com)
2. Create an API key
3. Verify your domain or use the test domain
4. Add to `.env`: `RESEND_API_KEY=re_xxxxx`

#### Plant.id (Disease Detection)

1. Sign up at [plant.id](https://web.plant.id)
2. Get your API key from the dashboard
3. Add to `.env`: `PLANT_ID_API_KEY=your-key-here`

## Running the Application

### Development Mode

```bash
# Using Flask development server
python run.py
```

The API will be available at `http://localhost:5000`

### Production Mode

```bash
# Using Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 'app:create_app()'
```

Or use the provided script:

```bash
./start_server.sh
```

## API Documentation

### Base URL

- Development: `http://localhost:5000`
- Production: `https://your-domain.onrender.com`

### Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Health Check

```http
GET /
GET /health
```

Returns API status and database connectivity.

#### Authentication

**Register User**
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Get Profile**
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

**Update Profile**
```http
PUT /api/auth/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Updated"
}
```

#### Disease Diagnosis

**Scan Crop Image**
```http
POST /api/diagnosis/scan
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>
```

**Get Diseases List**
```http
GET /api/diagnosis/diseases
```

**Health Check (Plant.id API)**
```http
GET /api/diagnosis/health
```

#### Reports

**Get User Reports**
```http
GET /api/reports?page=1&per_page=10&is_healthy=false
Authorization: Bearer <token>
```

**Get Specific Report**
```http
GET /api/reports/<report_id>
Authorization: Bearer <token>
```

**Get Statistics**
```http
GET /api/reports/stats
Authorization: Bearer <token>
```

### Response Format

#### Success Response
```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

#### Error Response
```json
{
  "error": "Error message",
  "details": "Additional error details"
}
```

## Deployment

### Render Deployment

This application is configured for deployment on Render using the `render.yaml` blueprint.

#### Prerequisites

1. GitHub repository
2. Render account
3. Resend API key
4. Plant.id API key

#### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically:
     - Create PostgreSQL database
     - Deploy web service
     - Link database to web service

3. **Configure Environment Variables**
   
   In Render Dashboard, add these manually:
   - `RESEND_API_KEY`: Your Resend API key
   - `PLANT_ID_API_KEY`: Your Plant.id API key
   
   Auto-generated by Render:
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `DATABASE_URL`

4. **Verify Deployment**
   ```bash
   curl https://your-service.onrender.com/health
   ```

#### Deployment Configuration

The `render.yaml` file defines:
- Python 3.13.4 runtime
- PostgreSQL database (free tier)
- Environment variables
- Build and start commands

See [DEPLOYMENT_FIXES.md](DEPLOYMENT_FIXES.md) for detailed deployment troubleshooting.

### Alternative Deployment (Railway, Heroku)

The application includes configuration files for:
- **Railway**: `railway.json`, `nixpacks.toml`
- **Heroku**: `Procfile`, `runtime.txt`

## Project Structure

```
agri-smart-detect-backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models/               # Database models
│   │   ├── user.py
│   │   ├── crop.py
│   │   ├── disease.py
│   │   ├── treatment.py
│   │   └── report.py
│   ├── routes/               # API endpoints
│   │   ├── auth.py
│   │   ├── diagnosis.py
│   │   └── reports.py
│   ├── services/             # Business logic
│   │   ├── email_service.py
│   │   └── plant_id_service.py
│   └── utils/                # Utility functions
├── instance/                 # SQLite database (development)
├── uploads/                  # Uploaded images
├── config.py                 # Configuration classes
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── render.yaml               # Render deployment config
├── Procfile                  # Heroku/Render process file
├── runtime.txt               # Python version specification
└── README.md                 # This file
```

## Database Schema

### Users
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `created_at`: Registration timestamp

### Crops
- `id`: Primary key
- `name`: Crop name (e.g., Maize, Cassava)
- `scientific_name`: Scientific name
- `common_names`: Comma-separated common names

### Diseases
- `id`: Primary key
- `name`: Disease name
- `description`: Disease description
- `symptoms`: Disease symptoms
- `crop_id`: Foreign key to crops

### Reports
- `id`: Primary key
- `user_id`: Foreign key to users
- `crop_name`: Identified crop
- `disease_id`: Foreign key to diseases (nullable)
- `confidence`: AI confidence score (0-1)
- `is_healthy`: Boolean health status
- `image_path`: Path to uploaded image
- `recommended_treatment`: Treatment recommendations
- `prevention_tips`: Prevention advice
- `created_at`: Scan timestamp

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Code Style

The project follows PEP 8 style guidelines. Format code using:

```bash
pip install black flake8
black .
flake8 .
```

### Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## Troubleshooting

### Common Issues

**1. Module Not Found Errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Database Connection Errors**
```bash
# Check DATABASE_URL is set correctly
echo $DATABASE_URL

# For PostgreSQL, ensure format is: postgresql://user:pass@host:port/dbname
```

**3. Email Not Sending**
- Verify `RESEND_API_KEY` is set
- Check `RESEND_FROM_EMAIL` is verified in Resend dashboard
- Review application logs for error messages

**4. Plant.id API Errors**
- Verify `PLANT_ID_API_KEY` is valid
- Check API quota hasn't been exceeded
- Application falls back to mock data if API fails

### Debug Mode

Enable debug logging:

```python
# In run.py or config
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### Recommended Production Settings

- **Workers**: 2-4 Gunicorn workers (based on CPU cores)
- **Timeout**: 120 seconds (for image processing)
- **Database**: Connection pooling enabled
- **Caching**: Consider Redis for session storage

### Scaling Considerations

- Use CDN for uploaded images
- Implement rate limiting on upload endpoints
- Add database read replicas for high traffic
- Consider background job queue (Celery) for email sending

## Security

### Best Practices Implemented

- Password hashing with Bcrypt
- JWT token-based authentication
- CORS configuration for frontend
- Environment-based secrets
- SQL injection protection (SQLAlchemy ORM)
- File upload validation
- HTTPS enforcement in production

### Security Checklist

- [ ] Rotate `SECRET_KEY` and `JWT_SECRET_KEY` regularly
- [ ] Keep dependencies updated
- [ ] Monitor API usage and rate limits
- [ ] Regular database backups
- [ ] Review and update CORS origins
- [ ] Implement request rate limiting

## API Rate Limits

Current limits (can be configured):
- Authentication: 5 requests/minute
- Image upload: 10 requests/hour per user
- General API: 100 requests/hour per user

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/agri-smart-detect-backend/issues)
- Email: support@agri-smart-detect.com
- Documentation: See additional docs in `/docs` folder

## Roadmap

- [ ] Add support for more crop types
- [ ] Implement real-time notifications
- [ ] Add multi-language support
- [ ] Integrate weather data for better predictions
- [ ] Mobile app API optimization
- [ ] Machine learning model training pipeline
- [ ] Admin dashboard for disease management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Plant.id for disease detection API
- Resend for email delivery service
- Flask community for excellent documentation
- Contributors and testers

## Contact

- Project Maintainer: Your Name
- Email: your.email@example.com
- Website: https://agri-smart-detect.com

---

Built with care for African farmers. Protecting harvests, one scan at a time.
