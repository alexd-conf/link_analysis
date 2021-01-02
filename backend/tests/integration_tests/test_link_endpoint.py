import json

from backend.app import app


class TestLink:
    def test_link_endpoint_proper_url(self):
        # a good URL
        test_url = "https://www.google.com"
        with app.test_client() as request:
            response = request.post("/api/link", json={"url": test_url})
            response_json = response.get_json()
            assert response_json["status"] == 0
    
    def test_link_endpoint_malformed_url(self):
        # a bad URL
        test_url = ""
        with app.test_client() as request:
            response = request.post("/api/link", json={"url": test_url})
            response_json = response.get_json()
            assert response_json["status"] == 1
