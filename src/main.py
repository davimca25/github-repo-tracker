
import logging
import sys

import requests

from api import fetch_repo
from db import init_db, save_snapshot

logger = logging.getLogger(__name__)

REPOS = [
    ("psf", "requests"),
    ("pallets", "flask"),
    ("pandas-dev", "pandas"),
]

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    init_db()

    ok = 0
    failed = 0

    for owner, repo in REPOS:
        try:
            data = fetch_repo(owner, repo)
            save_snapshot(data)
            ok += 1
            logger.info("Collected %s (%d stars)", data["repo"], data["stars"])
        except (requests.RequestException, ValueError) as e:
            failed += 1
            logger.error("Skipping %s/%s due to error: %s", owner, repo, e)

    logger.info("Finished run: ok=%d failed=%d", ok, failed)

    if ok == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
