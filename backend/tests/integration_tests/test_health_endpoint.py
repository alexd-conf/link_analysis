import json

from backend.app import app


class TestHealth:
    def test_link_endpoint_proper_url(self):
        with app.test_client() as request:
            response = request.get("/api/health")
            response_json = response.get_json()
            assert response_json["status"] == 0
