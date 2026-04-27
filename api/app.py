"""Tiny Flask API used to demonstrate a containerized 3-tier stack."""
from __future__ import annotations

import os

from flask import Flask, jsonify

from db import fetch_items

app = Flask(__name__)


@app.get("/health")
def health() -> tuple[dict, int]:
    """Liveness probe — returns 200 once the process is up."""
    return jsonify(status="ok"), 200


@app.get("/items")
def items() -> tuple[dict, int]:
    """Return all rows from the items table."""
    database_url = os.environ.get("DATABASE_URL", "")
    rows = fetch_items(database_url)
    return jsonify(rows), 200


if __name__ == "__main__":
    # Local dev only; in containers we run via gunicorn.
    app.run(host="0.0.0.0", port=5000, debug=False)
