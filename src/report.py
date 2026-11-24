import csv
import sqlite3
from contextlib import closing

from db import DB_PATH

def get_repos():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute(
            "SELECT DISTINCT repo FROM snapshots "
            "ORDER BY repo"
        ).fetchall()

    return [row[0] for row in rows]

def get_last_two(repo):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute(
            "SELECT stars, forks, open_issues, collected_at "
            "FROM snapshots WHERE repo = ? "
            "ORDER BY collected_at DESC LIMIT 2",
            (repo,)
        ).fetchall()

    return rows

if __name__ == "__main__":
    for r in get_repos():
        print(r, get_last_two(r))