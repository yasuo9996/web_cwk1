# HarmonySphere Technical Report

## 1. Project Overview
HarmonySphere is a music-themed web services project that combines a SQL-backed API with a product-style frontend. The system supports authenticated users to discover tracks, record listening behavior, receive feature-based similarity recommendations, and view personal music insights.

This project addresses three objectives:
1. Deliver a complete data-driven API with reliable CRUD behavior.
2. Provide explainable analytics/recommendation without black-box LLM inference.
3. Demonstrate practical software engineering quality in implementation, testing, and presentation readiness.

In the context of the module, the project is intentionally positioned as both an API engineering exercise and a usability exercise. The API layer demonstrates correctness and technical reasoning, while the frontend layer demonstrates that the service can be consumed in a realistic user journey.

## 2. Architecture and Technology Choices
### 2.1 Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Server**: Uvicorn
- **Frontend**: Multi-page HTML/CSS/JavaScript

### 2.2 Rationale
- **FastAPI**: fast implementation, automatic validation/docs, clean routing.
- **SQLAlchemy**: clear relational modeling and maintainable queries.
- **SQLite**: lightweight local reproducibility for coursework demonstration.
- **Vanilla frontend**: low complexity and direct control of user interactions.

### 2.3 System structure
- `routers/`: endpoint orchestration
- `models/` + `schemas/`: persistence and validation contracts
- `services.py`: reusable computation logic (cosine similarity)
- `pages/` + `static/`: user-facing interface
![structure](image1.png)

This separation improved clarity, extensibility, and testing.

### 2.4 Trade-off discussion
A key design trade-off was choosing implementation speed and clarity over production-level complexity. For example, SQLite and a lightweight token table are adequate for coursework reliability and demo reproducibility, but a production deployment would require stronger security controls, migration discipline, and scaling strategy. This trade-off was intentional and aligned with assessment scope.

## 3. Data Model and API Design
### 3.1 Core entities
- **AppUser**: account identity
- **AuthToken**: bearer token session records
- **Track**: music metadata + acoustic-style features (`energy`, `danceability`, `valence`, `acousticness`, `tempo`, etc.)
- **ListeningRecord**: user behavior events (`listen`, `like`, `skip`)

### 3.2 API design highlights
- Versioned API prefix: `/v1`
- Two-layer protection:
  - `X-API-Key` for `/v1/*`
  - Bearer token for user-context operations
- CRUD completeness shown in `listening-records`:
  - Create: `POST /v1/listening-records`
  - Read: `GET /v1/listening-records`, `GET /v1/listening-records/{id}`
  - Update: `PUT /v1/listening-records/{id}`
  - Delete: `DELETE /v1/listening-records/{id}`

### 3.3 Recommendation and analytics
- **Similarity**: cosine similarity over normalized track feature vectors.
- **Personal insights**: preferred energy/danceability ranges + average tempo from user history.
- **Global analytics**: histogram-style feature distributions (`energy`, `tempo`, etc.).

This keeps recommendations deterministic, explainable, and easy to validate.

### 3.4 Why this is still innovative without LLM inference
The project deliberately avoids model-heavy recommendation pipelines and instead focuses on transparent behavior. The recommendation output is reproducible, feature-driven, and auditable. This is valuable in domains where explainability matters (music curation, education demos, and controlled analytics use-cases).

## 4. Implementation Challenges and Resolutions
1. **Route mismatches (frontend vs backend)**
   - Issue: inconsistent paths caused `404 Not Found`.
   - Fix: standardized endpoint usage and updated page API calls.

2. **Database schema evolution**
   - Issue: runtime errors after adding authentication tables.
   - Fix: startup table initialization (`Base.metadata.create_all`).

3. **User identity trust**
   - Issue: client-supplied `user_id` was insecure.
   - Fix: backend now derives user identity from bearer token and scopes record operations to current user.

4. **Frontend usability vs debug output**
   - Issue: early pages exposed raw JSON blocks unsuitable for user-facing interaction.
   - Fix: redesigned to product-style cards, navigation, and interaction flows; user actions now map to API behavior without requiring manual JSON inspection.

These changes significantly improved reliability, security semantics, and user experience.

## 5. Testing Strategy and Evidence
### 5.1 Testing goals
Validate:
- authentication correctness,
- CRUD correctness,
- user authorization boundaries,
- error handling,
- analytics/recommendation endpoint behavior.

### 5.2 Method
`pytest` + FastAPI `TestClient` with isolated test database.

### 5.3 Covered scenarios
- Public endpoint: `/health`
- Auth flow: register/login/me
- Protected endpoint rejection without credentials (`401`)
- Listening records full CRUD lifecycle
- Track listing/features/similar endpoints
- Personal insights and feature-distribution analytics
- Representative error cases (`400`, `404`, `401`)

### 5.4 Result
All implemented tests pass with local execution via:

```bash
python -m pytest -q
```

This provides evidence that the service is functionally correct on core paths.

### 5.5 Testing limitations
Current tests focus on functional API behavior. Additional non-functional tests (load/performance and concurrency) are not yet included. This is acceptable for coursework scope but remains an identified improvement area.

![testResults](image.png)

## 6. Frontend Product Experience
The frontend was implemented as multi-page product navigation rather than a single technical console. The flow is:
- Login/Register page
- Home page with music-focused navigation
- Discovery page for tracks and similarity interactions
- Favorites/listening page for user behavior management
- Insights page for personal metrics and global feature statistics

Design choices include consistent visual hierarchy, card-based layout, clear call-to-action buttons, and minimal friction interaction patterns. These choices improve oral-demo quality because user journeys are easy to explain and demonstrate in a short time window.

## 7. Limitations and Future Work
### 7.1 Current limitations
- Password hashing is simplified and not production-grade.
- Token lifecycle currently lacks expiry/refresh/revocation.
- Spotify integration is example-driven rather than live ingestion.
- SQLite is suitable for coursework but limited for scale.

### 7.2 Future improvements
- Replace hashing/token approach with stronger production auth design.
- Integrate live Spotify API import/search.
- Add richer recommendation explanations and user trend dashboards.
- Add CI-based automated tests and cloud deployment.

## 8. Generative AI Declaration and Reflection
Generative AI tools were used for planning, debugging assistance, and documentation drafting. Outputs were treated as drafts, then manually reviewed, revised, and validated through execution/testing.

AI improved iteration speed and idea exploration, but route/assumption errors still required human verification. Final architecture, endpoint behavior, quality checks, and submission materials were finalized through independent judgment.

## 9. Conclusion
HarmonySphere satisfies coursework technical expectations by delivering:
- a SQL-backed API,
- complete CRUD for user behavior records,
- authentication and user-scoped data access,
- explainable recommendation and analytics,
- a usable product-style frontend.

The project demonstrates sound engineering choices, justified design decisions, and reflective development practice aligned with the assessment criteria. With strengthened production security and live data ingestion in future iterations, the system can evolve from coursework prototype to a more deployment-ready service.
