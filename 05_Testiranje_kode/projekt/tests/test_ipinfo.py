from app.ipinfo import get_my_public_ip
import requests


def test_get_my_public_ip(monkeypatch):
    my_ip = "8.8.8.8"
    test_json_body = {
        "ip": my_ip,
    }

    class MockResponse:
        def __init__(self, json_body) -> None:
            self.status_code = 200
            self.json_body = json_body

        def json(self):
            return self.json_body

    def mock_get(*args, **kwargs):
        return MockResponse(test_json_body)

    monkeypatch.setattr(requests, "get", mock_get)

    assert get_my_public_ip() == (200, my_ip)


def test_get_my_public_ip_failure(monkeypatch):
    test_json_body = {"error": "API down"}

    class MockResponse:
        def __init__(self, json_body) -> None:
            self.status_code = 404
            self.json_body = json_body

        def json(self):
            return self.json_body

    def mock_get(*args, **kwargs):
        return MockResponse(test_json_body)

    monkeypatch.setattr(requests, "get", mock_get)

    assert get_my_public_ip() == (404, None)
