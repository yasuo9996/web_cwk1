# HarmonySphere API Documentation (Submission Version)

## Module and Project Context
- Module: Web Services and Web Data (XJCO3011)
- Project: HarmonySphere (Individual Coursework)
- API style: REST-style JSON web service
- Local base URL: `http://127.0.0.1:8000`
- Version prefix: `/v1`

---

## 1. Authentication and Access Control

### 1.1 Required headers
All `/v1/*` endpoints require API key header:

```http
X-API-Key: dev-secret-key
```

User-scoped endpoints additionally require bearer token:

```http
Authorization: Bearer <token>
```

### 1.2 Authentication workflow
1. Register user
2. Login to get token
3. Use token for user-specific endpoints (listening records and personal insights)

---

## 2. API Endpoints Overview

| Category | Method | Endpoint | Purpose |
|---|---|---|---|
| System | GET | `/health` | Service health check |
| Auth | POST | `/v1/auth/register` | Register account |
| Auth | POST | `/v1/auth/login` | Login and return token |
| Auth | GET | `/v1/auth/me` | Get current user |
| Tracks | POST | `/v1/tracks` | Create track |
| Tracks | GET | `/v1/tracks` | List tracks |
| Tracks | GET | `/v1/tracks/features/{track_id}` | Get full feature profile |
| Tracks | GET | `/v1/tracks/similar` | Similar-track recommendation |
| Listening | POST | `/v1/listening-records` | Create listening event |
| Listening | GET | `/v1/listening-records` | List my events |
| Listening | GET | `/v1/listening-records/{record_id}` | Get one event |
| Listening | PUT | `/v1/listening-records/{record_id}` | Update one event |
| Listening | DELETE | `/v1/listening-records/{record_id}` | Delete one event |
| Insights | GET | `/v1/users/me/insights` | Personal preference insights |
| Analytics | GET | `/v1/analytics/feature-distribution` | Feature distribution histogram |

---

## 3. Endpoint Specifications

### 3.1 Health Check
#### `GET /health`
No authentication required.

**Response 200**
```json
{
  "status": "ok",
  "service": "HarmonySphere API",
  "version": "0.1.0"
}
```

---

### 3.2 Register
#### `POST /v1/auth/register`
Create a new user account.

**Request**
```json
{
  "username": "alice",
  "password": "alice123"
}
```

**Response 201**
```json
{
  "id": 1,
  "username": "alice"
}
```

**Error 409**
```json
{
  "detail": "Username already exists"
}
```

---

### 3.3 Login
#### `POST /v1/auth/login`
Authenticate and issue bearer token.

**Request**
```json
{
  "username": "alice",
  "password": "alice123"
}
```

**Response 200**
```json
{
  "token": "<token>",
  "token_type": "bearer"
}
```

**Error 401**
```json
{
  "detail": "Invalid username or password"
}
```

---

### 3.4 Current User
#### `GET /v1/auth/me`
Requires API key + bearer token.

**Response 200**
```json
{
  "id": 1,
  "username": "alice"
}
```

---

### 3.5 Create Track
#### `POST /v1/tracks`
Create a music track with feature attributes.

**Request**
```json
{
  "title": "Blinding Lights",
  "artist": "The Weeknd",
  "album": "After Hours",
  "duration_ms": 200040,
  "popularity": 95,
  "danceability": 0.74,
  "energy": 0.73,
  "loudness": -5.9,
  "valence": 0.34,
  "acousticness": 0.001,
  "tempo": 171.0
}
```

**Response 201**: full track object with generated `id`

---

### 3.6 List Tracks
#### `GET /v1/tracks?limit=10`
Return latest tracks.

**Query**
- `limit` (optional, integer, default 10, min 1, max 100)

**Response 200**
```json
[
  {
    "id": 1,
    "title": "Blinding Lights",
    "artist": "The Weeknd",
    "album": "After Hours",
    "duration_ms": 200040,
    "popularity": 95,
    "danceability": 0.74,
    "energy": 0.73,
    "loudness": -5.9,
    "valence": 0.34,
    "acousticness": 0.001,
    "tempo": 171.0
  }
]
```

---

### 3.7 Track Feature Profile
#### `GET /v1/tracks/features/{track_id}`
Get full feature profile by track id.

**Error 404**
```json
{
  "detail": "Track not found"
}
```

---

### 3.8 Similar Tracks
#### `GET /v1/tracks/similar?track_id=1&limit=5`
Return most similar tracks by cosine similarity.

**Response 200**
```json
[
  {"track_id": 3, "similarity": 0.9781},
  {"track_id": 2, "similarity": 0.9624}
]
```

---

### 3.9 Create Listening Record
#### `POST /v1/listening-records`
Create a listening event for current authenticated user.

**Request**
```json
{
  "track_id": 1,
  "action_type": "like"
}
```

Allowed action types:
- `listen`
- `like`
- `skip`

**Response 201**
```json
{
  "id": 10,
  "user_id": 1,
  "track_id": 1,
  "listened_at": "2026-04-21T12:34:56.789Z",
  "action_type": "like"
}
```

---

### 3.10 List My Listening Records
#### `GET /v1/listening-records`
Returns only records belonging to current user.

**Response 200**: array of ListeningRecord objects

---

### 3.11 Get One Listening Record
#### `GET /v1/listening-records/{record_id}`
Returns one owned record.

**Error 404**
```json
{
  "detail": "Listening record not found"
}
```

---

### 3.12 Update Listening Record
#### `PUT /v1/listening-records/{record_id}`
Update event action type.

**Request**
```json
{
  "action_type": "skip"
}
```

**Response 200**: updated ListeningRecord object

---

### 3.13 Delete Listening Record
#### `DELETE /v1/listening-records/{record_id}`
Delete one owned record.

**Response 204**
No response body.

---

### 3.14 Personal Insights
#### `GET /v1/users/me/insights`
Compute personal profile from listening history and track features.

**Response 200**
```json
{
  "user_id": 1,
  "preferred_energy_range": [0.43, 0.8],
  "preferred_danceability_range": [0.52, 0.74],
  "avg_tempo": 145.75,
  "total_records": 4
}
```

---

### 3.15 Feature Distribution Analytics
#### `GET /v1/analytics/feature-distribution?feature=energy&bins=10`
Return histogram-like distribution for one feature.

Supported features:
- `energy`
- `danceability`
- `valence`
- `acousticness`
- `popularity`
- `tempo`

**Response 200**
```json
{
  "feature": "energy",
  "bins": [
    {"range_start": 0.0, "range_end": 0.1, "count": 0},
    {"range_start": 0.1, "range_end": 0.2, "count": 1}
  ]
}
```

**Error 400**
```json
{
  "detail": "Unsupported feature 'xxx'. Supported: energy, danceability, valence, acousticness, popularity, tempo"
}
```

---

## 4. HTTP Status Codes Used
- `200 OK` – successful read/update
- `201 Created` – resource created
- `204 No Content` – resource deleted
- `400 Bad Request` – invalid query or unsupported feature
- `401 Unauthorized` – invalid/missing API key or token
- `404 Not Found` – resource missing or not owned by user
- `409 Conflict` – duplicate username
- `422 Unprocessable Entity` – validation failure

---

## 5. Quick End-to-End Validation Sequence
1. Register: `POST /v1/auth/register`
2. Login: `POST /v1/auth/login`
3. Create track: `POST /v1/tracks`
4. Create listening event: `POST /v1/listening-records`
5. Query my insights: `GET /v1/users/me/insights`
6. Query distribution: `GET /v1/analytics/feature-distribution`

---

## 6. Documentation Artifacts
- Interactive Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- This document: `API_DOCUMENTATION_SUBMISSION.md`

This file is prepared for conversion to PDF for coursework submission.
