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

def build_summary():
    summary = []
    for r in get_repos():
        rows = get_last_two(r)
        current = rows[0]
        previous = rows[1] if len(rows) == 2 else None
        summary.append({
            "repo": r,
            "stars": current[0],
            "forks": current[1],
            "open_issues": current[2],
            "stars_delta": current[0] - previous[0] if previous else None,
            "forks_delta": current[1] - previous[1] if previous else None,
            "open_issues_delta": current[2] - previous[2] if previous else None,
        })

    return summary


if __name__ == "__main__":
    for item in build_summary():
        print(item)