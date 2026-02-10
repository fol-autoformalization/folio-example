#!/usr/bin/env python3
import json
import os
import shutil
import tempfile
import urllib.request
import zipfile
from collections import Counter
import io

import pandas as pd


ORIGINAL_ZIP = "2024.emnlp-main.1229.data.zip"
ORIGINAL_URL = "https://aclanthology.org/attachments/2024.emnlp-main.1229.data.zip"
FIXED_ZIP = "2024.emnlp-main.1229.data.fixed.zip"
JSONL_PATHS = [
    "FOLIO/folio_train.jsonl",
    "FOLIO/folio_validation.jsonl",
    "FOLIO/folio_test.jsonl",
]


def ensure_original_zip_present():
    if os.path.exists(ORIGINAL_ZIP):
        return

    print(f"downloading_original_zip: {ORIGINAL_URL}")
    with urllib.request.urlopen(ORIGINAL_URL) as r:
        zip_data = r.read()

    with zipfile.ZipFile(io.BytesIO(zip_data), "r") as z:
        for p in JSONL_PATHS:
            z.getinfo(p)

    with open(ORIGINAL_ZIP, "wb") as f:
        f.write(zip_data)


def iter_formulas(zip_path: str, jsonl_paths: list[str]):
    with zipfile.ZipFile(zip_path, "r") as z:
        for jsonl_path in jsonl_paths:
            with z.open(jsonl_path) as f:
                for raw in f:
                    if not raw.strip():
                        continue
                    ex = json.loads(raw.decode("utf-8"))
                    prem = ex["premises-FOL"]
                    if isinstance(prem, str):
                        for p in [p.strip() for p in prem.split("\n") if p.strip()]:
                            yield p
                    else:
                        for p in prem:
                            yield p
                    yield ex["conclusion-FOL"]


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def main():
    ensure_original_zip_present()

    rows = []
    for a, b in zip(iter_formulas(ORIGINAL_ZIP, JSONL_PATHS), iter_formulas(FIXED_ZIP, JSONL_PATHS)):
        rows.append((a, b))

    df = pd.DataFrame(rows, columns=["a", "b"])
    df["d"] = [levenshtein(a, b) for a, b in rows]

    print(f"total_formulas: {len(df)}")
    print(f"changed_formulas: {(df['d'] != 0).sum()}")

    u = df.loc[df["d"] != 0, ["a", "b", "d"]].drop_duplicates(subset=["a", "b"])
    print(f"unique_changed_formulas: {len(u)}")
    for d, c in u["d"].value_counts().sort_index().items():
        print(f"{int(d)} {int(c)}")


if __name__ == "__main__":
    main()
