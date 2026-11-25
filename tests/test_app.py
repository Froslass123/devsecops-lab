import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client() #Flask's fake browser: it calls the app directly, without a server or network.


def test_home_lists_the_notes(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "hello there" in response.text


def test_unknown_page_returns_404(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404

@pytest.mark.parametrize("path", ["/", "/does-not-exist"])
@pytest.mark.parametrize("header", [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Permissions-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
])
def test_security_headers_are_set(client, path, header):
    assert header in client.get(path).headers


def test_search_finds_only_matching_notes(client):
    page = client.get("/?search=hello").text

    assert "hello there" in page
    assert "walk the dog" not in page


def test_search_is_safe_from_sql_injection(client):
    response = client.get("/", query_string={"search": "' OR 1=1 --"}) #tries to list every note

    assert response.status_code == 200
    assert "hello there" not in response.text


def test_search_is_safe_from_xss(client):
    page = client.get("/", query_string={"search": "<script>alert(1)</script>"}).text

    assert "<script>" not in page