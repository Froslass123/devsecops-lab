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


def test_home_lists_the_notes():
    status, body = get("/")

    assert status == 200
    assert "hello there" in body

def test_unknown_page_returns_404():
    status, body = get("/does-not-exist")

    assert status == 404


def test_does_not_run_as_root():
    result = subprocess.run(["docker", "exec", "app", "id", "-u"], capture_output=True, text=True, check=True)

    assert result.stdout.strip() != "0"

def test_filesystem_is_read_only():
    result = subprocess.run(["docker", "exec", "app", "touch", "/home/appuser/test"], capture_output=True, text=True)

    assert "Read-only file system" in result.stderr


def test_has_no_extra_privileges():
    result = subprocess.run(["docker", "exec", "app", "cat", "/proc/1/status"], capture_output=True, text=True, check=True)
    status = dict(line.split(":\t", 1) for line in result.stdout.splitlines() if ":\t" in line)

    assert int(status["CapBnd"], 16) == 0 #the root powers (capabilities) the process could ever get, as a hex number. 0 means none.
    assert status["NoNewPrivs"] == "1" #1 means it can't gain privileges, for example through sudo-style programs.