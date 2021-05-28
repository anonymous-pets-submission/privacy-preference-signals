#!/usr/bin/env python3

import fileinput
import sqlite3

import util

if __name__ == "__main__":
    # order-preserving unique. :)
    todo = dict.fromkeys(
        line.split(",")[-1].strip()
        for line in fileinput.input()
    )

    db = sqlite3.connect(util.data / "tranco-reachability.db")

    # This is a bit of a hack, but https > http and www. > no prefix is what we want.
    urls = dict(db.execute("""
                SELECT domain, MAX(url) 
                FROM requests 
                WHERE success = 1
                GROUP BY domain
            """))

    for domain in todo:
        url = urls.get(domain, f"http://{domain}/")
        print(f"{domain},{url}")
