# -*- coding: utf-8 -*-
"""Cek relevansi topik: bandingkan isi riset dengan isu industri 2025-2026."""
import io
import sys
import os
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import pandas as pd

pp = pd.read_csv("research/data/pain-point.csv")
print("=== 53 PAIN POINT (per segmen) ===")
for seg, g in pp.groupby("segmen"):
    print(f"--- {seg} ({len(g)}) ---")
    print("; ".join(g["pain_point"].tolist()))

print()
print("=== cek topik 2025-2026 di seluruh riset ===")
kws = ["AI", "GEO", "generatif", "ChatGPT", "live shopping", "live commerce",
       "creator", "KOL", "retail media", "first-party", "privasi", "UGC"]
files = glob.glob("research/*.md") + glob.glob("research/data/*.csv")
for kw in kws:
    hits = []
    for f in files:
        n = open(f, encoding="utf-8").read().lower().count(kw.lower())
        if n:
            hits.append(f"{os.path.basename(f)}({n})")
    print(f"{kw}: {', '.join(hits) if hits else 'TIDAK ADA'}")
