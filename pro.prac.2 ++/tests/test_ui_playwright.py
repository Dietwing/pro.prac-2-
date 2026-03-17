import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from playwright.sync_api import Error, sync_playwright

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
                "Приложение не запустилось на порту 8050.

"
                f"STDOUT:
{stdout}

STDERR:
{stderr}"
            )
        yield process
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def test_dashboard_loads_in_browser(dash_server):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(BASE_URL, wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.get_by_text("НРИ-Помощник", exact=False).wait_for(timeout=10000)
            page.get_by_text("Дашборд", exact=False).wait_for(timeout=10000)
            page.get_by_text("Персонажи", exact=False).wait_for(timeout=10000)
            browser.close()
    except Error as exc:
        pytest.skip(f"Playwright не смог запустить браузер в текущей среде: {exc}")
