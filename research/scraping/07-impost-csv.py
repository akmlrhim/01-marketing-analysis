# -*- coding: utf-8 -*-
"""Tulis ulang impost-layanan.csv dengan quoting yang benar (csv.writer)."""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).resolve().parents[1] / "data" / "impost-layanan.csv"

ROWS = [
    {
        "layanan": "Content & Social Media Management",
        "kategori": "Konten & Sosmed",
        "layanan_terkait": "SMM / Konten",
        "harga_pasar_min_rp": 2500000,
        "harga_pasar_max_rp": 15000000,
        "satuan_pasar": "per bulan",
        "sumber_harga_pasar": (
            "SMM retainer Indonesia 2-4 platform 12-20 konten (biaya-iklan.csv); "
            "WebNesia Rp2,1 jt promo (S35); freelance Fastwork/Sribu mulai Rp99-250 rb (S37)"
        ),
        "harga_ideal_min_rp": 3000000,
        "harga_ideal_max_rp": 8000000,
        "satuan_ideal": "per bulan",
        "dasar_harga_ideal": (
            "Jangkar paket internal: Ignite Rp2,5 jt (1 platform) sampai Growth "
            "Rp6,5 jt (2 platform + ads management); pasar Kalsel Rp2,5-15 jt"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Performance Marketing (Ads)",
        "kategori": "Iklan & Performance",
        "layanan_terkait": "Ads / Performance",
        "harga_pasar_min_rp": 1500000,
        "harga_pasar_max_rp": 6000000,
        "satuan_pasar": "per bulan",
        "sumber_harga_pasar": (
            "Fee manajemen iklan pasar Indonesia 10-20% dari spend; CPL Rp20-80 rb "
            "dan CPC Rp1,5-15 rb (biaya-iklan.csv); internasional US$500-5.000/bln"
        ),
        "harga_ideal_min_rp": 2500000,
        "harga_ideal_max_rp": 6000000,
        "satuan_ideal": "per bulan",
        "dasar_harga_ideal": (
            "Fee flat (spend ditagih terpisah); kompetitor lokal mulai Rp500 rb "
            "(corefreelancers) sehingga hindari posisi termurah; jangkar paket Growth Rp6,5 jt"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Branding & Growth System",
        "kategori": "Branding",
        "layanan_terkait": "Branding",
        "harga_pasar_min_rp": 8000000,
        "harga_pasar_max_rp": 25000000,
        "satuan_pasar": "per proyek",
        "sumber_harga_pasar": (
            "Brand identity pasar Rp8-25 jt (layanan-addon.csv); sinyal etnicode Rp10-50 jt"
        ),
        "harga_ideal_min_rp": 10000000,
        "harga_ideal_max_rp": 25000000,
        "satuan_ideal": "per proyek",
        "dasar_harga_ideal": (
            "Posisi menengah-atas; diferensiasi pada sistem growth (roadmap + review "
            "kuartalan) bukan sekadar visual"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Marketplace Optimization",
        "kategori": "E-commerce",
        "layanan_terkait": "Marketplace",
        "harga_pasar_min_rp": 1500000,
        "harga_pasar_max_rp": 5000000,
        "satuan_pasar": "per bulan",
        "sumber_harga_pasar": (
            "Sinyal pasar terbatas: freelance optimasi mulai Rp99 rb (Sribu); "
            "retainer agency disetarakan dengan konten + operasional toko"
        ),
        "harga_ideal_min_rp": 2000000,
        "harga_ideal_max_rp": 5000000,
        "satuan_ideal": "per bulan",
        "dasar_harga_ideal": (
            "Per toko: konten produk + promo + kelola ulasan; benchmark belum banyak "
            "di Kalimantan sehingga mengikuti struktur retainer SMM"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Live Stream",
        "kategori": "Konten & Sosmed",
        "layanan_terkait": "Video / Foto",
        "harga_pasar_min_rp": 1500000,
        "harga_pasar_max_rp": 6000000,
        "satuan_pasar": "per event",
        "sumber_harga_pasar": (
            "Paket live 1 kamera pasar Jakarta Rp5 jt (Kreasi Ukasah, S39); "
            "produksi video Rp0,5-3 jt per konten"
        ),
        "harga_ideal_min_rp": 2000000,
        "harga_ideal_max_rp": 6000000,
        "satuan_ideal": "per event",
        "dasar_harga_ideal": (
            "Per event 3-4 jam 1 kamera; multi-kamera dan multi-platform menaikkan harga"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "App Development & Website",
        "kategori": "Teknologi",
        "layanan_terkait": "Website; Software / App",
        "harga_pasar_min_rp": 980000,
        "harga_pasar_max_rp": 40000000,
        "satuan_pasar": "per proyek",
        "sumber_harga_pasar": (
            "Landing page mulai Rp980 rb (publish.co.id); rentang pasar website "
            "Indonesia Rp800 rb-40 jt, company profile Rp1-20 jt (Iniwebsitemu, S40)"
        ),
        "harga_ideal_min_rp": 8000000,
        "harga_ideal_max_rp": 35000000,
        "satuan_ideal": "per proyek",
        "dasar_harga_ideal": (
            "Website company profile/UMKM Rp8-35 jt; aplikasi custom Rp25-80 jt "
            "dihitung terpisah; hindari segmen di bawah Rp1 jt karena perang harga "
            "(websitemurah/jasamurahweb)"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Customer Service",
        "kategori": "Operasional",
        "layanan_terkait": "CRM / Lead",
        "harga_pasar_min_rp": 3000000,
        "harga_pasar_max_rp": 6000000,
        "satuan_pasar": "per bulan per agen",
        "sumber_harga_pasar": (
            "Setara UMK Banjarmasin Rp3,49 jt + overhead; benchmark global "
            "US$8-35 per jam (EverHelp, S38)"
        ),
        "harga_ideal_min_rp": 3500000,
        "harga_ideal_max_rp": 5000000,
        "satuan_ideal": "per bulan per agen",
        "dasar_harga_ideal": (
            "1 agen remote dengan SLA jam kerja tetap; menempel pada paket CRM sebagai bundel"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "CRM Sales Pipeline & CS AI",
        "kategori": "Operasional",
        "layanan_terkait": "CRM / Lead",
        "harga_pasar_min_rp": 5000000,
        "harga_pasar_max_rp": 15000000,
        "satuan_pasar": "per proyek",
        "sumber_harga_pasar": "Setup CRM pasar menengah: template + integrasi WhatsApp",
        "harga_ideal_min_rp": 5000000,
        "harga_ideal_max_rp": 15000000,
        "satuan_ideal": "per proyek",
        "dasar_harga_ideal": (
            "Setup + training sekali bayar; retainer pemeliharaan Rp1,5-4 jt per bulan; "
            "komponen AI auto-reply menaikkan 20-30%"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Brand Foundation Guideline & Logo",
        "kategori": "Branding",
        "layanan_terkait": "Branding",
        "harga_pasar_min_rp": 8000000,
        "harga_pasar_max_rp": 25000000,
        "satuan_pasar": "per proyek",
        "sumber_harga_pasar": (
            "Brand identity pasar Rp8-25 jt (layanan-addon.csv); freelance logo mulai "
            "Rp60-99 rb (Fastwork/Sribu, S37) = bawah pasar"
        ),
        "harga_ideal_min_rp": 8000000,
        "harga_ideal_max_rp": 20000000,
        "satuan_ideal": "per proyek",
        "dasar_harga_ideal": (
            "Logo + fondasi merek + guideline 20-40 halaman; bundling dengan Branding "
            "& Growth System memberi diskon paket"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Foto Produk Katalog & Dokumentasi Event",
        "kategori": "Konten & Sosmed",
        "layanan_terkait": "Video / Foto",
        "harga_pasar_min_rp": 500000,
        "harga_pasar_max_rp": 8000000,
        "satuan_pasar": "per sesi/proyek",
        "sumber_harga_pasar": (
            "Per foto Rp50-250 rb; paket katalog 50-100 foto Rp3-8 jt (Depotkamera, S36); "
            "studio Rp149 rb per foto (Tapstudio)"
        ),
        "harga_ideal_min_rp": 1500000,
        "harga_ideal_max_rp": 4000000,
        "satuan_ideal": "per sesi",
        "dasar_harga_ideal": (
            "Per sesi 3-5 jam atau per event; paket 2 sesi per bulan sudah termasuk "
            "dalam paket Growth"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
    {
        "layanan": "Forecasting & Growth",
        "kategori": "Data & Strategi",
        "layanan_terkait": "Data / Analytics; Training / Consult",
        "harga_pasar_min_rp": 3000000,
        "harga_pasar_max_rp": 10000000,
        "satuan_pasar": "per bulan",
        "sumber_harga_pasar": "Retainer konsultan strategi pasar menengah Indonesia",
        "harga_ideal_min_rp": 3000000,
        "harga_ideal_max_rp": 8000000,
        "satuan_ideal": "per bulan",
        "dasar_harga_ideal": (
            "Audit + forecast kuartalan + dashboard; diferensiator B2B; dijual mulai "
            "paket Market Leader ke atas"
        ),
        "status_harga_ideal": "Hipotesis (usulan analis)",
    },
]

with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys()))
    w.writeheader()
    w.writerows(ROWS)

print(f"{len(ROWS)} baris -> {OUT}")

# verifikasi: baca balik
import pandas as pd

df = pd.read_csv(OUT)
assert df["layanan"].tolist() == [r["layanan"] for r in ROWS], "kolom layanan bergeser!"
print("Verifikasi kolom layanan: OK")
print(df[["layanan", "harga_pasar_min_rp", "harga_ideal_min_rp"]].to_string(index=False))
