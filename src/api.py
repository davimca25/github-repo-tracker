import os
import logging
import requests

logger = logging.getLogger(__name__)
REQUIRED_KEYS = ["stargazers_count", "forks_count", "open_issues_count"]

def fetch_repo(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {"Accept": "application/vnd.github+json"}

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except  requests.RequestException as e: 
        logger.error("Failed to fetch %s/%s: %s", owner, repo, e)
        raise

    if not isinstance(data, dict):
        raise ValueError(f"Response error {owner}/{repo}: expected JSON object")

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"Response error {owner}/{repo}: missing {missing}")

    return {
        "repo": f"{owner}/{repo}",
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
    }