"""Pipeline analisis data riset pasar Kalimantan.

Jalankan langsung:
    python dashboard/analysis.py

Output:
    dashboard/data/derived/*.csv
    dashboard/data/derived/metrics.json
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "research" / "data"
OUT_DIR = Path(__file__).resolve().parent / "data" / "derived"

NATIONAL_INTERNET = 80.66  # APJII 2025, %
NATIONAL_SOCIAL_USERS = 180.0  # juta identitas, DataReportal Digital 2026

INDUSTRY_WEIGHTS = {
    "ukuran_pasar": 0.20,
    "pertumbuhan": 0.20,
    "belanja_digital": 0.20,
    "kompetisi_rendah": 0.15,
    "akses_dan_sales_cycle": 0.15,
    "margin_retainer": 0.10,
}

SERVICE_RULES = {
    "SMM / Konten": r"smm|social media|konten|content",
    "Ads / Performance": r"ads|iklan|performance|sem\b|paid",
    "Website": r"web|landing",
    "Branding": r"brand",
    "Video / Foto": r"video|foto|photo",
    "SEO": r"seo",
    "CRM / Lead": r"crm|lead",
    "Software / App": r"software|mobile app|aplikasi",
    "KOL / Influencer": r"kol|influencer",
    "Marketplace": r"marketplace|e-commerce|ecommerce",
    "Cyber Security": r"cyber|security",
    "PR / Event": r"pr\b|event|public relations",
    "Training / Consult": r"training|konsultasi|consult",
    "No-code / Hosting": r"no-code|nocode|hosting",
    "Data / Analytics": r"analytics|analitik|data",
}

REQUIRED = {
    "makro-kalimantan.csv": [
        "provinsi",
        "pertumbuhan_2024_persen",
        "pertumbuhan_2025_persen",
        "penetrasi_internet_2025_persen",
    ],
    "kota-kalimantan.csv": [
        "kota",
        "provinsi",
        "penduduk",
        "umk_rp",
        "lat",
        "lon",
    ],
    "skor-industri.csv": [
        "industri",
        *INDUSTRY_WEIGHTS.keys(),
    ],
    "kompetitor.csv": [
        "nama",
        "basis_kota",
        "tipe",
        "layanan_utama",
        "sinyal_harga",
    ],
    "industri-layanan.csv": ["industri", "layanan_inti"],
    "platform-indonesia.csv": [
        "platform",
        "jangkauan_iklan_juta",
        "persen_populasi",
    ],
    "ecommerce-indonesia.csv": [
        "platform",
        "jenis",
        "mau_juta",
        "gmv_2025_usd_miliar",
    ],
    "biaya-iklan.csv": [
        "kanal",
        "objective",
        "metrik",
        "batas_bawah_rp",
        "batas_atas_rp",
    ],
    "pain-point.csv": [
        "segmen",
        "pain_point",
        "frekuensi",
        "dampak",
        "kesiapan_bayar",
    ],
    "persepsi.csv": ["dimensi", "kepentingan", "kinerja_agency"],
    "layanan-winning.csv": [
        "tier",
        "target",
        "harga_min_rp",
        "harga_max_rp",
        "satuan",
    ],
    "layanan-industri.csv": [
        "paket",
        "industri",
        "harga_min_rp",
        "harga_max_rp",
        "satuan",
    ],
    "layanan-addon.csv": ["layanan", "harga_min_rp", "harga_max_rp", "satuan"],
    "impost-layanan.csv": [
        "layanan",
        "kategori",
        "layanan_terkait",
        "harga_pasar_min_rp",
        "harga_pasar_max_rp",
        "satuan_pasar",
        "harga_ideal_min_rp",
        "harga_ideal_max_rp",
        "satuan_ideal",
    ],
    "channel-matrix.csv": ["industri"],
    "sumber.csv": ["id", "topik", "sumber", "url"],
}

WILAYAH_DEMAND = ["Kalsel", "Kalimantan", "Nasional"]


def _read(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Data tidak ditemukan: {path}")
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    missing = set(REQUIRED.get(filename, [])) - set(df.columns)
    if missing:
        raise ValueError(f"{filename} kehilangan kolom: {sorted(missing)}")
    return df


def _numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df


def clean_macro(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["provinsi"] = df["provinsi"].astype(str).str.strip()
    df = _numeric(
        df,
        [
            "pertumbuhan_2024_persen",
            "pertumbuhan_2025_persen",
            "pdrb_2024_triliun_rp",
            "umkm_unit",
            "penetrasi_internet_2025_persen",
            "penduduk_2025",
            "ump_2025_rp",
            "ipm_2025",
            "jumlah_kota",
        ],
    )
    df["pertumbuhan_terbaru"] = df["pertumbuhan_2025_persen"].fillna(
        df["pertumbuhan_2024_persen"]
    )
    df["tahun_pertumbuhan"] = np.where(
        df["pertumbuhan_2025_persen"].notna(), "2025", "2024"
    )
    df["gap_internet_vs_nasional"] = (
        df["penetrasi_internet_2025_persen"] - NATIONAL_INTERNET
    ).round(2)
    df["kelas_penetrasi"] = pd.cut(
        df["penetrasi_internet_2025_persen"],
        bins=[-1, 75, 85, 100],
        labels=["Menengah-rendah", "Menengah", "Tinggi"],
    )
    df["ump_juta"] = (df["ump_2025_rp"] / 1_000_000).round(2)
    return df


def clean_cities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["kota", "provinsi", "sektor_utama", "status_data", "catatan"])
    df = _numeric(
        df,
        [
            "penduduk",
            "umk_rp",
            "umkm_unit",
            "internet_provinsi_persen",
            "lat",
            "lon",
        ],
    )
    df["umk_juta"] = (df["umk_rp"] / 1_000_000).round(2)
    df["umkm_per_1000_penduduk"] = (
        df["umkm_unit"] / df["penduduk"] * 1000
    ).round(1)
    return df.sort_values("penduduk", ascending=False).reset_index(drop=True)


def competitor_supply(df: pd.DataFrame) -> pd.Series:
    """Pasokan layanan tiap kategori, dibobot kekuatan agency.

    Bobot per agency: 1 + 0.5 (terverifikasi) + 0.5 (jumlah layanan / 5).
    """
    strength = (
        1.0
        + 0.5 * (df["status_verifikasi"] == "Terverifikasi").astype(float)
        + 0.5 * (df["jumlah_layanan"].clip(lower=0, upper=5) / 5)
    )
    supply = {}
    for label in SERVICE_RULES:
        supply[label] = float(strength[df[label] == 1].sum())
    return pd.Series(supply, dtype=float)


def measured_competition(
    industri: pd.DataFrame, layanan_map: pd.DataFrame, supply: pd.Series
) -> pd.DataFrame:
    """Skor kompetisi 1-5 dari pasokan layanan. 5 berarti paling sedikit pesaing."""
    df = industri.copy()
    mapping = dict(
        zip(
            layanan_map["industri"],
            layanan_map["layanan_inti"].astype(str),
        )
    )
    top = float(supply.max()) if len(supply) and supply.max() > 0 else 1.0

    coverage = []
    for name in df["industri"]:
        raw = mapping.get(name, "")
        services = [s.strip() for s in raw.split(";") if s.strip()]
        values = [float(supply.get(s, 0.0)) for s in services]
        coverage.append(sum(values) / len(values) / top if values else 0.0)

    df["layanan_inti"] = df["industri"].map(lambda n: mapping.get(n, ""))
    df["cakupan_pesaing"] = pd.Series(coverage).round(3)
    df["kompetisi_terukur"] = (1 + 4 * (1 - df["cakupan_pesaing"])).round(2)

    df["skor_tertimbang_terukur"] = (
        sum(
            df[col].fillna(0) * weight
            for col, weight in INDUSTRY_WEIGHTS.items()
            if col != "kompetisi_rendah"
        )
        + df["kompetisi_terukur"] * INDUSTRY_WEIGHTS["kompetisi_rendah"]
    ).round(2)

    df["peringkat_terukur"] = (
        df["skor_tertimbang_terukur"]
        .rank(ascending=False, method="min")
        .astype(int)
    )
    df["prioritas_terukur"] = pd.cut(
        df["skor_tertimbang_terukur"],
        bins=[0, 3.5, 3.8, 5.0],
        labels=["Potensial", "Prioritas", "Prioritas inti"],
        include_lowest=True,
    )
    df["delta_skor"] = (df["skor_tertimbang_terukur"] - df["skor_tertimbang"]).round(2)
    df["delta_peringkat"] = df["peringkat"] - df["peringkat_terukur"]
    return df


def score_industries(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["industri"] = df["industri"].astype(str).str.strip()
    df = _numeric(df, list(INDUSTRY_WEIGHTS))
    df["skor_file"] = pd.to_numeric(df.get("skor_tertimbang"), errors="coerce")
    df["skor_hitung"] = sum(
        df[col].fillna(0) * weight for col, weight in INDUSTRY_WEIGHTS.items()
    )
    df["skor_tertimbang"] = df["skor_hitung"].round(2)
    df["peringkat"] = (
        df["skor_tertimbang"].rank(ascending=False, method="min").astype(int)
    )
    df["prioritas"] = pd.cut(
        df["skor_tertimbang"],
        bins=[0, 3.5, 3.8, 5.0],
        labels=["Potensial", "Prioritas", "Prioritas inti"],
        include_lowest=True,
    )
    df["selisih_vs_file"] = (df["skor_tertimbang"] - df["skor_file"]).round(2)
    return df.sort_values("skor_tertimbang", ascending=False).reset_index(drop=True)


def _tipe_sederhana(value: str) -> str:
    text = str(value).lower()
    if "internasional" in text:
        return "Internasional"
    if "nasional" in text:
        return "Nasional"
    return "Lokal"


def clean_competitors(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text_cols = [
        "nama",
        "basis_kota",
        "tipe",
        "positioning",
        "layanan_utama",
        "kanal_jual",
        "sinyal_harga",
        "segmen",
        "kekuatan",
        "celah",
        "url",
        "status_verifikasi",
        "sumber",
        "lokasi_terverifikasi",
        "bukti_lokasi",
        "tahun_data",
    ]
    df = _text(df, text_cols)

    df["tipe_sederhana"] = df["tipe"].map(_tipe_sederhana)
    df["kota_utama"] = (
        df["basis_kota"]
        .str.split("/")
        .str[0]
        .str.replace(r"\(.*\)", "", regex=True)
        .str.strip()
    )
    df["harga_transparan"] = df["sinyal_harga"].str.contains(
        r"rp|rb|jt|juta", case=False, regex=True, na=False
    ) & ~df["sinyal_harga"].str.contains(
        r"tidak publik|via wa|gaji", case=False, regex=True, na=False
    )

    for label, pattern in SERVICE_RULES.items():
        df[label] = (
            df["layanan_utama"]
            .str.contains(pattern, case=False, regex=True, na=False)
            .astype(int)
        )
    df["jumlah_layanan"] = df[list(SERVICE_RULES)].sum(axis=1)
    return df


def platform_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["platform", "kategori", "catatan", "sumber"])
    df = _numeric(
        df, ["jangkauan_iklan_juta", "persen_populasi", "persen_internet"]
    )
    df["peringkat"] = (
        df["jangkauan_iklan_juta"].rank(ascending=False, method="min").astype(int)
    )
    df["share_dari_terbesar"] = (
        df["jangkauan_iklan_juta"] / df["jangkauan_iklan_juta"].max() * 100
    ).round(1)
    return df.sort_values("jangkauan_iklan_juta", ascending=False).reset_index(drop=True)


def ecommerce_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["platform", "jenis", "kategori_utama", "catatan", "status"])
    df = _numeric(df, ["mau_juta", "gmv_2025_usd_miliar"])
    df["gmv_per_mau_usd"] = (df["gmv_2025_usd_miliar"] / df["mau_juta"]).round(3)
    return df.sort_values("mau_juta", ascending=False).reset_index(drop=True)


def adcost_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["kanal", "objective", "metrik", "satuan", "catatan", "status"])
    df = _numeric(df, ["batas_bawah_rp", "batas_atas_rp"])
    df["titik_tengah_rp"] = (
        (df["batas_bawah_rp"] + df["batas_atas_rp"]) / 2
    ).round(0)
    df["rentang"] = df.apply(
        lambda r: f"Rp{r['batas_bawah_rp']:,.0f} - Rp{r['batas_atas_rp']:,.0f}".replace(
            ",", "."
        ),
        axis=1,
    )
    return df.sort_values("titik_tengah_rp", ascending=False).reset_index(drop=True)


def pain_priority(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["segmen", "pain_point", "status", "sumber"])
    df = _numeric(df, ["frekuensi", "dampak", "kesiapan_bayar"])
    df["skor_prioritas"] = (
        0.4 * df["frekuensi"] + 0.4 * df["dampak"] + 0.2 * df["kesiapan_bayar"]
    ).round(2)
    df["peringkat"] = (
        df["skor_prioritas"].rank(ascending=False, method="min").astype(int)
    )
    df["kuadran"] = np.select(
        [
            (df["frekuensi"] >= 4) & (df["dampak"] >= 4),
            (df["frekuensi"] >= 4) & (df["dampak"] < 4),
            (df["frekuensi"] < 4) & (df["dampak"] >= 4),
        ],
        ["Kritis", "Sering tapi ringan", "Jarang tapi berat"],
        default="Monitor",
    )
    return df.sort_values("skor_prioritas", ascending=False).reset_index(drop=True)


def trust_gap(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _text(df, ["dimensi", "status", "sumber"])
    df = _numeric(df, ["kepentingan", "kinerja_agency"])
    df["gap"] = (df["kepentingan"] - df["kinerja_agency"]).round(2)
    df["prioritas_perbaikan"] = (
        df["gap"].rank(ascending=False, method="min").astype(int)
    )
    return df.sort_values("gap", ascending=False).reset_index(drop=True)


def service_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(SERVICE_RULES)
    matrix = df.set_index("nama")[cols].copy()
    matrix["Total layanan"] = matrix.sum(axis=1)
    return matrix.sort_values("Total layanan", ascending=False)


def competitor_by_city(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("kota_utama", dropna=False)
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )


def competitor_by_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("tipe_sederhana")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )


def service_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df[list(SERVICE_RULES)].sum().sort_values(ascending=False)
    out = counts.reset_index()
    out.columns = ["layanan", "jumlah"]
    return out


def price_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df[df["harga_transparan"]].copy()
    return out.sort_values("nama")[
        ["nama", "basis_kota", "tipe_sederhana", "sinyal_harga", "url"]
    ]


def impost_supply(kompetitor_df: pd.DataFrame, impost: pd.DataFrame) -> pd.Series:
    """Jumlah kompetitor yang menjual layanan terkait tiap layanan IMPOST.

    layanan_terkait berisi label SERVICE_RULES dipisah ';'. Pasokan diambil
    sebagai nilai maksimum antar label (satu agency dihitung sekali per
    layanan IMPOST meski mencakup beberapa label).
    """
    sup = {}
    for layanan in impost["layanan"]:
        terkait = impost.loc[impost["layanan"] == layanan, "layanan_terkait"].iloc[0]
        labels = [s.strip() for s in str(terkait).split(";") if s.strip() in SERVICE_RULES]
        values = [int(kompetitor_df[label].sum()) for label in labels if label in kompetitor_df]
        sup[layanan] = max(values) if values else 0
    return pd.Series(sup, dtype=int)


def impost_demand(
    impost: pd.DataFrame,
    supply: pd.Series,
    demand_ringkas: pd.DataFrame | None,
) -> pd.DataFrame:
    """Skor demand 1-5 per layanan x wilayah dari sinyal pencarian + pasokan.

    sinyal_cari = jumlah domain unik hasil pencarian 'jasa <layanan> <wilayah>'
    (scraping ddgs, Lapis 1). demand_skor = 1 + 4 * (0,6 * normalisasi sinyal
    dalam wilayah + 0,4 * normalisasi pasokan kompetitor). Label: Hipotesis.
    """
    df = impost.copy()
    df = _numeric(
        df,
        [
            "harga_pasar_min_rp", "harga_pasar_max_rp",
            "harga_ideal_min_rp", "harga_ideal_max_rp",
        ],
    )
    df = _text(
        df,
        ["kategori", "layanan_terkait", "satuan_pasar", "sumber_harga_pasar",
         "satuan_ideal", "dasar_harga_ideal", "status_harga_ideal"],
    )
    df["tengah_pasar_rp"] = (
        (df["harga_pasar_min_rp"] + df["harga_pasar_max_rp"]) / 2
    ).round(0)
    df["tengah_ideal_rp"] = (
        (df["harga_ideal_min_rp"] + df["harga_ideal_max_rp"]) / 2
    ).round(0)
    df["posisi_vs_pasar"] = (
        df["tengah_ideal_rp"] / df["tengah_pasar_rp"]
    ).round(2)

    df["pasokan_kompetitor"] = df["layanan"].map(supply).fillna(0).astype(int)
    sup_max = max(float(supply.max()) if len(supply) else 0.0, 1.0)
    sup_norm = df["pasokan_kompetitor"] / sup_max

    if demand_ringkas is not None and len(demand_ringkas):
        for wil in WILAYAH_DEMAND:
            sub = demand_ringkas[demand_ringkas["wilayah"] == wil]
            n_map = dict(zip(sub["layanan"], sub["n_domain"]))
            sig = df["layanan"].map(n_map).fillna(0).astype(float)
            sig_max = max(float(sig.max()), 1.0)
            df[f"sinyal_cari_{wil.lower()}"] = sig.astype(int)
            df[f"demand_{wil.lower()}"] = (
                1 + 4 * (0.6 * (sig / sig_max) + 0.4 * sup_norm)
            ).round(2)
    else:
        for wil in WILAYAH_DEMAND:
            df[f"sinyal_cari_{wil.lower()}"] = 0
            df[f"demand_{wil.lower()}"] = (1 + 4 * 0.4 * sup_norm).round(2)
    return df


def prepare_all(write: bool = True) -> dict:
    makro = clean_macro(_read("makro-kalimantan.csv"))
    kota = clean_cities(_read("kota-kalimantan.csv"))
    industri = score_industries(_read("skor-industri.csv"))
    kompetitor = clean_competitors(_read("kompetitor.csv"))
    kompetitor["cakupan"] = "Kalimantan"
    platform = platform_summary(_read("platform-indonesia.csv"))
    ecommerce = ecommerce_summary(_read("ecommerce-indonesia.csv"))
    adcost = adcost_summary(_read("biaya-iklan.csv"))
    pain = pain_priority(_read("pain-point.csv"))
    persepsi = trust_gap(_read("persepsi.csv"))
    layanan = _numeric(
        _read("layanan-winning.csv"), ["harga_min_rp", "harga_max_rp"]
    )
    layanan = _text(layanan, ["tier", "target", "satuan", "isi", "tujuan"])
    layanan_industri = _numeric(
        _read("layanan-industri.csv"), ["harga_min_rp", "harga_max_rp"]
    )
    layanan_industri = _text(
        layanan_industri,
        ["paket", "industri", "satuan", "komponen", "kpi", "alasan_menang"],
    )
    layanan_addon = _numeric(
        _read("layanan-addon.csv"), ["harga_min_rp", "harga_max_rp"]
    )
    layanan_addon = _text(layanan_addon, ["layanan", "satuan"])
    impost_raw = _read("impost-layanan.csv")
    demand_ringkas = None
    demand_path = DATA_DIR / "scraping" / "demand-ringkas.csv"
    if demand_path.exists():
        demand_ringkas = pd.read_csv(demand_path)
        demand_ringkas = _text(demand_ringkas, ["layanan", "wilayah"])
        demand_ringkas = _numeric(demand_ringkas, ["n_domain"])
    sumber = _read("sumber.csv")
    sumber = _text(
        sumber,
        ["topik", "sumber", "url", "tahun", "jenis_data", "status", "catatan"],
    )
    channel = _read("channel-matrix.csv")
    channel["industri"] = channel["industri"].astype(str).str.strip()
    channel = channel.set_index("industri")
    channel = channel.apply(pd.to_numeric, errors="coerce").fillna(0)
    channel["rata_rata"] = channel.mean(axis=1).round(2)
    channel = channel.sort_values("rata_rata", ascending=False)

    by_city = competitor_by_city(kompetitor)
    by_type = competitor_by_type(kompetitor)
    svc_counts = service_counts(kompetitor)
    matrix = service_matrix(kompetitor)
    prices = price_signals(kompetitor)

    supply = competitor_supply(kompetitor)
    industri_map = _read("industri-layanan.csv")
    industri_map = _text(industri_map, ["industri", "layanan_inti", "catatan"])
    industri = measured_competition(industri, industri_map, supply)

    supply_impost = impost_supply(kompetitor, impost_raw)
    impost = impost_demand(impost_raw, supply_impost, demand_ringkas)

    fastest = makro.loc[makro["pertumbuhan_terbaru"].idxmax()]
    highest_net = makro.loc[makro["penetrasi_internet_2025_persen"].idxmax()]
    lowest_net = makro.loc[makro["penetrasi_internet_2025_persen"].idxmin()]
    largest_pop = makro.loc[makro["penduduk_2025"].idxmax()]
    top_industry = industri.iloc[0]
    top_pain = pain.iloc[0]
    top_platform = platform.iloc[0]
    top_ecommerce = ecommerce.iloc[0]
    city_umkm = kota.dropna(subset=["umkm_unit"]).sort_values(
        "umkm_unit", ascending=False
    )
    top_city_umkm = city_umkm.iloc[0] if len(city_umkm) else None
    channel_top = channel.drop(columns=["rata_rata"]).mean(axis=1).idxmax()
    paket_bulanan = layanan[
        (layanan["satuan"] == "per bulan") & layanan["harga_min_rp"].notna()
    ].sort_values("harga_min_rp")
    entry_offer = paket_bulanan.iloc[0] if len(paket_bulanan) else None
    growth_offer = layanan[layanan["tier"].str.lower() == "growth"]
    top_service = svc_counts.iloc[0] if len(svc_counts) else None
    imp_kalsel_top = impost.sort_values("demand_kalsel", ascending=False).iloc[0]
    imp_nas_top = impost.sort_values("demand_nasional", ascending=False).iloc[0]
    imp_lowest = impost.sort_values("demand_kalimantan").iloc[0]

    metrics = {
        "generated_at": datetime.now().strftime("%d %b %Y %H:%M"),
        "data_status": "Desk research + hipotesis; fokus pengumpulan data internet",
        "n_provinsi": int(len(makro)),
        "n_kota": int(len(kota)),
        "n_industri": int(len(industri)),
        "n_industri_naik": int((industri["delta_peringkat"] > 0).sum()),
        "n_industri_turun": int((industri["delta_peringkat"] < 0).sum()),
        "n_industri_tetap": int((industri["delta_peringkat"] == 0).sum()),
        "n_prioritas_inti_terukur": int(
            (industri["prioritas_terukur"] == "Prioritas inti").sum()
        ),
        "industri_naik_terbanyak": str(
            industri.loc[industri["delta_peringkat"].idxmax(), "industri"]
        ),
        "industri_turun_terbanyak": str(
            industri.loc[industri["delta_peringkat"].idxmin(), "industri"]
        ),
        "delta_peringkat_maks": int(industri["delta_peringkat"].max()),
        "delta_peringkat_min": int(industri["delta_peringkat"].min()),
        "n_kompetitor": int(len(kompetitor)),
        "n_kompetitor_lokal": int((kompetitor["tipe_sederhana"] == "Lokal").sum()),
        "n_kompetitor_nasional": int((kompetitor["tipe_sederhana"] == "Nasional").sum()),
        "n_harga_transparan": int(kompetitor["harga_transparan"].sum()),
        "n_pain_point": int(len(pain)),
        "n_pain_kritis": int((pain["kuadran"] == "Kritis").sum()),
        "n_persepsi_dimensi": int(len(persepsi)),
        "n_platform": int(len(platform)),
        "n_ecommerce": int(len(ecommerce)),
        "n_ad_benchmark": int(len(adcost)),
        "n_sumber": int(len(sumber)),
        "n_paket": int(len(layanan)),
        "n_paket_industri": int(len(layanan_industri)),
        "n_addon": int(len(layanan_addon)),
        "n_impost_layanan": int(len(impost)),
        "impost_demand_tertinggi_kalsel": str(imp_kalsel_top["layanan"]),
        "impost_demand_kalsel_skor": float(imp_kalsel_top["demand_kalsel"]),
        "impost_demand_tertinggi_nasional": str(imp_nas_top["layanan"]),
        "impost_demand_nasional_skor": float(imp_nas_top["demand_nasional"]),
        "impost_demand_terendah_kalimantan": str(imp_lowest["layanan"]),
        "impost_demand_kalimantan_skor": float(imp_lowest["demand_kalimantan"]),
        "paket_entry": str(entry_offer["tier"]) if entry_offer is not None else "-",
        "harga_entry_rp": int(entry_offer["harga_min_rp"]) if entry_offer is not None else 0,
        "harga_growth_rp": int(growth_offer["harga_min_rp"].iloc[0]) if len(growth_offer) else 0,
        "layanan_terlaris": str(top_service["layanan"]) if top_service is not None else "-",
        "layanan_terlaris_jumlah": int(top_service["jumlah"]) if top_service is not None else 0,
        "internet_nasional": NATIONAL_INTERNET,
        "social_users_juta": NATIONAL_SOCIAL_USERS,
        "provinsi_tumbuh_tercepat": str(fastest["provinsi"]),
        "pertumbuhan_tercepat": float(fastest["pertumbuhan_terbaru"]),
        "tahun_pertumbuhan_tercepat": str(fastest["tahun_pertumbuhan"]),
        "provinsi_internet_tertinggi": str(highest_net["provinsi"]),
        "internet_tertinggi": float(highest_net["penetrasi_internet_2025_persen"]),
        "provinsi_internet_terendah": str(lowest_net["provinsi"]),
        "internet_terendah": float(lowest_net["penetrasi_internet_2025_persen"]),
        "provinsi_penduduk_terbesar": str(largest_pop["provinsi"]),
        "penduduk_provinsi_terbesar": int(largest_pop["penduduk_2025"]),
        "total_penduduk_provinsi": int(makro["penduduk_2025"].sum()),
        "total_penduduk_kota": int(kota["penduduk"].sum()),
        "industri_prioritas": str(top_industry["industri"]),
        "skor_industri_prioritas": float(top_industry["skor_tertimbang"]),
        "pain_point_prioritas": str(top_pain["pain_point"]),
        "skor_pain_prioritas": float(top_pain["skor_prioritas"]),
        "platform_terbesar": str(top_platform["platform"]),
        "platform_terbesar_juta": float(top_platform["jangkauan_iklan_juta"]),
        "ecommerce_terbesar": str(top_ecommerce["platform"]),
        "kanal_prioritas": str(channel_top),
        "kota_umkm_terbesar": str(top_city_umkm["kota"]) if top_city_umkm is not None else "-",
        "umkm_kota_terbesar": int(top_city_umkm["umkm_unit"]) if top_city_umkm is not None else 0,
    }

    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        makro.to_csv(OUT_DIR / "makro_clean.csv", index=False)
        kota.to_csv(OUT_DIR / "kota_clean.csv", index=False)
        industri.to_csv(OUT_DIR / "industri_rank.csv", index=False)
        supply.to_frame("pasokan").to_csv(OUT_DIR / "layanan_supply.csv")
        kompetitor.to_csv(OUT_DIR / "kompetitor_clean.csv", index=False)
        platform.to_csv(OUT_DIR / "platform_summary.csv", index=False)
        ecommerce.to_csv(OUT_DIR / "ecommerce_summary.csv", index=False)
        adcost.to_csv(OUT_DIR / "biaya_iklan_clean.csv", index=False)
        pain.to_csv(OUT_DIR / "pain_priority.csv", index=False)
        persepsi.to_csv(OUT_DIR / "trust_gap.csv", index=False)
        layanan.to_csv(OUT_DIR / "layanan_winning.csv", index=False)
        layanan_industri.to_csv(OUT_DIR / "layanan_industri.csv", index=False)
        layanan_addon.to_csv(OUT_DIR / "layanan_addon.csv", index=False)
        impost.to_csv(OUT_DIR / "impost_layanan.csv", index=False)
        sumber.to_csv(OUT_DIR / "sumber_clean.csv", index=False)
        by_city.to_csv(OUT_DIR / "kompetitor_by_city.csv", index=False)
        by_type.to_csv(OUT_DIR / "kompetitor_by_type.csv", index=False)
        svc_counts.to_csv(OUT_DIR / "service_counts.csv", index=False)
        matrix.to_csv(OUT_DIR / "service_matrix.csv")
        prices.to_csv(OUT_DIR / "harga_kompetitor.csv", index=False)
        channel.to_csv(OUT_DIR / "channel_matrix_clean.csv")
        (OUT_DIR / "metrics.json").write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return {
        "makro": makro,
        "kota": kota,
        "industri": industri,
        "kompetitor": kompetitor,
        "supply": supply,
        "industri_map": industri_map,
        "platform": platform,
        "ecommerce": ecommerce,
        "adcost": adcost,
        "pain": pain,
        "persepsi": persepsi,
        "layanan": layanan,
        "layanan_industri": layanan_industri,
        "layanan_addon": layanan_addon,
        "impost": impost,
        "sumber": sumber,
        "channel": channel,
        "competitor_by_city": by_city,
        "competitor_by_type": by_type,
        "service_counts": svc_counts,
        "service_matrix": matrix,
        "prices": prices,
        "metrics": metrics,
    }


if __name__ == "__main__":
    result = prepare_all()
    m = result["metrics"]
    print("Analisis selesai.")
    print(f"  Provinsi          : {m['n_provinsi']}")
    print(f"  Kota              : {m['n_kota']}")
    print(f"  Industri          : {m['n_industri']}")
    print(f"  Kompetitor        : {m['n_kompetitor']} "
          f"({m['n_kompetitor_lokal']} lokal / {m['n_kompetitor_nasional']} nasional)")
    print(f"  Pain point        : {m['n_pain_point']} "
          f"({m['n_pain_kritis']} kritis)")
    print(f"  Paket layanan     : {m['n_paket']} paket + "
          f"{m['n_paket_industri']} paket industri + {m['n_addon']} add-on")
    print(f"  Sumber            : {m['n_sumber']}")
    print(f"  Tumbuh tercepat   : {m['provinsi_tumbuh_tercepat']} "
          f"{m['pertumbuhan_tercepat']:.2f}%")
    print(f"  Internet tertinggi: {m['provinsi_internet_tertinggi']} "
          f"{m['internet_tertinggi']:.2f}%")
    print(f"  Industri prioritas: {m['industri_prioritas']} "
          f"({m['skor_industri_prioritas']:.2f})")
    print(f"  Output            : {OUT_DIR}")
