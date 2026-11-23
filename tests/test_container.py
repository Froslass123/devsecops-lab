import subprocess
import time
from http.client import HTTPConnection

import pytest


def get(path):
    connection = HTTPConnection("127.0.0.1", 8000, timeout=5)
    connection.request("GET", path)
    response = connection.getresponse()
    return response.status, response.read().decode()


@pytest.fixture(scope="session", autouse=True)
def wait_until_ready():
    for _ in range(10):
        try:
            get("/")
            return
        except OSError:
            time.sleep(0.5)
    pytest.fail("the container never answered on port 8000")


def test_home_says_hello():
    status, body = get("/")

    assert status == 200
    assert body == "hello"

def test_unknown_page_returns_404():
    status, body = get("/does-not-exist")

    assert status == 404


def test_does_not_run_as_root():
    result = subprocess.run(["docker", "exec", "app", "id", "-u"], capture_output=True, text=True, check=True)

    assert result.stdout.strip() != "0"