from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Track


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.track = Track.objects.create(
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000,
            popularity=70,
            danceability=0.6,
            energy=0.8,
            loudness=-6.0,
            valence=0.7,
            acousticness=0.2,
            tempo=120.0,
        )
        self.auth_headers = {"HTTP_X_API_KEY": settings.API_KEY}

    def test_protected_endpoint_requires_api_key(self):
        res = self.client.get("/v1/listening")
        self.assertEqual(res.status_code, 403)

    def test_listening_crud(self):
        create_res = self.client.post(
            "/v1/listening/log",
            data={"user_id": 1, "track_id": self.track.id, "action_type": "listen"},
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(create_res.status_code, 201)
        record_id = create_res.json()["id"]

        list_res = self.client.get("/v1/listening", **self.auth_headers)
        self.assertEqual(list_res.status_code, 200)
        self.assertGreaterEqual(len(list_res.json()), 1)

        detail_res = self.client.get(f"/v1/listening/{record_id}", **self.auth_headers)
        self.assertEqual(detail_res.status_code, 200)

        update_res = self.client.put(
            f"/v1/listening/{record_id}",
            data={"action_type": "like"},
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.json()["action_type"], "like")

        delete_res = self.client.delete(f"/v1/listening/{record_id}", **self.auth_headers)
        self.assertEqual(delete_res.status_code, 204)
