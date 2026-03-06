"""Download sample prescription-like entries from OpenFDA and save locally.

This is a helper script to fetch sample drug label data and serialize it as a
simple list of prescription texts in `data/prescriptions.json`.

Usage:
    python scripts/download_prescriptions.py --count 100
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"


def _fetch_labels(limit: int, skip: int = 0) -> list[dict]:
    params = {"limit": limit, "skip": skip}
    resp = requests.get(OPENFDA_LABEL_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("results", [])


def _format_label(label: dict) -> str:
    # Compose a simple prescription-like text from select fields.
    parts: list[str] = []
    if (brand := label.get("openfda", {}).get("brand_name")):
        parts.append(f"Brand name: {brand}")
    if (generic := label.get("openfda", {}).get("generic_name")):
        parts.append(f"Generic name: {generic}")

    if (purpose := label.get("purpose")):
        parts.append(f"Purpose: {purpose}")
    if (indications := label.get("indications_and_usage")):
        parts.append(f"Indications: {indications}")
    if (dosage := label.get("dosage_and_administration")):
        parts.append(f"Dosage: {dosage}")
    if (warnings := label.get("warnings")):
        parts.append(f"Warnings: {warnings}")

    return "\n\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download sample prescription data from OpenFDA.")
    parser.add_argument("--count", type=int, default=100, help="Number of prescription entries to download.")
    parser.add_argument("--out", type=str, default="data/prescriptions.json", help="Output JSON file path.")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    chunk = 50
    items: list[str] = []
    for skip in range(0, args.count, chunk):
        to_fetch = min(chunk, args.count - skip)
        print(f"Fetching {to_fetch} prescriptions (skip={skip})...")
        labels = _fetch_labels(to_fetch, skip=skip)
        for label in labels:
            items.append(_format_label(label))

    out_path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    print(f"Saved {len(items)} prescriptions to {out_path}")


if __name__ == "__main__":
    main()
