# 📚 StudyTrack API

A production-ready RESTful API for tracking study sessions and managing subjects, built with Flask and modern Python best practices.

## 🚀 Features

- **JWT Authentication** - Secure token-based auth with access & refresh tokens
- **Subject Management** - Create, read, update, delete study subjects with goals & priorities
- **Study Session Tracking** - Log study sessions with duration, notes, and timestamps
- **Redis Caching** - 80-90% cache hit rate for optimal performance
- **Rate Limiting** - API protection against abuse (configurable per endpoint)
- **Pagination** - Efficient data retrieval with customizable page sizes
- **Input Validation** - Comprehensive validation with detailed error messages
- **Security** - Password hashing, input sanitization, user isolation, XSS protection
- **OpenAPI/Swagger** - Interactive API documentation built-in
- **Load Tested** - Validated for 50+ concurrent users with Locust

---

## 🛠️ Tech Stack

**Core:**
- Python 3.10+ | Flask 3.1.2 | SQLAlchemy 2.0 | PostgreSQL/SQLite

**Security:**
- Flask-JWT-Extended | Werkzeug (bcrypt) | Bleach | Flask-Limiter

**Performance:**
- Redis | Flask-Caching | Database indexing | Eager loading

**API & Validation:**
- Flask-Smorest (OpenAPI/Swagger) | Marshmallow

**Testing:**
- Pytest | Locust | 91% test coverage

---

## 📦 Quick Start

### Prerequisites
- Python 3.10 or higher
- Redis server
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/studytrack.git
cd studytrack

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your configuration

# 5. Initialize database
flask db upgrade

# 6. Start Redis
# Option A: Docker
docker run -d -p 6379:6379 redis:7-alpine

# Option B: Local installation
redis-server

# 7. Run application
python run.py
```

API available at: `http://localhost:5000`

---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DEV_DATABASE_URL=sqlite:///dev.db
# Production: postgresql://user:password@localhost:5432/studytrack

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

---

## 📖 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[API Reference](docs/API.md)** - Complete endpoint documentation with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design, database schema, design decisions
- **[Testing Guide](docs/TESTING.md)** - Unit tests, integration tests, load testing
- **[Documentation Index](docs/README.md)** - Overview and quick reference

### Interactive API Documentation

When the server is running:
- **Swagger UI**: [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)
- **OpenAPI Spec**: [http://localhost:5000/api-spec.json](http://localhost:5000/api-spec.json)

---

## 🎯 Quick Example

### 1. Register & Login
```bash
# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "email": "john@example.com",
    "password": "secure1234",
    "confirm_password": "secure1234"
  }'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "password": "secure1234"
  }'
```

### 2. Create Subject
```bash
curl -X POST http://localhost:5000/subjects \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mathematics",
    "description": "Advanced calculus",
    "total_hours_goal": 100,
    "total_hours_completed": 0,
    "priority_level": "high",
    "status": "active"
  }'
```

### 3. Track Study Session
```bash
curl -X POST http://localhost:5000/sessions \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": 1,
    "start_time": "14:00",
    "end_time": "16:00",
    "notes": "Studied derivatives and integrals"
  }'
```

More examples in [docs/API.md](docs/API.md)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html

# Run load tests
locust -f tests/load/locustfile.py --host=http://localhost:5000
# Open http://localhost:8089 for web UI
```

See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing guide.

---

## 📈 Roadmap

**Current Version: 1.0.0**

**Planned Features:**
- [ ] User profiles with avatar upload
- [ ] Study statistics and analytics dashboard
- [ ] Export study data (CSV, PDF)
- [ ] Email notifications for goals
- [ ] Study streak tracking
- [ ] Social features (study groups)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Before submitting:**
- Run tests: `pytest`
- Check coverage: `pytest --cov=app`
- Follow PEP 8 style guide
- Update documentation if needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---
