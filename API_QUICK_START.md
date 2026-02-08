# PRATIK API - Quick Start Guide

**Version:** 1.0  
**Date:** February 8, 2026

---

## Table of Contents
1. [Authentication](#authentication)
2. [API Endpoints](#api-endpoints)
3. [Common Use Cases](#common-use-cases)
4. [Error Handling](#error-handling)
5. [Rate Limits](#rate-limits)

---

## Authentication

### Obtain JWT Token
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "your-email@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token in Requests
```bash
GET /api/evolution/tracked/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refresh Token
```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## API Endpoints

### Recommendations

#### Create Recommendation (Company Only)
```bash
POST /api/recommendations/create/
Authorization: Bearer <company_token>
Content-Type: application/json

{
  "student": 1,
  "internship": 1,
  "rating": 5,
  "autonomy": 5,
  "teamwork": 4,
  "rigor": 5,
  "creativity": 4,
  "punctuality": 5,
  "comment": "Excellent intern!",
  "skills_validated": ["Python", "Django", "REST API"],
  "recommended_domains": ["Web Development", "Backend"],
  "is_public": true,
  "is_featured": false
}
```

#### Get Student Recommendations
```bash
GET /api/recommendations/student/{student_id}/
```

**Query Parameters:**
- `ordering`: `-created_at`, `rating`, `-rating`

#### List Recommended Students
```bash
GET /api/recommendations/students/
```

**Query Parameters:**
- `min_rating`: Filter by minimum rating (1-5)
- `is_featured`: Filter featured recommendations (true/false)
- `search`: Search in student name, skills, domains
- `ordering`: `rating`, `-rating`, `created_at`, `-created_at`

---

### Evolution Tracking

#### Start Tracking Student (Company Only)
```bash
POST /api/evolution/start/
Authorization: Bearer <company_token>
Content-Type: application/json

{
  "student_id": 1,
  "current_level": "BEGINNER",
  "domain": "Web Development",
  "status": "AVAILABLE"
}
```

**Levels:** `BEGINNER`, `INTERMEDIATE`, `ADVANCED`, `EXPERT`  
**Status:** `AVAILABLE`, `IN_INTERNSHIP`, `EMPLOYED`, `UNAVAILABLE`

#### List Tracked Students (Company Only)
```bash
GET /api/evolution/tracked/
Authorization: Bearer <company_token>
```

**Query Parameters:**
- `current_level`: Filter by level
- `status`: Filter by status
- `search`: Search in student name, domain
- `ordering`: `updated_at`, `-updated_at`, `current_level`

#### Update Student Evolution (Company Only)
```bash
PATCH /api/evolution/update/{tracking_id}/
Authorization: Bearer <company_token>
Content-Type: application/json

{
  "current_level": "INTERMEDIATE",
  "domain": "Full Stack Development",
  "status": "IN_INTERNSHIP"
}
```

---

### Internship Calendars

#### Create Calendar (School Only)
```bash
POST /api/calendars/create/
Authorization: Bearer <school_token>
Content-Type: application/json

{
  "program_manager": 1,
  "program_name": "Computer Science Internship",
  "program_level": "BACHELOR",
  "number_of_students": 25,
  "start_date": "2026-06-01",
  "end_date": "2026-08-31",
  "skills_sought": ["Python", "JavaScript", "SQL"],
  "description": "Summer internship program for CS students",
  "is_visible_to_companies": true
}
```

**Program Levels:** `BACHELOR`, `MASTER`, `DOCTORATE`, `PROFESSIONAL`

#### Publish Calendar (School Only)
```bash
POST /api/calendars/publish/{calendar_id}/
Authorization: Bearer <school_token>
```

#### List Public Calendars
```bash
GET /api/calendars/public/
```

**Query Parameters:**
- `program_level`: Filter by level
- `school`: Filter by school ID
- `start_date_from`: Filter by start date (YYYY-MM-DD)
- `start_date_to`: Filter by start date (YYYY-MM-DD)
- `search`: Search in program name, school name, skills
- `ordering`: `start_date`, `-start_date`, `published_at`

#### List Upcoming Calendars
```bash
GET /api/calendars/upcoming/
```

**Query Parameters:**
- `months_ahead`: Number of months to look ahead (default: 6)

---

### Partner Companies

#### List Partner Companies
```bash
GET /api/partners/companies/
```

**Query Parameters:**
- `sector`: Filter by sector
- `partnership_type`: Filter by partnership type
- `search`: Search in company name, city, sector
- `ordering`: `partner_since`, `-partner_since`, `total_interns_hosted`, `average_rating`

#### Get Available Sectors
```bash
GET /api/partners/sectors/
```

**Response:**
```json
{
  "sectors": ["Technology", "Finance", "Healthcare", ...]
}
```

#### Get Partner Statistics
```bash
GET /api/partners/stats/
```

**Response:**
```json
{
  "total_partners": 150,
  "total_interns_hosted": 1250,
  "sectors_count": 12,
  "average_rating": 4.5,
  "top_sectors": [
    {"sector": "Technology", "count": 45},
    {"sector": "Finance", "count": 30},
    ...
  ]
}
```

---

### Verification

#### Submit Verification Documents
```bash
POST /api/verification/submit/
Authorization: Bearer <user_token>
Content-Type: multipart/form-data

{
  "documents": [
    {
      "document_type": "ID_CARD",
      "file": <file_upload>,
      "expiry_date": "2030-12-31"
    },
    {
      "document_type": "ADDRESS_PROOF",
      "file": <file_upload>
    }
  ]
}
```

**Document Types:**
- `ID_CARD`, `PASSPORT`, `PROPERTY_PROOF`, `ADDRESS_PROOF`
- `DRIVER_LICENSE`, `VEHICLE_REGISTRATION`, `INSURANCE`, `CRIMINAL_RECORD`

#### Verify Document (Admin Only)
```bash
POST /api/verification/verify/{document_id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "approved": true,
  "rejection_reason": ""
}
```

Or reject:
```json
{
  "approved": false,
  "rejection_reason": "Document is not clear, please resubmit"
}
```

#### List Pending Verifications (Admin Only)
```bash
GET /api/verification/pending/
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `document_type`: Filter by document type
- `user__user_type`: Filter by user type
- `ordering`: `submitted_at`, `-submitted_at`

#### Get User Verification Status
```bash
GET /api/verification/status/
Authorization: Bearer <user_token>
```

**Response:**
```json
{
  "is_verified": true,
  "documents": [
    {
      "id": 1,
      "document_type": "ID_CARD",
      "status": "APPROVED",
      "submitted_at": "2026-01-15T10:30:00Z",
      "verified_at": "2026-01-16T14:20:00Z"
    }
  ]
}
```

---

## Common Use Cases

### Use Case 1: Company Recommends a Student

```bash
# 1. Authenticate as company
POST /api/token/
{
  "username": "company@example.com",
  "password": "password123"
}

# 2. Create recommendation
POST /api/recommendations/create/
Authorization: Bearer <token>
{
  "student": 5,
  "internship": 10,
  "rating": 5,
  "autonomy": 5,
  "teamwork": 4,
  "rigor": 5,
  "creativity": 4,
  "punctuality": 5,
  "comment": "Outstanding performance!",
  "skills_validated": ["Python", "Django"],
  "recommended_domains": ["Web Development"]
}
```

### Use Case 2: School Publishes Internship Calendar

```bash
# 1. Authenticate as school
POST /api/token/
{
  "username": "school@example.com",
  "password": "password123"
}

# 2. Create calendar
POST /api/calendars/create/
Authorization: Bearer <token>
{
  "program_manager": 1,
  "program_name": "Engineering Internship 2026",
  "program_level": "BACHELOR",
  "number_of_students": 30,
  "start_date": "2026-06-01",
  "end_date": "2026-08-31",
  "skills_sought": ["Python", "C++", "Electronics"],
  "description": "Summer internship for engineering students"
}

# 3. Publish calendar
POST /api/calendars/publish/1/
Authorization: Bearer <token>
```

### Use Case 3: Student Views Recommendations

```bash
# No authentication required for public recommendations
GET /api/recommendations/student/5/
```

### Use Case 4: Company Tracks Student Evolution

```bash
# 1. Authenticate as company
POST /api/token/
{
  "username": "company@example.com",
  "password": "password123"
}

# 2. Start tracking
POST /api/evolution/start/
Authorization: Bearer <token>
{
  "student_id": 5,
  "current_level": "BEGINNER",
  "domain": "Web Development"
}

# 3. Update evolution after internship
PATCH /api/evolution/update/1/
Authorization: Bearer <token>
{
  "current_level": "INTERMEDIATE",
  "status": "AVAILABLE"
}

# 4. View all tracked students
GET /api/evolution/tracked/
Authorization: Bearer <token>
```

---

## Error Handling

### Common HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid data provided
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

### Error Response Format

```json
{
  "error": "Error message",
  "detail": "Detailed error description",
  "field_errors": {
    "field_name": ["Error message for this field"]
  }
}
```

### Example Errors

**Invalid Rating:**
```json
{
  "rating": ["Rating must be between 1 and 5."]
}
```

**Permission Denied:**
```json
{
  "detail": "Only companies can perform this action."
}
```

**Authentication Required:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Rate Limits

**Current Status:** No rate limits implemented (recommended for production)

**Recommended Limits:**
- Authentication endpoints: 5 requests/minute
- Verification endpoints: 10 requests/minute
- General endpoints: 100 requests/minute

---

## Testing with cURL

### Example: Complete Recommendation Flow

```bash
# 1. Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"company@test.com","password":"password123"}' \
  | jq -r '.access')

# 2. Create recommendation
curl -X POST http://localhost:8000/api/recommendations/create/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "internship": 1,
    "rating": 5,
    "autonomy": 5,
    "teamwork": 4,
    "rigor": 5,
    "creativity": 4,
    "punctuality": 5,
    "comment": "Excellent!"
  }'

# 3. View student recommendations
curl http://localhost:8000/api/recommendations/student/1/
```

---

## Testing with Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# 1. Authenticate
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "company@test.com",
    "password": "password123"
})
token = response.json()["access"]

# 2. Create recommendation
headers = {"Authorization": f"Bearer {token}"}
data = {
    "student": 1,
    "internship": 1,
    "rating": 5,
    "autonomy": 5,
    "teamwork": 4,
    "rigor": 5,
    "creativity": 4,
    "punctuality": 5,
    "comment": "Excellent intern!"
}
response = requests.post(
    f"{BASE_URL}/recommendations/create/",
    headers=headers,
    json=data
)
print(response.json())

# 3. Get student recommendations
response = requests.get(f"{BASE_URL}/recommendations/student/1/")
print(response.json())
```

---

## Support

For issues or questions:
- Check the full documentation in `docs/PLATFORM_RESTRUCTURING_COMPLETE.md`
- Review API endpoint implementations in `api/views/`
- Check service layer logic in `core/services/`

---

**Last Updated:** February 8, 2026  
**API Version:** 1.0
