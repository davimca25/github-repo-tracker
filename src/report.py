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

def write_csv(summary, path="summary.csv"):
    if not summary:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

def fmt(delta):
    if delta is None:
        return "-"
    return f"{delta:+d}"

    
def print_summary(summary):
    if not summary:
        print("no data yet")
        return

    print(f"{'repo':<25} {'stars':>8} {'Δ stars':>8}")
    for item in summary:
        print(f"{item['repo']:<25} {item['stars']:>8} {fmt(item['stars_delta']):>8}")


if __name__ == "__main__":
    summary = build_summary()
    print_summary(summary)
    write_csv(summary)