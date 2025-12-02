# 🏗️ Architecture Guide

System design, database schema, and architectural decisions for StudyTrack API.

---

## 🎯 System Overview

StudyTrack is a RESTful API built with a layered architecture pattern:

```
┌─────────────────────────────────────────┐
│          Client Applications            │
│    (Web, Mobile, CLI, Postman, etc.)   │
└─────────────────┬───────────────────────┘
                  │ HTTP/JSON
                  │
┌─────────────────▼───────────────────────┐
│         Flask Application Layer         │
│  ┌────────────────────────────────────┐ │
│  │     Rate Limiting (Flask-Limiter)  │ │
│  └────────────┬───────────────────────┘ │
│               │                          │
│  ┌────────────▼───────────────────────┐ │
│  │     JWT Authentication Layer       │ │
│  └────────────┬───────────────────────┘ │
│               │                          │
│  ┌────────────▼───────────────────────┐ │
│  │    Input Validation (Marshmallow)  │ │
│  └────────────┬───────────────────────┘ │
│               │                          │
│  ┌────────────▼───────────────────────┐ │
│  │      Business Logic (Routes)       │ │
│  └────────────┬───────────────────────┘ │
└───────────────┼─────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼──────┐  ┌─────▼──────┐
│    Redis     │  │  Database  │
│  (Caching)   │  │ (SQLite/   │
│              │  │ PostgreSQL)│
└──────────────┘  └────────────┘
```

### Key Characteristics

- **Stateless**: Each request is independent, JWT handles authentication
- **Cacheable**: Redis caching for frequently accessed data
- **Layered**: Clear separation between routes, models, schemas, and utilities
- **Secure**: Multiple security layers (authentication, authorization, rate limiting, input sanitization)

---

## 🛠️ Technology Stack

### Core Framework
- **Flask 3.1.2** - Lightweight WSGI web framework
- **Python 3.10+** - Modern Python with type hints

### Database & ORM
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **Alembic** - Database migrations
- **PostgreSQL** (production) / **SQLite** (development)

### Authentication & Security
- **Flask-JWT-Extended** - JWT token management
- **Werkzeug** - Password hashing (bcrypt)
- **Bleach** - HTML/XSS sanitization
- **Flask-Limiter** - Rate limiting

### Performance
- **Redis** - In-memory caching
- **Flask-Caching** - Caching integration

### API & Validation
- **Flask-Smorest** - REST API framework with OpenAPI
- **Marshmallow** - Object serialization and validation

### Testing
- **Pytest** - Unit and integration testing
- **Locust** - Load testing

### Development Tools
- **Flask-Migrate** - Database migrations
- **python-dotenv** - Environment variable management

---

## 📁 Project Structure

```
studytrack/
├── app/
│   ├── __init__.py           # App factory, extensions initialization
│   ├── config.py             # Configuration classes (Dev/Test/Prod)
│   ├── models.py             # SQLAlchemy models
│   │
│   ├── routes/               # API endpoints
│   │   ├── auth_routes.py    # Authentication endpoints
│   │   ├── subject_routes.py # Subject CRUD
│   │   └── study_sessions_routes.py  # Session CRUD
│   │
│   ├── schemas/              # Marshmallow validation schemas
│   │   ├── user_schema.py    # User registration/login
│   │   ├── subject_schema.py # Subject validation
│   │   └── study_sessions_schema.py  # Session validation
│   │
│   └── utils/                # Utility modules
│       ├── cache_utils.py    # Cache key generation, invalidation
│       ├── error_handler.py  # Global error handlers
│       └── limiters.py       # Rate limiter configuration
│
├── tests/                    # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_subjects.py     # Subject endpoint tests
│   ├── test_sessions.py     # Session endpoint tests
│   ├── test_models.py       # Model tests
│   ├── test_password_utils.py  # Security tests
│   ├── test_tokens.py       # JWT tests
│   │
│   └── load/                # Load testing
│       └── locustfile.py    # Locust scenarios
│
├── migrations/              # Alembic database migrations
│   ├── versions/            # Migration scripts
│   └── alembic.ini         # Alembic configuration
│
├── docs/                    # Documentation
│   ├── README.md           # Documentation index
│   ├── API.md              # API reference
│   ├── ARCHITECTURE.md     # This file
│   └── TESTING.md          # Testing guide
│
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── README.md               # Project overview
```

### Module Responsibilities

**`app/__init__.py`**: 
- Application factory pattern
- Extension initialization (DB, cache, JWT, etc.)
- Blueprint registration

**`app/models.py`**: 
- Database models (User, Subject, StudySession)
- Relationships and constraints
- Business logic (password hashing)

**`app/routes/`**: 
- HTTP endpoint handlers
- Request validation
- Response formatting
- Authorization checks

**`app/schemas/`**: 
- Input validation
- Data serialization
- Error messages

**`app/utils/`**: 
- Shared utilities
- Cache management
- Error handling

---

### Relationships

**User → Subject**: One-to-Many (Cascade Delete)
- One user can have multiple subjects
- Deleting a user deletes all their subjects

**Subject → StudySession**: One-to-Many (Cascade Delete)
- One subject can have multiple study sessions
- Deleting a subject deletes all its sessions

---

### Token Expiration

**Access Token**: 30 minutes
- Used for all API requests
- Short-lived for security

**Refresh Token**: 7 days
- Used only to get new access tokens
- Longer-lived for better UX

---

### Cached Endpoints

| Endpoint | TTL | Cache Key Pattern |
|----------|-----|-------------------|
| GET /subjects (list) | 5 min | `user:{id}:subjects:page:{p}:per_page:{pp}` |
| GET /subjects/{id} | 5 min | `user:{id}:subject:{subject_id}` |
| GET /sessions (list) | 5 min | `user:{id}:sessions:page:{p}:per_page:{pp}` |
| GET /sessions/{id} | 5 min | `user:{id}:session:{session_id}` |

### Cache Invalidation

**Automatic invalidation on:**
- POST /subjects → Invalidate subjects list cache
- PUT /subjects/{id} → Invalidate subjects list + single subject cache
- DELETE /subjects/{id} → Invalidate subjects list + single subject cache
- POST /sessions → Invalidate sessions list cache
- PUT /sessions/{id} → Invalidate sessions list + single session cache
- DELETE /sessions/{id} → Invalidate sessions list + single session cache

**Strategy**: Aggressive invalidation
- Better to invalidate too much than serve stale data
- 5-minute TTL balances performance vs. freshness
---

## 🔒 Security Measures

### 1. Password Security
- **Hashing**: Werkzeug's `generate_password_hash` (bcrypt)
- **No plaintext**: Passwords never stored in plain text
- **Complexity**: Minimum 8 chars, must contain letters AND numbers

### 2. JWT Security
- **HS256 algorithm**: Industry standard symmetric signing
- **Short expiration**: Access tokens expire after 30 minutes
- **Refresh tokens**: 7-day expiration, only for token refresh
- **Secret rotation**: Environment-based secrets

### 3. Input Sanitization
- **Bleach library**: Strips HTML/XSS from all text inputs
- **Marshmallow validation**: Type checking and format validation
- **Pre-load hooks**: Sanitize before validation

### 4. Rate Limiting
- **Per-IP limiting**: Prevents brute force attacks
- **Different tiers**:
  - Auth: 10/minute (prevent credential stuffing)
  - Reads: 100/minute (generous for normal use)
  - Writes: 20/minute (prevent spam)

### 5. Authorization
- **User isolation**: Users can only access their own data
- **JWT-based**: Every protected endpoint checks JWT
- **Ownership verification**: Additional checks for update/delete

### 6. SQL Injection Prevention
- **ORM usage**: SQLAlchemy parameterizes queries
- **No raw SQL**: Avoid string concatenation in queries

### 7. Error Handling
- **No sensitive data leaks**: Generic error messages
- **Logging**: Detailed errors logged server-side only
- **Status codes**: Proper HTTP status codes

