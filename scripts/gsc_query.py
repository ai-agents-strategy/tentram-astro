#!/usr/bin/env python3
"""
Google Search Console query tool for tentram-id (tentram.id).

Uses the platform's shared service account (~/.hermes/google_service_account.json).
That service account must be added as a user (Restricted is enough) on the
target property in Search Console before this will return data:
  Search Console -> Settings -> Users and permissions -> Add user

Usage:
  gsc_query.py --list-sites
  gsc_query.py --dimensions query --days 7
  gsc_query.py --dimensions page,query --days 28 --row-limit 20
  gsc_query.py --dimensions date --start 2026-07-01 --end 2026-07-29
  gsc_query.py --summary --days 7
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = Path("/root/.hermes/google_service_account.json")
DEFAULT_PROPERTY = "https://tentram.id/"


def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    return build("webmasters", "v3", credentials=credentials)


def list_sites(service):
    sites = service.sites().list().execute().get("siteEntry", [])
    if not sites:
        print("No sites visible to this service account.")
        return
    print("Sites this service account can access:")
    for s in sites:
        print(f"  - {s['siteUrl']}  (permission: {s['permissionLevel']})")


def query(service, site_url, start, end, dimensions, row_limit):
    body = {
        "startDate": start.strftime("%Y-%m-%d"),
        "endDate": end.strftime("%Y-%m-%d"),
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    return service.searchanalytics().query(siteUrl=site_url, body=body).execute()


def print_table(resp, dimensions):
    rows = resp.get("rows", [])
    if not rows:
        print("No data for this range.")
        return
    header = dimensions + ["clicks", "impressions", "ctr", "position"]
    print(" | ".join(header))
    print(" | ".join("---" for _ in header))
    for row in rows:
        keys = row["keys"]
        ctr = f"{row['ctr'] * 100:.1f}%"
        position = f"{row['position']:.1f}"
        print(" | ".join([*keys, str(row["clicks"]), str(row["impressions"]), ctr, position]))


def print_summary(service, site_url, start, end):
    resp = query(service, site_url, start, end, [], 1)
    rows = resp.get("rows", [])
    if not rows:
        print("No summary data for this range.")
        return
    row = rows[0]
    print(f"Range: {start:%Y-%m-%d} to {end:%Y-%m-%d}")
    print(f"Total clicks:      {row['clicks']:,}")
    print(f"Total impressions: {row['impressions']:,}")
    print(f"Average CTR:       {row['ctr'] * 100:.1f}%")
    print(f"Average position:  {row['position']:.1f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--site", default=DEFAULT_PROPERTY, help="GSC property (default: %(default)s)")
    p.add_argument("--dimensions", default="query", help="Comma-separated: query,page,date,country,device")
    p.add_argument("--days", type=int, default=7, help="Look back N days (ignored if --start/--end given)")
    p.add_argument("--start", help="YYYY-MM-DD")
    p.add_argument("--end", help="YYYY-MM-DD")
    p.add_argument("--row-limit", type=int, default=10)
    p.add_argument("--summary", action="store_true", help="Print totals instead of a per-dimension table")
    p.add_argument("--list-sites", action="store_true", help="List sites this service account can access, then exit")
    args = p.parse_args()

    if not SERVICE_ACCOUNT_FILE.exists():
        sys.exit(f"Missing service account file: {SERVICE_ACCOUNT_FILE}")

    service = get_service()

    if args.list_sites:
        list_sites(service)
        return

    if args.end:
        end = datetime.strptime(args.end, "%Y-%m-%d")
    else:
        end = datetime.now() - timedelta(days=1)
    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d")
    else:
        start = end - timedelta(days=args.days)

    if args.summary:
        print_summary(service, args.site, start, end)
        return

    dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    resp = query(service, args.site, start, end, dimensions, args.row_limit)
    print_table(resp, dimensions)


if __name__ == "__main__":
    main()
