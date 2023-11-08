import pytest

@pytest.fixture(scope="module")
def authenticated_client(app):
    client = app.test_client()
    client.post("/login", data=dict(email="dummy@email.ai", password="notreal"), follow_redirects=True)
    return client