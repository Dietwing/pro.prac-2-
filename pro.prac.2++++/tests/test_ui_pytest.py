import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "nri_combat_analytics_dashboard"
APP_FILE = APP_DIR / "app.py"
BASE_URL = "http://127.0.0.1:8050"


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="module")
def dash_server():
    if not APP_FILE.exists():
        pytest.fail(f"Файл приложения не найден: {APP_FILE}")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    process = subprocess.Popen(
        [sys.executable, str(APP_FILE)],
        cwd=str(APP_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    try:
        if not _wait_for_port("127.0.0.1", 8050, timeout=30):
            stdout, stderr = process.communicate(timeout=5)
            pytest.fail(
                "Приложение не запустилось на порту 8050.\n\n"
                f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
            )
        yield process
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def test_home_page_returns_200(dash_server):
    response = requests.get(BASE_URL, timeout=10)
    assert response.status_code == 200


def test_home_page_contains_project_title(dash_server):
    response = requests.get(BASE_URL, timeout=10)
    html = response.text
    assert "НРИ-Помощник (офлайн)" in html
    assert "Аналитический дашборд" in html


def test_home_page_contains_main_tabs(dash_server):
    response = requests.get(BASE_URL, timeout=10)
    html = response.text
    for tab_name in [
        "Дашборд",
        "Персонажи",
        "Боевые события",
        "Боевые столкновения",
        "Способности",
        "Сессии",
        "Аналитика",
    ]:
        assert tab_name in html


def test_dash_layout_endpoint_is_available(dash_server):
    response = requests.get(f"{BASE_URL}/_dash-layout", timeout=10)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")


def test_dash_dependencies_endpoint_is_available(dash_server):
    response = requests.get(f"{BASE_URL}/_dash-dependencies", timeout=10)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")
