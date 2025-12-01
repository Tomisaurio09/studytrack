Perfecto, te armo una versión **reducida y ejecutiva** del README que funciona como portada rápida. Mantiene lo esencial y deja espacio para que la documentación extendida viva en `/docs` o en Swagger. Aquí va:

---

# 📚 StudyTrack API

A RESTful API for tracking study sessions and managing subjects, built with Flask and modern Python best practices.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features
- JWT-based authentication (access & refresh tokens)  
- Subject CRUD with goals, priorities, and status  
- Study session tracking with notes and duration  
- Redis caching & rate limiting  
- Pagination & input validation (Marshmallow)  
- Secure practices: password hashing, sanitization, user isolation  

## 🛠️ Tech Stack
- **Core:** Python 3.10+, Flask 3.1.2, SQLAlchemy 2.0, PostgreSQL/SQLite  
- **Security:** Flask-JWT-Extended, Werkzeug, Bleach  
- **Performance:** Redis, Flask-Caching, DB indexing  
- **Docs & Validation:** Flask-Smorest, Marshmallow  
- **Other:** Flask-Migrate, Flask-Limiter, Pytest  

## 📦 Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/studytrack.git
cd studytrack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env   # edit values

# Initialize DB
flask db upgrade

# Run Redis (Docker example)
docker run -d -p 6379:6379 redis:7-alpine

# Start app
python run.py
```

API available at: `http://localhost:5000`

## ⚙️ Configuration
`.env` example:
```env
FLASK_ENV=development
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
DEV_DATABASE_URL=sqlite:///dev.db
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 📖 Documentation
Full API reference (endpoints, payloads, responses) available in:  
- `/docs/api.md`  
- Swagger UI at `/swagger`  

## 🧪 Testing
```bash
pytest
pytest --cov=app tests/
```

## 🚀 Deployment
- **Render**: connect repo, set env vars, run with `gunicorn run:app`  
- **Docker**: `docker build -t studytrack-api . && docker run -p 5000:5000 --env-file .env studytrack-api`

## 🤝 Contributing
1. Fork repo  
2. Create branch (`feature/...`)  
3. Commit & push  
4. Open PR  

## 📝 License
MIT License – see [LICENSE](LICENSE)

---
