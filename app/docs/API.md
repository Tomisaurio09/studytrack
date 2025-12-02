# 📡 API Reference

Complete API documentation for StudyTrack.

---

## Base URL
```
http://localhost:5000
```

## Authentication

Most endpoints require JWT authentication. Include the access token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

**Token Expiration:**
- Access Token: 30 minutes
- Refresh Token: 7 days

---

# 🔐 Authentication Endpoints

## Register User

Create a new user account.

**Endpoint:** `POST /auth/register`  
**Rate Limit:** 10 requests/minute  
**Auth Required:** No

### Request
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john123",
  "email": "john@example.com",
  "password": "secure1234",
  "confirm_password": "secure1234"
}
```

### Field Validation
- `username`: Alphanumeric, max 15 characters
- `email`: Valid email format
- `password`: Min 8 characters, must contain letters AND numbers
- `confirm_password`: Must match password

### Response (201 Created)
```json
{
  "message": "User created successfully"
}
```

### Error Responses
```json
// 400 - Username exists
{
  "error": "This username already exists"
}

// 400 - Validation error
{
  "errors": {
    "password": ["The password must be at least 8 characters long."]
  }
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "email": "john@example.com",
    "password": "secure1234",
    "confirm_password": "secure1234"
  }'
```

---

## Login

Authenticate and receive tokens.

**Endpoint:** `POST /auth/login`  
**Rate Limit:** 10 requests/minute  
**Auth Required:** No

### Request
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john123",
  "password": "secure1234"
}
```

### Response (200 OK)
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Error Response (401 Unauthorized)
```json
{
  "error": "Invalid username or password"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "password": "secure1234"
  }'
```

---

## Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/refresh`  
**Auth Required:** Yes (refresh token)

### Request
```http
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

### Response (200 OK)
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

# 📚 Subject Endpoints

## Create Subject

**Endpoint:** `POST /subjects`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Request
```http
POST /subjects
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Mathematics",
  "description": "Advanced calculus and linear algebra",
  "total_hours_goal": 100,
  "total_hours_completed": 0,
  "priority_level": "high",
  "status": "active"
}
```

### Field Descriptions
- `name`: Subject name (max 100 chars)
- `description`: Description (max 512 chars)
- `total_hours_goal`: Target hours (non-negative integer)
- `total_hours_completed`: Hours completed (default: 0)
- `priority_level`: `low`, `medium`, or `high`
- `status`: `active`, `completed`, or `archived`

### Response (201 Created)
```json
{
  "message": "Subject added successfully",
  "id": 1,
  "name": "Mathematics"
}
```

### cURL Example
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

---

## List All Subjects

Get paginated list of your subjects (cached for 5 minutes).

**Endpoint:** `GET /subjects`  
**Rate Limit:** 100 requests/minute  
**Auth Required:** Yes  
**Cached:** Yes (5 minutes)

### Request
```http
GET /subjects?page=1&per_page=10
Authorization: Bearer <access_token>
```

### Query Parameters
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 50)

### Response (200 OK)
```json
{
  "subjects": [
    {
      "id": 1,
      "name": "Mathematics",
      "description": "Advanced calculus",
      "total_hours_goal": 100,
      "total_hours_completed": 25,
      "priority_level": "high",
      "status": "active",
      "created_at": "2025-01-15T10:30:00",
      "updated_at": "2025-01-20T14:45:00"
    }
  ],
  "total": 15,
  "page": 1,
  "pages": 2
}
```

### cURL Example
```bash
curl -X GET "http://localhost:5000/subjects?page=1&per_page=10" \
  -H "Authorization: Bearer <access_token>"
```

---

## Get Single Subject

Get details of a specific subject (cached for 5 minutes).

**Endpoint:** `GET /subjects/{id}`  
**Rate Limit:** 100 requests/minute  
**Auth Required:** Yes  
**Cached:** Yes (5 minutes)

### Response (200 OK)
```json
{
  "id": 1,
  "name": "Mathematics",
  "description": "Advanced calculus",
  "total_hours_goal": 100,
  "total_hours_completed": 25,
  "priority_level": "high",
  "status": "active",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-20T14:45:00"
}
```

### Error Response (404 Not Found)
```json
{
  "error": "Subject not found"
}
```

### cURL Example
```bash
curl -X GET http://localhost:5000/subjects/1 \
  -H "Authorization: Bearer <access_token>"
```

---

## Update Subject

Update an existing subject (owner only).

**Endpoint:** `PUT /subjects/{id}`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Request
```http
PUT /subjects/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Advanced Mathematics",
  "description": "Updated description",
  "total_hours_goal": 120,
  "total_hours_completed": 30,
  "priority_level": "high",
  "status": "active"
}
```

### Response (200 OK)
```json
{
  "message": "Subject updated successfully"
}
```

### Error Response (404 Not Found)
```json
{
  "error": "Subject not found or unauthorized"
}
```

### cURL Example
```bash
curl -X PUT http://localhost:5000/subjects/1 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced Mathematics",
    "description": "Updated description",
    "total_hours_goal": 120,
    "total_hours_completed": 30,
    "priority_level": "high",
    "status": "active"
  }'
```

---

## Delete Subject

Delete a subject and all its study sessions.

**Endpoint:** `DELETE /subjects/{id}`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Response (200 OK)
```json
{
  "message": "Subject deleted successfully"
}
```

### Error Response (404 Not Found)
```json
{
  "error": "Subject not found or unauthorized"
}
```

### cURL Example
```bash
curl -X DELETE http://localhost:5000/subjects/1 \
  -H "Authorization: Bearer <access_token>"
```

---

# ⏱️ Study Session Endpoints

## Create Study Session

**Endpoint:** `POST /sessions`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Request
```http
POST /sessions
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "subject_id": 1,
  "start_time": "14:00",
  "end_time": "16:30",
  "notes": "Studied chapters 5-7 on derivatives"
}
```

### Field Descriptions
- `subject_id`: ID of subject (must belong to you)
- `start_time`: Session start (12h: `03:30PM` or 24h: `15:30`)
- `end_time`: Session end (must be after start_time)
- `notes`: Study notes (optional, max 2048 chars)

### Response (201 Created)
```json
{
  "message": "Session added successfully",
  "id": 1,
  "subject_id": 1
}
```

### Error Response (403 Forbidden)
```json
{
  "error": "Subject not found or unauthorized"
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/sessions \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": 1,
    "start_time": "14:00",
    "end_time": "16:30",
    "notes": "Studied derivatives"
  }'
```

---

## List All Sessions

Get paginated list of your study sessions (cached for 5 minutes).

**Endpoint:** `GET /sessions`  
**Rate Limit:** 100 requests/minute  
**Auth Required:** Yes  
**Cached:** Yes (5 minutes)

### Request
```http
GET /sessions?page=1&per_page=10
Authorization: Bearer <access_token>
```

### Response (200 OK)
```json
{
  "sessions": [
    {
      "session_id": 1,
      "subject_id": 1,
      "subject_name": "Mathematics",
      "start_time": "2025-01-20T14:00:00",
      "end_time": "2025-01-20T16:30:00",
      "duration_minutes": 150,
      "notes": "Studied derivatives"
    }
  ],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

### cURL Example
```bash
curl -X GET "http://localhost:5000/sessions?page=1&per_page=10" \
  -H "Authorization: Bearer <access_token>"
```

---

## Get Single Session

Get details of a specific study session (cached for 5 minutes).

**Endpoint:** `GET /sessions/{id}`  
**Rate Limit:** 100 requests/minute  
**Auth Required:** Yes  
**Cached:** Yes (5 minutes)

### Response (200 OK)
```json
{
  "session_id": 1,
  "subject_id": 1,
  "subject_name": "Mathematics",
  "start_time": "2025-01-20T14:00:00",
  "end_time": "2025-01-20T16:30:00",
  "duration_minutes": 150,
  "notes": "Studied chapters 5-7"
}
```

### cURL Example
```bash
curl -X GET http://localhost:5000/sessions/1 \
  -H "Authorization: Bearer <access_token>"
```

---

## Update Session

Update an existing study session (owner only).

**Endpoint:** `PUT /sessions/{id}`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Request
```http
PUT /sessions/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "subject_id": 1,
  "start_time": "15:00",
  "end_time": "17:00",
  "notes": "Updated study notes"
}
```

### Response (200 OK)
```json
{
  "message": "Session updated successfully"
}
```

### cURL Example
```bash
curl -X PUT http://localhost:5000/sessions/1 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": 1,
    "start_time": "15:00",
    "end_time": "17:00",
    "notes": "Updated notes"
  }'
```

---

## Delete Session

Delete a study session.

**Endpoint:** `DELETE /sessions/{id}`  
**Rate Limit:** 20 requests/minute  
**Auth Required:** Yes

### Response (200 OK)
```json
{
  "message": "Session deleted"
}
```

### cURL Example
```bash
curl -X DELETE http://localhost:5000/sessions/1 \
  -H "Authorization: Bearer <access_token>"
```

---

# 📊 Reference

## Enums

**Priority Levels:** `low`, `medium`, `high`  
**Subject Status:** `active`, `completed`, `archived`

## Rate Limits

| Endpoint Type | Rate Limit |
|--------------|------------|
| Authentication | 10 requests/minute |
| Read (GET) | 100 requests/minute |
| Write (POST/PUT/DELETE) | 20 requests/minute |

**429 Response:**
```json
{
  "error": "Too Many Requests"
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Validation error |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Not resource owner |
| 404 | Not Found |
| 429 | Too Many Requests - Rate limit |
| 500 | Internal Server Error |

## Caching

GET endpoints are cached with Redis:
- **Duration:** 5 minutes
- **Invalidation:** Automatic on POST/PUT/DELETE

---

**Last Updated:** December 2025  
**API Version:** 1.0.0