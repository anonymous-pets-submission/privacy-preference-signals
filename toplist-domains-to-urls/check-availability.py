#!/usr/bin/env python3
import fileinput
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple, Tuple

import httpx
import util

here = Path(__file__).absolute().parent


class Result(NamedTuple):
    domain: str
    url: str
    timestamp: datetime
    success: bool
    details: str


def try_connect(url) -> Tuple[bool, str]:
    try:
        # We could spoof Chrome headers here, but what's the point?
        resp = httpx.get(
            url,
            allow_redirects=False,
            timeout=30,
        )
        return resp.status_code < 400, json.dumps({
            "status_code": resp.status_code,
            "headers": resp.headers.multi_items(),
            "elapsed": resp.elapsed.total_seconds()
        })
    except Exception as e:
        return False, json.dumps({
            "error": str(e)
        })


def check_domain(domain: str) -> List[Result]:
    results = []
    # Order matters here: the latest timestamp is used.
    for proto in ["http", "https"]:
        for prefix in ["", "www."]:
            url = f"{proto}://{prefix}{domain}/"
            result = Result(domain, url, datetime.now(), *try_connect(url))
            results.append(result)
    return results


if __name__ == "__main__":
    print("Ingesting domains...")
    todo = list({
        line.split(",")[-1].strip()
        for line in fileinput.input()
    })
    print(f"Unique entries: {len(todo)}")

    db = sqlite3.connect(util.data / "tranco-reachability.db")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS requests (
          domain,
          url,
          timestamp,
          success,
          details
    )
    """)

    print(f'Existing records: {db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]}')

    start = time.time()
    for i, results in enumerate(util.as_completed(check_domain, todo)):
        with db:
            db.executemany("INSERT INTO requests (domain, url, timestamp, success, details) VALUES(?,?,?,?,?);", results)
        if i % 100 == 0:
            print(f"{100 * i / len(todo):.2f}% {time.time() - start:.1f}s")
