import sqlite3
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path


class DatabaseClient:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, key TEXT UNIQUE NOT NULL, "
                         "fingerprint TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 0)")

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()
