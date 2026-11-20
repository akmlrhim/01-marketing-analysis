# -*- coding: utf-8 -*-
"""Cek topik AI/GEO dsb dengan word boundary (hindari false positive kata Indonesia)."""
import io
import sys
import os
import glob
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

files = glob.glob("research/*.md") + glob.glob("research/data/*.csv")
patterns = {
    "AI": re.compile(r"\bAI\b"),
    "artificial/kecerdasan artifisial": re.compile(r"artificial|kecerdasan artifisial", re.IGNORECASE),
    "GEO (generative engine optimization)": re.compile(r"\bGEO\b|generative engine", re.IGNORECASE),
    "generative/LLM/ChatGPT": re.compile(r"generative|LLM|ChatGPT", re.IGNORECASE),
    "otomasi/automation": re.compile(r"otomasi|automation", re.IGNORECASE),
    "chatbot/WhatsApp API": re.compile(r"chatbot|WhatsApp API|WAB A", re.IGNORECASE),
}
for label, pat in patterns.items():
    hits = []
    for f in files:
        n = len(pat.findall(open(f, encoding="utf-8").read()))
        if n:
            hits.append(f"{os.path.basename(f)}({n})")
    print(f"{label}: {', '.join(hits) if hits else 'TIDAK ADA'}")
