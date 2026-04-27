"""Unit tests for the Flask API.

The DB layer falls back to a deterministic in-memory list when DATABASE_URL
isn't a Postgres URL, so we can run the full HTTP test suite with no DB.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Make `api/` importable when pytest runs from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DATABASE_URL", "")

from app import app  # noqa: E402


def test_health_returns_ok():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_items_returns_seed_data_without_db():
    client = app.test_client()
    resp = client.get("/items")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert isinstance(payload, list)
    assert payload[0] == {"id": 1, "name": "hello"}
