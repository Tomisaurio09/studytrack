# 📖 StudyTrack API Documentation

Welcome to the comprehensive documentation for StudyTrack API - a production-ready REST API for tracking study sessions and managing subjects.

## 📑 Documentation Index

### Core Documentation
- **[API Reference](API.md)** - Complete endpoint documentation with examples
- **[Architecture Guide](ARCHITECTURE.md)** - System design, database schema, and design decisions
- **[Testing Guide](TESTING.md)** - Unit testing, integration testing, and load testing

### Additional Resources
- **[Main README](../README.md)** - Quick start and installation guide
- **[Swagger UI](http://localhost:5000/swagger-ui)** - Interactive API documentation (when server is running)
- **[OpenAPI Spec](http://localhost:5000/api-spec.json)** - Machine-readable API specification

---

## 🎯 Quick Reference

### Base URL
```
http://localhost:5000
```

### Authentication
All protected endpoints require JWT authentication:
```bash
Authorization: Bearer <access_token>
```

### Rate Limits
| Endpoint Type | Rate Limit |
|--------------|------------|
| Auth (register/login) | 10 requests/minute |
| Read operations (GET) | 100 requests/minute |
| Write operations (POST/PUT/DELETE) | 20 requests/minute |

### Pagination
All list endpoints support pagination:
```bash
GET /subjects?page=1&per_page=10
GET /sessions?page=2&per_page=20
```

### Caching
GET endpoints are cached with Redis:
- **Cache Duration**: 5 minutes
- **Invalidation**: Automatic on POST/PUT/DELETE
- **Cache Hit Rate**: 80-90% in production

---

## 🚀 Common Workflows

### 1. Authentication Flow
```bash
# Register
POST /auth/register

# Login
POST /auth/login
# Returns: access_token, refresh_token

# Refresh token when expired
POST /auth/refresh
# Headers: Authorization: Bearer <refresh_token>
```

### 2. Subject Management
```bash
# Create subject
POST /subjects

# List all subjects (cached)
GET /subjects?page=1&per_page=10

# Get single subject (cached)
GET /subjects/{id}

# Update subject
PUT /subjects/{id}

# Delete subject
DELETE /subjects/{id}
```

### 3. Study Session Tracking
```bash
# Create study session
POST /sessions

# List all sessions (cached)
GET /sessions?page=1&per_page=10

# Get single session (cached)
GET /sessions/{id}

# Update session
PUT /sessions/{id}

# Delete session
DELETE /sessions/{id}
```

---

## 📊 Data Models

### Enums
**Priority Levels**: `low`, `medium`, `high`  
**Subject Status**: `active`, `completed`, `archived`

### Relationships
```
User (1) ────< (N) Subject (1) ────< (N) StudySession
```

---

## 🐛 Troubleshooting

### Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Request completed successfully |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request payload format |
| 401 | Unauthorized | Invalid or expired token |
| 403 | Forbidden | You don't own this resource |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Wait 60 seconds, you hit rate limit |
| 500 | Internal Server Error | Check server logs |

### Debug Checklist

1. **401 Unauthorized**
   - Check if token is valid
   - Token might be expired (expires after 30 minutes)
   - Use refresh token endpoint

2. **404 Not Found**
   - Verify the resource ID exists
   - Check if resource belongs to your user
   - Confirm endpoint URL is correct

3. **429 Rate Limit**
   - Wait 60 seconds before retrying
   - Implement exponential backoff
   - Consider caching on client side

4. **500 Internal Error**
   - Check `app.log` for details
   - Verify database connection
   - Ensure Redis is running

---

## 🔧 Development Tools

### Postman Collection
Import the OpenAPI spec into Postman:
```
http://localhost:5000/api-spec.json
```

### cURL Examples
See [API.md](API.md) for comprehensive cURL examples for all endpoints.

### Python Client Example
```python
import requests

# Login
response = requests.post("http://localhost:5000/auth/login", json={
    "username": "john123",
    "password": "secure1234"
})
token = response.json()["access_token"]

# Create subject
headers = {"Authorization": f"Bearer {token}"}
response = requests.post("http://localhost:5000/subjects", 
    json={
        "name": "Mathematics",
        "description": "Advanced calculus",
        "total_hours_goal": 100,
        "total_hours_completed": 0,
        "priority_level": "high",
        "status": "active"
    },
    headers=headers
)
```

---

## 📈 Performance Tips

1. **Use Pagination**: Always paginate large lists
2. **Leverage Caching**: GET endpoints are cached for 5 minutes
3. **Batch Operations**: Group multiple updates when possible
4. **Respect Rate Limits**: Implement client-side throttling
5. **Use Compression**: Enable gzip compression on client

---

## 🔗 External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [JWT.io](https://jwt.io/) - JWT debugging tool
- [Postman](https://www.postman.com/) - API testing tool
- [Redis Documentation](https://redis.io/docs/)

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/studytrack/issues)
- **Email**: your.email@example.com
- **Documentation**: You're reading it! 📚

---

**Last Updated**: December 2025  
**API Version**: 1.0.0  
**Maintained by**: Your Name