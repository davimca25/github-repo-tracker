# GitHub Repository Tracker

An automated data pipeline built in Python that tracks daily metrics (`stars`, `forks`, and `open_issues`) of selected open-source GitHub repositories, persists historical snapshots in SQLite, and generates delta reports via GitHub Actions.

## Architecture & Workflow

```
GitHub REST API  ──►  src/api.py (Fetch & Validate)
                           │
                           ▼
SQLite (data.db) ◄──  src/db.py (Parameterized Persistence)
                           │
                           ▼
summary.csv      ◄──  src/report.py (Delta Calculation & CSV Export)

```

1. **Collection (`src/api.py`):** Queries the GitHub REST API v3 with explicit timeouts, `User-Agent` headers, optional `GITHUB_TOKEN` authentication, and response schema validation.

2. **Persistence (`src/db.py`):** Stores timestamped snapshots in a local SQLite database (`data.db`) using context managers (`contextlib.closing` + transactional commits) and parameterized SQL queries.

3. **Orchestration (`src/main.py`):** Iterates over target repositories with structured logging and graceful degradation — individual repository failures are logged and skipped without aborting the batch, exiting with code `1` only on total failure.

4. **Reporting (`src/report.py`):** Compares the two most recent snapshots per repository to compute metric deltas (`stars_delta`, `forks_delta`, `open_issues_delta`), prints a formatted summary table, and exports `summary.csv`.

5. **Automation (`.github/workflows/collect.yml`):** Runs daily at `11:00 UTC` (and on-demand via `workflow_dispatch`), committing updated `data.db` and `summary.csv` artifacts back to the repository.

## Project Structure

```
github-repo-tracker/
├── .github/
│   └── workflows/
│       └── collect.yml      # Scheduled & manual CI/CD collection pipeline
├── src/
│   ├── api.py               # GitHub REST API client and payload validation
│   ├── db.py                # SQLite schema initialization and snapshot inserts
│   ├── main.py              # Pipeline orchestrator and error handling
│   └── report.py            # Historical delta computation and CSV generator
├── data.db                  # SQLite database storing historical snapshots
├── summary.csv              # Latest generated metrics and delta report
├── requirements.txt         # Python dependencies
└── README.md

```

## Tracked Repositories

* [`psf/requests`](https://github.com/psf/requests)

* [`pallets/flask`](https://github.com/pallets/flask)

* [`pandas-dev/pandas`](https://github.com/pandas-dev/pandas)

## Getting Started

### Prerequisites

* Python 3.12+

* `pip`

### Local Setup & Execution

1. **Clone the repository:**

   ```
   git clone https://github.com/davimca25/github-repo-tracker.git
   cd github-repo-tracker
   
   ```

2. **Create and activate a virtual environment:**

   ```
   python -m venv .venv
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   # Linux / macOS
   source .venv/bin/activate
   
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

4. **Run the pipeline:**

   ```
   python src/main.py
   python src/report.py
   
   ```

*(Optional)* Set a `GITHUB_TOKEN` environment variable to increase GitHub REST API rate limits from 60 to 5,000 requests/hour:

```
export GITHUB_TOKEN="your_personal_access_token"

```

## Sample Output

Console output produced by `src/report.py`:

```
repo                         stars  Δ stars
pallets/flask                68500       +4
pandas-dev/pandas            44200       +7
psf/requests                 52400       +3

```

## Key Engineering Decisions

* **Graceful Degradation:** Network errors or malformed payloads on a single repository increment a `failed` counter and log the error without halting data collection for the remaining repositories.

* **SQL Injection Prevention & Resource Safety:** All SQLite queries use `?` placeholders instead of string interpolation, wrapped in `closing()` and transactional `with conn:` blocks to ensure atomic commits and deterministic file handle cleanup.

* **Zero-Infrastructure Persistence:** Committing `data.db` and `summary.csv` via GitHub Actions eliminates external database hosting costs while keeping an auditable version history of every collection run.