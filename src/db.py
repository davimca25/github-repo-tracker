import sqlite3
from contextlib import closing
from datetime import datetime, timezone

DB_PATH = "data.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo TEXT NOT NULL,
                    stars INTEGER NOT NULL,
                    forks INTEGER NOT NULL,
                    open_issues INTEGER NOT NULL,
                    collected_at TEXT NOT NULL
                )
                """
            )

def save_snapshot(data):
    collected_at = datetime.now(timezone.utc).isoformat()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO snapshots (repo, stars, forks, open_issues, collected_at) " 
                "VALUES (?, ?, ?, ?, ?)",
                (
                    data["repo"],
                    data["stars"],
                    data["forks"],
                    data["open_issues"],
                    collected_at
                )
            )