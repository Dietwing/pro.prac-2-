import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "nri_combat_analytics_dashboard"
APP_FILE = APP_DIR / "app.py"


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="session", autouse=True)
def run_dash_server_for_ui_tests(request):
    needs_server = any("playwright" in item.nodeid for item in request.session.items)
    if not needs_server:
        yield
        return

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
            process.terminate()
            raise RuntimeError("Dash-приложение не успело запуститься для Playwright-тестов.")
        yield
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
