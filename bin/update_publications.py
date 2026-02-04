#!/usr/bin/env python3
import json
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ARXIV_LIST = Path("_data/publications_arxiv.txt")
OUT_YML = Path("_data/publications.yml")

INSPIRE_ARXIV_ENDPOINT = "https://inspirehep.net/api/arxiv/{}"

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "strong-action-publications-updater/1.2"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def normalize_arxiv_id(s: str) -> str:
    s = s.strip()
    s = s.replace("arXiv:", "")
    s = s.replace("https://arxiv.org/abs/", "")
    s = s.replace("http://arxiv.org/abs/", "")
    return s.strip()

def _fmt_journal(pubinfo: dict) -> str:
    """
    Try to format INSPIRE publication_info entry as:
    'JournalTitle Volume (Year) ArtID or PageStart-PageEnd'
    """
    if not isinstance(pubinfo, dict):
        return ""

    title = (pubinfo.get("journal_title") or pubinfo.get("journal") or "").strip()
    volume = str(pubinfo.get("journal_volume") or pubinfo.get("volume") or "").strip()
    year = str(pubinfo.get("year") or "").strip()

    artid = str(pubinfo.get("artid") or pubinfo.get("article_id") or "").strip()
    page_start = str(pubinfo.get("page_start") or "").strip()
    page_end = str(pubinfo.get("page_end") or "").strip()

    tail = ""
    if artid:
        tail = artid
    elif page_start and page_end:
        tail = f"{page_start}-{page_end}"
    elif page_start:
        tail = page_start

    parts = []
    if title:
        parts.append(title)
    if volume:
        parts.append(volume)
    if year:
        parts.append(f"({year})")
    if tail:
        parts.append(tail)

    return " ".join(parts).strip()

def parse_inspire_record(arxiv_id: str) -> dict:
    data = fetch_json(INSPIRE_ARXIV_ENDPOINT.format(arxiv_id))
    meta = data.get("metadata", {}) or {}

    # Title
    title = ""
    titles = meta.get("titles") or []
    if titles and isinstance(titles, list):
        title = (titles[0] or {}).get("title", "") or ""
    title = " ".join(title.split()).strip()

    # Authors
    authors_list = meta.get("authors") or []
    authors = []
    for a in authors_list:
        if not isinstance(a, dict):
            continue
        name = a.get("full_name") or a.get("display_name") or ""
        name = " ".join(str(name).split()).strip()
        if name:
            authors.append(name)
    authors_str = ", ".join(authors)

    # Date
    date_iso = meta.get("preprint_date") or meta.get("date_published") or meta.get("earliest_date") or ""
    if not date_iso:
        imprints = meta.get("imprints") or []
        if imprints and isinstance(imprints, list):
            date_iso = (imprints[0] or {}).get("date", "") or ""
    date_iso = str(date_iso)

    dt = None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            dt = datetime.strptime(date_iso, fmt)
            break
        except Exception:
            continue

    if dt is None:
        m = re.match(r"^(\d{2})(\d{2})\.\d+", arxiv_id)
        if m:
            yy = int(m.group(1))
            mm = int(m.group(2))
            year = 2000 + yy
            mm = min(max(mm, 1), 12)
            dt = datetime(year, mm, 1)
        else:
            dt = datetime(1900, 1, 1)

    date_str = f"{dt.day:02d} {MONTHS[dt.month-1]} {dt.year}" if dt.year >= 1901 else ""

    # DOI
    doi = ""
    dois = meta.get("dois") or []
    if isinstance(dois, list) and dois:
        first = dois[0] or {}
        if isinstance(first, dict):
            doi = (first.get("value") or "").strip()

    # INSPIRE literature page
    inspire_url = ""
    control_number = meta.get("control_number")
    if isinstance(control_number, int):
        inspire_url = f"https://inspirehep.net/literature/{control_number}"

    # Journal reference from publication_info (best-effort)
    journal = ""
    pubinfo_list = meta.get("publication_info") or []
    if isinstance(pubinfo_list, list) and pubinfo_list:
        # sometimes multiple entries; pick the first non-empty formatted one
        for pi in pubinfo_list:
            journal = _fmt_journal(pi)
            if journal:
                break
    # fallback: pubinfo_freetext if present
    if not journal:
        ft = (meta.get("pubinfo_freetext") or "").strip()
        journal = ft

    return {
        "title": title,
        "date": date_str,
        "year": dt.year if dt.year >= 1901 else 1900,
        "arxiv": arxiv_id,
        "authors": authors_str,
        "doi": doi,
        "inspire": inspire_url,
        "journal": journal,
    }

def dump_yaml_grouped(blocks) -> str:
    lines = []
    for year in sorted(blocks.keys(), reverse=True):
        papers = blocks[year]
        lines.append(f"- year: {year}")
        lines.append("  papers:")
        for p in papers:
            def q(s: str) -> str:
                return str(s).replace('"', '\\"')

            lines.append(f'    - title: "{q(p.get("title",""))}"')
            lines.append(f'      date: "{q(p.get("date",""))}"')
            lines.append(f'      arxiv: "{q(p.get("arxiv",""))}"')
            lines.append(f'      authors: "{q(p.get("authors",""))}"')

            if p.get("journal"):
                lines.append(f'      journal: "{q(p["journal"])}"')
            if p.get("doi"):
                lines.append(f'      doi: "{q(p["doi"])}"')
            if p.get("inspire"):
                lines.append(f'      inspire: "{q(p["inspire"])}"')

        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def main() -> int:
    if not ARXIV_LIST.exists():
        print(f"Missing {ARXIV_LIST}. Create it with one arXiv ID per line.", file=sys.stderr)
        return 2

    arxiv_ids = []
    for raw in ARXIV_LIST.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        arxiv_ids.append(normalize_arxiv_id(raw))

    if not arxiv_ids:
        print("No arXiv IDs found in _data/publications_arxiv.txt", file=sys.stderr)
        return 2

    blocks = defaultdict(list)
    errors = 0

    for aid in arxiv_ids:
        try:
            rec = parse_inspire_record(aid)
            blocks[rec["year"]].append(rec)
        except Exception as e:
            errors += 1
            print(f"[ERROR] {aid}: {e}", file=sys.stderr)

    def date_key(p):
        try:
            return datetime.strptime(p["date"], "%d %b %Y")
        except Exception:
            return datetime(1900, 1, 1)

    for y in list(blocks.keys()):
        blocks[y].sort(key=date_key, reverse=True)

    OUT_YML.write_text(dump_yaml_grouped(blocks), encoding="utf-8")

    print(f"Wrote {OUT_YML} from {len(arxiv_ids)} arXiv IDs ({errors} errors).")
    return 0 if errors == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
