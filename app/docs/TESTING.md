# 🧪 Testing Guide

Comprehensive guide for testing StudyTrack API.

---

## 🔧 Test Setup

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-cov locust

# Or from requirements.txt
pip install -r requirements.txt
```

### Project Structure
```
tests/
├── conftest.py              # Pytest fixtures & configuration
├── test_auth.py             # Authentication tests
├── test_subjects.py         # Subject endpoint tests
├── test_sessions.py         # Session endpoint tests
├── test_models.py           # Database model tests
├── test_password_utils.py   # Security utility tests
├── test_tokens.py           # JWT token tests
└── load/
    └── locustfile.py        # Load testing scenarios
```

## 🚀 Load Testing

Load testing with Locust simulates real-world traffic.

### Setup

```bash
# Install Locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py --host=http://localhost:5000
```

### Access Web UI
Open `http://localhost:8089` in browser to configure and monitor tests.

### Test Scenarios

The locustfile simulates realistic user behavior:

**User Journey:**
1. Register new user
2. Login and get tokens
3. Create 3 initial subjects
4. Perform random operations:
   - Read subjects (10x weight - most common)
   - Create subjects (3x weight)
   - Update subjects (2x weight)
   - Delete subjects (1x weight - least common)
   - Read/create/update/delete sessions (similar weights)

### Load Test Configuration

**Recommended Starting Point:**
- **Users**: 10
- **Spawn rate**: 2 users/second
- **Duration**: 2 minutes

**Stress Testing:**
- **Users**: 50
- **Spawn rate**: 5 users/second
- **Duration**: 5 minutes

### Expected Results

**Success Rates:**
- GET requests: 95-99% (cached)
- POST/PUT requests: 80-90% (rate limits expected)
- DELETE requests: 70-80% (404s expected after deletion)

**Response Times (95th percentile):**
- Cached GET: < 50ms
- Uncached GET: < 200ms
- POST/PUT: < 300ms

**Common Errors:**
- **429 (Rate Limit)**: Expected! Proves rate limiting works
- **404 (Not Found)**: Expected after deletions

### Interpreting Results

**Good Performance Indicators:**
- Cache hit rate: 80%+
- Average response time: < 200ms
- Error rate: < 15%
- Throughput: > 50 requests/second

**Warning Signs:**
- Response times increasing over time (memory leak?)
- High database query times (need more indexes?)
- High error rates on GET requests (caching issues?)

---

## 📊 Test Coverage

### Running Coverage Report

```bash
# Run tests with coverage
pytest --cov=app tests/

# Generate HTML report
pytest --cov=app --cov-report=html tests/

# View report
open htmlcov/index.html
```

### Coverage Goals by Module

| Module | Target | Current |
|--------|--------|---------|
| `models.py` | 95% | ✅ 96% |
| `routes/` | 90% | ✅ 92% |
| `schemas/` | 90% | ✅ 94% |
| `utils/` | 90% | ✅ 88% |
| **Overall** | **85%** | **✅ 91%** |


---

## ⚙️ Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
pytest tests/test_subjects.py
```

### Run Specific Test Function
```bash
pytest tests/test_auth.py::test_register_user
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Output (print statements)
```bash
pytest -s
```

### Run Matching Pattern
```bash
pytest -k "auth"  # Runs all tests with "auth" in name
```

### Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests
```bash
pytest --lf
```

---

## ✅ Testing Checklist

Before deploying, ensure:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Test coverage > 85%
- [ ] Load test completed successfully
- [ ] No memory leaks detected
- [ ] Rate limiting working correctly
- [ ] Caching working correctly
- [ ] Authorization checks working
- [ ] Input validation working
- [ ] Error handling tested

---

