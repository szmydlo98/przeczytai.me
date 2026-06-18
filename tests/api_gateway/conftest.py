import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import httpx
import pytest

from helpers import create_reading, wait_for_completed


REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def api_base_url() -> str:
    url = os.getenv("API_BASE_URL") or os.getenv("API_GATEWAY_BASE_URL")
    if url:
        return url.rstrip("/")

    if not shutil.which("terraform"):
        pytest.skip(
            "Set API_BASE_URL or install Terraform before running API Gateway tests."
        )

    tf_dir = REPO_ROOT / "infrastructure" / "environments" / "dev"
    result = subprocess.run(
        ["terraform", f"-chdir={tf_dir}", "output", "-raw", "api_base_url"],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        pytest.skip(
            "Set API_BASE_URL or deploy the dev Terraform stack before running these tests."
        )
    return result.stdout.strip().rstrip("/")


@pytest.fixture(scope="session")
def api_bearer_token() -> str:
    token = os.getenv("CLERK_JWT")
    if not token:
        pytest.skip("Set CLERK_JWT to run API Gateway tests against protected routes.")
    return token


@pytest.fixture
def public_api_client(api_base_url: str) -> httpx.Client:
    with httpx.Client(base_url=api_base_url, timeout=60.0) as client:
        yield client


@pytest.fixture
def api_client(api_base_url: str, api_bearer_token: str) -> httpx.Client:
    with httpx.Client(
        base_url=api_base_url,
        headers={"Authorization": f"Bearer {api_bearer_token}"},
        timeout=60.0,
    ) as client:
        yield client


@pytest.fixture(scope="session")
def completed_reading(api_base_url: str, api_bearer_token: str) -> dict[str, Any]:
    with httpx.Client(
        base_url=api_base_url,
        headers={"Authorization": f"Bearer {api_bearer_token}"},
        timeout=60.0,
    ) as client:
        created = create_reading(client)
        completed = wait_for_completed(client, created["id"])
        completed["submitted_text"] = created["submitted_text"]
        return completed
