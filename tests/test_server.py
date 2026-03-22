"""T034 [US3] Server transport tests."""

import os
import subprocess
import sys
import time

import httpx
import pytest


@pytest.fixture()
def streamable_http_server():
    """Start the server with streamable-http transport and yield the base URL."""
    env = os.environ.copy()
    env["MCP_TRANSPORT"] = "streamable-http"
    env["MCP_HOST"] = "127.0.0.1"
    env["MCP_PORT"] = "3001"

    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_tekna"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to be ready by polling the /mcp endpoint
    # GET /mcp returns 405 or 406 when the server is up (expects POST)
    base = "http://127.0.0.1:3001"
    for _ in range(30):
        try:
            resp = httpx.get(f"{base}/mcp", timeout=1.0)
            if resp.status_code in (405, 406):
                break
        except (httpx.ConnectError, httpx.ReadError, httpx.ConnectTimeout):
            time.sleep(0.5)
    else:
        proc.kill()
        pytest.fail("Server did not start within 15 seconds")

    yield base

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


class TestStreamableHttp:
    """T034 [US3] Server starts with streamable-http transport."""

    def test_mcp_endpoint_responds(self, streamable_http_server: str) -> None:
        """Server responds on the configured port via /mcp endpoint."""
        resp = httpx.get(f"{streamable_http_server}/mcp", timeout=5.0)
        # GET returns 405/406 because MCP expects POST - but the server is up
        assert resp.status_code in (405, 406)
