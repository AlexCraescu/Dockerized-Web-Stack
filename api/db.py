"""Database access. Kept tiny on purpose — this is a portfolio demo, not an ORM."""
from __future__ import annotations

from typing import Any


def fetch_items(database_url: str) -> list[dict[str, Any]]:
    """Return all items.

    If `database_url` does not look like a Postgres URL (e.g. during unit
    tests where it's empty or set to `sqlite:///:memory:`), return a
    deterministic in-memory list so the app stays testable without a DB.
    """
    if not database_url.startswith("postgresql://"):
        return [
            {"id": 1, "name": "hello"},
            {"id": 2, "name": "world"},
        ]

    # Imported lazily so unit tests don't need the driver installed.
    import psycopg

    with psycopg.connect(database_url) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name FROM items ORDER BY id")
        return [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
