# HarmonySphere API

A music-themed web service project for the module **Web Services and Web Data (XJCO3011)**.

HarmonySphere provides:
- user authentication,
- track management,
- user listening behavior CRUD,
- feature-based similarity recommendations,
- personal and global music analytics,
- product-style frontend pages.

---

## 1. Coursework Deliverables Index

This section is included to match the coursework submission checklist.

- **Public GitHub Repository**: (https://github.com/yasuo9996/web_cwk1.git)
- **API Documentation (Markdown)**: (https://github.com/yasuo9996/web_cwk1/blob/main/API_DOCUMENTATION_SUBMISSION.md)
- **API Documentation (PDF)**: (https://github.com/yasuo9996/web_cwk1/blob/main/API_DOCUMENTATION_SUBMISSION.pdf)
- **Technical Report (Markdown)**: (https://github.com/yasuo9996/web_cwk1/blob/main/TECHNICAL_REPORT.md)
- **Technical Report (PDF)**: (https://github.com/yasuo9996/web_cwk1/blob/main/TECHNICAL_REPORT.pdf)
- **GenAI Appendix Template**: (https://github.com/yasuo9996/web_cwk1/blob/main/TECHNICAL_REPORT.pdf)
- **Presentation Slides (PPTX)**: (https://github.com/yasuo9996/web_cwk1/blob/main/HarmonySphere%20API%20Presentation.pptx)

---

## 2. Project Features

### 2.1 Authentication
- Register: `POST /v1/auth/register`
- Login: `POST /v1/auth/login`
- Current user: `GET /v1/auth/me`

### 2.2 Tracks
- Create track: `POST /v1/tracks`
- List tracks: `GET /v1/tracks`
- Track features: `GET /v1/tracks/features/{track_id}`
- Similar tracks (cosine similarity): `GET /v1/tracks/similar?track_id=...&limit=...`

### 2.3 Listening Records (CRUD)
- Create: `POST /v1/listening-records`
- Read list: `GET /v1/listening-records`
- Read single: `GET /v1/listening-records/{record_id}`
- Update: `PUT /v1/listening-records/{record_id}`
- Delete: `DELETE /v1/listening-records/{record_id}`

### 2.4 Insights and Analytics
- My insights: `GET /v1/users/me/insights`
- Feature distribution: `GET /v1/analytics/feature-distribution?feature=...&bins=...`

---

## 3. Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: SQLite
- **Server**: Uvicorn
- **Testing**: Pytest + FastAPI TestClient
- **Frontend**: HTML/CSS/JavaScript

---

## 4. Setup and Run

### 4.1 Prerequisites
- Python 3.10+

### 4.2 Install dependencies
```bash
pip install -r requirements.txt
```

### 4.3 Run server
```bash
python manage.py runserver
```

Default local URL:
- `http://127.0.0.1:8000`

---

## 5. Frontend Pages

- Login page: `http://127.0.0.1:8000/`
- Home page: `http://127.0.0.1:8000/home`
- Discover tracks: `http://127.0.0.1:8000/tracks`
- Favorites/listening: `http://127.0.0.1:8000/listening`
- Insights page: `http://127.0.0.1:8000/insights`

---

## 6. Authentication Usage

All `/v1/*` endpoints require:

1. API Key header:
```http
X-API-Key: dev-secret-key
```

2. For user-scoped endpoints, also include Bearer token:
```http
Authorization: Bearer <token>
```

Get token via login endpoint:
- `POST /v1/auth/login`

---

## 7. API Documentation

- Interactive docs (Swagger): `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Full API write-up: `API_DOCUMENTATION.pdf`

---

## 8. Testing

Run tests with:

```bash
python -m pytest -q
```

The test suite covers:
- auth-required protection,
- auth flow (register/login/me),
- CRUD lifecycle,
- error handling,
- insights and analytics endpoints.

---

## 9. Mapping to Coursework Minimum Requirements

- At least one model with full CRUD + database: **Yes** (`listening-records`, SQLite)
- At least four endpoints: **Yes**
- JSON responses and input handling: **Yes**
- Correct status/error codes: **Yes**
- Runnable demonstration: **Yes** (local run via `manage.py runserver`)

---

## 10. GenAI Declaration (Summary)

GenAI tools were used for planning, debugging support, and documentation drafting. All outputs were reviewed and adapted manually before inclusion.

Detailed declaration and log template:
- `GENAI_APPENDIX_TEMPLATE.pdf`

---

## 11. Author

- Student Name: Yi Fanyu
- Student ID: 201690960
- Module: Web Services and Web Data (XJCO3011)
