from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import API_KEY_HEADER
from app.database import Base, get_db
from app.main import app
from app.models import Track


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_harmonysphere.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
API_HEADERS = {API_KEY_HEADER: "dev-secret-key"}



def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        tracks = [
            Track(
                title="Test Track A",
                artist="Artist A",
                album="Album A",
                duration_ms=200000,
                popularity=70,
                danceability=0.8,
                energy=0.9,
                loudness=-5.0,
                valence=0.6,
                acousticness=0.1,
                tempo=128.0,
            ),
            Track(
                title="Test Track B",
                artist="Artist B",
                album="Album B",
                duration_ms=190000,
                popularity=60,
                danceability=0.7,
                energy=0.75,
                loudness=-6.0,
                valence=0.5,
                acousticness=0.2,
                tempo=120.0,
            ),
        ]
        db.add_all(tracks)
        db.commit()
    finally:
        db.close()



def teardown_module():
    Base.metadata.drop_all(bind=engine)



def auth_headers(username: str = "tester", password: str = "tester123"):
    register = client.post(
        "/v1/auth/register",
        headers=API_HEADERS,
        json={"username": username, "password": password},
    )
    if register.status_code not in (201, 409):
        raise AssertionError(f"register failed: {register.status_code} {register.text}")

    login = client.post(
        "/v1/auth/login",
        headers=API_HEADERS,
        json={"username": username, "password": password},
    )
    assert login.status_code == 200
    token = login.json()["token"]
    return {**API_HEADERS, "Authorization": f"Bearer {token}"}



def test_health_public_endpoint():
    response = client.get("/health")
    assert response.status_code == 200



def test_auth_required_on_protected_endpoint():
    response = client.get("/v1/listening-records")
    assert response.status_code == 401



def test_register_login_and_me():
    headers = auth_headers("auth_user", "auth_pass_123")
    me = client.get("/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["username"] == "auth_user"



def test_track_endpoints_and_error_handling():
    headers = auth_headers("track_user", "track_pass_123")

    list_response = client.get("/v1/tracks?limit=5", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 2

    features_response = client.get("/v1/tracks/features/1", headers=headers)
    assert features_response.status_code == 200
    assert features_response.json()["id"] == 1

    similar_response = client.get("/v1/tracks/similar?track_id=1&limit=3", headers=headers)
    assert similar_response.status_code == 200
    assert isinstance(similar_response.json(), list)

    missing_track = client.get("/v1/tracks/features/9999", headers=headers)
    assert missing_track.status_code == 404



def test_listening_crud_user_scoped_flow():
    headers = auth_headers("listen_user", "listen_pass_123")

    create_response = client.post(
        "/v1/listening-records",
        headers=headers,
        json={"user_id": 999, "track_id": 1, "action_type": "listen"},
    )
    assert create_response.status_code == 201
    created = create_response.json()
    record_id = created["id"]

    list_response = client.get("/v1/listening-records", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == record_id for item in list_response.json())

    detail_response = client.get(f"/v1/listening-records/{record_id}", headers=headers)
    assert detail_response.status_code == 200
    assert detail_response.json()["action_type"] == "listen"

    update_response = client.put(
        f"/v1/listening-records/{record_id}",
        headers=headers,
        json={"action_type": "like"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["action_type"] == "like"

    delete_response = client.delete(f"/v1/listening-records/{record_id}", headers=headers)
    assert delete_response.status_code == 204

    after_delete = client.get(f"/v1/listening-records/{record_id}", headers=headers)
    assert after_delete.status_code == 404



def test_insights_and_analytics_endpoints():
    headers = auth_headers("insight_user", "insight_pass_123")

    create_one = client.post(
        "/v1/listening-records",
        headers=headers,
        json={"user_id": 1, "track_id": 1, "action_type": "like"},
    )
    assert create_one.status_code == 201

    create_two = client.post(
        "/v1/listening-records",
        headers=headers,
        json={"user_id": 1, "track_id": 2, "action_type": "listen"},
    )
    assert create_two.status_code == 201

    insights = client.get("/v1/users/me/insights", headers=headers)
    assert insights.status_code == 200
    payload = insights.json()
    assert payload["total_records"] >= 2
    assert payload["preferred_energy_range"] is not None

    distribution = client.get(
        "/v1/analytics/feature-distribution?feature=energy&bins=5",
        headers=headers,
    )
    assert distribution.status_code == 200
    assert distribution.json()["feature"] == "energy"

    bad_feature = client.get(
        "/v1/analytics/feature-distribution?feature=unknown&bins=5",
        headers=headers,
    )
    assert bad_feature.status_code == 400
