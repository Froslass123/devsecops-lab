import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client() #Flask's fake browser: it calls the app directly, without a server or network.


def test_home_says_hello(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.text == "hello"


def test_unknown_page_returns_404(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404