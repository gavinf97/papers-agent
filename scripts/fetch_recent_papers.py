#!/usr/bin/env python3
"""Query Europe PMC for papers in the target journals published in a date window.

Stdlib only (urllib) -- no dependencies to install. Prints a compact JSON array
to stdout: [{title, doi, journal, date, abstract}, ...].
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

EUROPEPMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
ABSTRACT_CHAR_LIMIT = 500

JOURNALS = [
    "Nature",
    "Nature Methods",
    "Nature Machine Intelligence",
    "Science",
    "Bioinformatics",
    "Scientific Data",
    "PLOS Computational Biology",
    "PLOS Biology",
    "Nucleic Acids Research",
    "Database (Oxford)",
]


def build_query(since: str, until: str) -> str:
    journal_clause = " OR ".join(f'JOURNAL:"{j}"' for j in JOURNALS)
    return f'({journal_clause}) AND FIRST_PDATE:[{since} TO {until}]'


def fetch_page(query: str, cursor_mark: str, page_size: int = 100) -> dict:
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": str(page_size),
        "cursorMark": cursor_mark,
    }
    url = f"{EUROPEPMC_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "papers-agent/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract(record: dict) -> dict | None:
    doi = record.get("doi")
    if not doi:
        return None
    abstract = record.get("abstractText", "")
    if len(abstract) > ABSTRACT_CHAR_LIMIT:
        abstract = abstract[:ABSTRACT_CHAR_LIMIT].rsplit(" ", 1)[0] + "..."
    return {
        "title": record.get("title", "").strip(),
        "doi": doi,
        "journal": record.get("journalInfo", {}).get("journal", {}).get("title", ""),
        "date": record.get("firstPublicationDate", ""),
        "abstract": abstract,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", required=True, help="YYYY-MM-DD, inclusive")
    parser.add_argument("--until", required=True, help="YYYY-MM-DD, inclusive")
    parser.add_argument("--out", help="write JSON to this file instead of stdout")
    parser.add_argument("--exclude-dois", default="", help="comma-separated DOIs to drop (already seen)")
    args = parser.parse_args()

    exclude = {d.strip() for d in args.exclude_dois.split(",") if d.strip()}
    query = build_query(args.since, args.until)
    results = []
    cursor_mark = "*"
    seen_dois = set()

    while True:
        page = fetch_page(query, cursor_mark)
        hits = page.get("resultList", {}).get("result", [])
        for record in hits:
            item = extract(record)
            if item and item["doi"] not in seen_dois:
                seen_dois.add(item["doi"])
                results.append(item)

        next_cursor = page.get("nextCursorMark")
        if not next_cursor or next_cursor == cursor_mark or not hits:
            break
        cursor_mark = next_cursor

    if exclude:
        results = [r for r in results if r["doi"] not in exclude]

    if args.out:
        with open(args.out, "w") as f:
            json.dump(results, f, indent=None)
        print(f"wrote {len(results)} candidates to {args.out}")
    else:
        json.dump(results, sys.stdout, indent=None)

if __name__ == "__main__":
    main()
