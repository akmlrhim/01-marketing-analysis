# -*- coding: utf-8 -*-
"""Audit konsistensi internal: hitung ulang klaim README/KNOWLEDGE dari CSV mentah."""
import pandas as pd
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

D = "research/data"
ok = []
warn = []
fail = []

def check(label, cond, detail=""):
    (ok if cond else fail).append(f"{label} {'OK' if cond else 'GAGAL'} {detail}")
    print(f"[{'OK  ' if cond else 'GAGAL'}] {label} {detail}")

# ---------- jumlah baris per dataset ----------
claims = {
    "makro-kalimantan.csv": 5, "kota-kalimantan.csv": 9, "skor-industri.csv": 30,
    "industri-layanan.csv": 30, "kompetitor.csv": 50, "platform-indonesia.csv": 10,
    "ecommerce-indonesia.csv": 6, "biaya-iklan.csv": 14, "channel-matrix.csv": 30,
    "pain-point.csv": 53, "persepsi.csv": 14, "layanan-winning.csv": 5,
    "impost-layanan.csv": 11, "sumber.csv": 40,
}
print("== Jumlah baris vs klaim README ==")
for f, exp in claims.items():
    df = pd.read_csv(f"{D}/{f}")
    check(f, len(df) == exp, f"(aktual {len(df)}, klaim {exp})")

# ---------- kompetitor ----------
print("\n== Kompetitor ==")
k = pd.read_csv(f"{D}/kompetitor.csv")
print("Kolom:", list(k.columns))
for col in ["status_verifikasi", "jenis_lokasi", "tipe", "lokasi", "cakupan"]:
    if col in k.columns:
        print(f"- {col}:", k[col].value_counts().to_dict())

if "status_verifikasi" in k.columns:
    vc = k["status_verifikasi"].value_counts()
    check("Terverifikasi=26", vc.get("Terverifikasi", 0) == 26, f"(aktual {vc.get('Terverifikasi',0)})")
    check("Profil publik=19", vc.get("Profil publik", 0) == 19, f"(aktual {vc.get('Profil publik',0)})")
    check("Perlu verifikasi=5", vc.get("Perlu verifikasi", 0) == 5, f"(aktual {vc.get('Perlu verifikasi',0)})")

# lokal 38 / nasional 12
for col in k.columns:
    if k[col].nunique() <= 5 and k[col].astype(str).str.contains("asional|okal", case=False).any():
        print(f"- {col}:", k[col].value_counts().to_dict())

# bukti lokasi terisi
for col in ["lokasi_terverifikasi", "bukti_lokasi"]:
    if col in k.columns:
        n = k[col].notna().sum()
        check(f"{col} terisi semua", n == len(k), f"({n}/{len(k)})")

# ---------- skor industri: hitung ulang ----------
print("\n== Skor industri (hitung ulang SAW) ==")
s = pd.read_csv(f"{D}/skor-industri.csv")
w = {"ukuran_pasar": .20, "pertumbuhan": .20, "belanja_digital": .20,
     "kompetisi_rendah": .15, "akses_dan_sales_cycle": .15, "margin_retainer": .10}
cols = [c for c in w if c in s.columns]
if len(cols) == 6:
    re_calc = sum(s[c] * v for c, v in w.items()).round(2)
    if "skor_tertimbang" in s.columns:
        diff = (s["skor_tertimbang"].round(2) - re_calc).abs()
        check("skor_tertimbang = rumus bobot", diff.max() < 0.01, f"(max diff {diff.max()})")
else:
    print("Kolom skor mentah:", list(s.columns))

# ---------- pain point & persepsi ----------
p = pd.read_csv(f"{D}/pain-point.csv")
pc = [c for c in p.columns if c in ("frekuensi", "dampak", "kesiapan_bayar")]
if len(pc) == 3:
    p["calc"] = (0.4 * p["frekuensi"] + 0.4 * p["dampak"] + 0.2 * p["kesiapan_bayar"]).round(2)
    if "skor_prioritas" in p.columns:
        diff = (p["skor_prioritas"].round(2) - p["calc"]).abs()
        check("skor_prioritas pain = 0.4/0.4/0.2", diff.max() < 0.01, f"(max diff {diff.max()})")

pr = pd.read_csv(f"{D}/persepsi.csv")
if {"kepentingan", "kinerja_agency"}.issubset(pr.columns):
    pr["gap_calc"] = (pr["kepentingan"] - pr["kinerja_agency"]).round(1)
    if "gap" in pr.columns:
        diff = (pr["gap"] - pr["gap_calc"]).abs()
        check("gap persepsi = kepentingan - kinerja", diff.max() < 0.01, f"(max diff {diff.max()})")
    top = pr.loc[pr["gap_calc"].idxmax()]
    check("Gap terbesar = Akuntabilitas KPI (2.4)", "kpi" in str(top.values).lower() or top["gap_calc"] == 2.4,
          f"(top gap {top['gap_calc']})")

# ---------- kota: UMK Tarakan 4.74 jt ----------
print("\n== Kota ==")
kt = pd.read_csv(f"{D}/kota-kalimantan.csv")
print(kt.to_string(max_cols=12))

# ---------- makro ----------
print("\n== Makro ==")
mk = pd.read_csv(f"{D}/makro-kalimantan.csv")
print(mk.to_string(max_cols=14))

# ---------- derived vs raw ----------
print("\n== Derived metrics.json ==")
m = json.load(open("dashboard/data/derived/metrics.json", encoding="utf-8"))
print(json.dumps(m, indent=1, ensure_ascii=False)[:3000])
