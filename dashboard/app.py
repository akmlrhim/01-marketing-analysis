"""Streamlit dashboard: Riset Pasar Agency Digital Marketing Kalimantan.

Gaya: dashboard gelap utilitarian, aksen merah bata, font Source Sans 3.
Navigasi radio-style di sidebar; tiap halaman = satu blok `if page == ...`.
Grafik Plotly dibuat noninteraktif (tanpa zoom/pan/seleksi).
"""

from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import NATIONAL_INTERNET, OUT_DIR, prepare_all

st.set_page_config(
    page_title="Riset Pasar Kalimantan",
    page_icon="ðŸ“Š",
    layout="wide",
    initial_sidebar_state="auto",
)

# Palet mengikuti variabel :root di CSS di bawah; ubah keduanya bersama-sama.
AKSEN = "#C15B3C"  # merah bata
AKSEN_TERANG = "#E29B7E"
SLATE = "#CBD5E1"
AMBER = "#FBBF24"
RED = "#F87171"
HIJAU = "#4ADE80"
BLUE = "#60A5FA"
VIOLET = "#A78BFA"
PALETTE = [AKSEN, AKSEN_TERANG, AMBER, BLUE, VIOLET, "#22D3EE", "#A3E635"]

PAGES = [
    "Industri Winning",
    "Pain Point Owner",
    "Industri Potensial",
    "Kompetitor Agency",
    "Layanan Winning",
    "Layanan IMPOST",
    "Sosial Media",
    "Persepsi Agency",
    "Pasar Kota",
    "Metodologi",
]

st.markdown(
    """
    <style>
    /* ======:root — satu-satunya tempat menyetel warna, radius, dan lebar ====== */
    :root {
      --bg: #0F172A;           /* latar halaman */
      --panel: #1E293B;        /* kartu / panel */
      --border: #334155;       /* garis */
      --teks: #F1F5F9;         /* teks utama */
      --abu: #94A3B8;          /* teks sekunder */
      --aksen: #C15B3C;        /* merah bata — bullet aktif, bar, elemen inti */
      --aksen-terang: #E29B7E; /* varian aksen untuk teks di atas panel */
      --amber: #FBBF24;
      --hijau: #4ADE80;
      --merah: #F87171;
      --netral: #94A3B8;       /* biru-abu untuk badge netral */
      --radius: 14px;
      --sidebar: 300px;
    }

    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700&display=swap');
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
    *, body { font-family: "Source Sans 3", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif !important; }
    [data-testid="stIconMaterial"] { font-family: "Material Symbols Rounded" !important;
                                     font-size: 20px; line-height: 1; }
    header[data-testid="stHeader"] { background: var(--bg); }
    [data-testid="stMain"] { margin-top: 3.75rem; height: calc(100% - 3.75rem); }
    h1, h2, h3, h4 { color: var(--teks); letter-spacing: -0.01em; }
    h2 { font-size: 1.3rem; margin-top: .3rem; letter-spacing: -0.02em; }
    h3 { font-size: 1.02rem; letter-spacing: -0.02em; }

    /* --- Sidebar: radio-style, bullet merah bata saat aktif --- */
    section[data-testid="stSidebar"] { background: var(--bg); border-right: 1px solid var(--border); }
    [data-testid="stSidebar"] input[type="radio"] { accent-color: var(--aksen); }
    [data-testid="stSidebar"] [role="radiogroup"] label { padding: 3px 0; }
    [data-testid="stSidebar"] label:has(input[type="radio"]:checked) { color: var(--aksen-terang); font-weight: 600; }
    [data-testid="stSidebar"] hr { border-color: var(--border); }
    [data-testid="stSidebar"] [data-testid="stExpander"] details {
        border: 1px solid var(--border); border-radius: 10px; background: transparent; }

    /* --- Kartu stats: st.metric native, font default Streamlit --- */
    [data-testid="stMetric"], [data-testid="stMetric"] * {
        font-family: "Source Sans 3", "Source Sans Pro", sans-serif !important;
    }
    /* Animasi stagger: kartu metrik muncul bertahap saat halaman dibuka */
    @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); }
                        to { opacity: 1; transform: translateY(0); } }
    [data-testid="stMetric"] { animation: fadeUp .45s ease backwards; }
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] { animation-delay: .05s; }
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] { animation-delay: .15s; }
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] { animation-delay: .25s; }
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] { animation-delay: .35s; }

    /* --- Badge semantik: pill bulat --- */
    .badge { display: inline-block; padding: 2px 11px; border-radius: 999px;
             font-size: 11.5px; font-weight: 600; line-height: 1.7; white-space: nowrap; }
    .badge.tinggi { background: rgba(193,91,60,.16); color: var(--aksen-terang); border: 1px solid var(--aksen); }
    .badge.sedang { background: rgba(251,191,36,.13); color: var(--amber); border: 1px solid rgba(251,191,36,.55); }
    .badge.baik   { background: rgba(74,222,128,.12); color: var(--hijau); border: 1px solid rgba(74,222,128,.5); }
    .badge.netral { background: rgba(148,163,184,.12); color: var(--netral); border: 1px solid rgba(148,163,184,.45); }

    /* --- Bar chart CSS murni: kategori + bar + angka --- */
    .bars { display: flex; flex-direction: column; gap: 9px; padding: 4px 0 8px; }
    .bars-row { display: grid; grid-template-columns: minmax(150px, 240px) 1fr auto;
                gap: 12px; align-items: center; }
    .bars-label { color: var(--teks); font-size: 13px; overflow: hidden;
                  text-overflow: ellipsis; white-space: nowrap; }
    .bars-track { background: rgba(148,163,184,.10); border-radius: 6px; height: 16px; overflow: hidden; }
    .bars-fill { background: var(--aksen); height: 100%; border-radius: 6px;
                 animation: tumbuh .7s cubic-bezier(.2,.7,.3,1) backwards; }
    @keyframes tumbuh { from { width: 0 !important; } }
    .bars-value { font-family: "Source Sans 3", ui-monospace, monospace !important;
                  color: var(--abu); font-size: 13px; min-width: 44px; text-align: right;
                  font-variant-numeric: tabular-nums; }

    /* --- Tabel HTML: hover baris, angka rata kanan, badge di kolom status --- */
    table.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
    table.tbl th { text-align: left; color: var(--abu); font-size: 11px; font-weight: 700;
                   letter-spacing: .06em; text-transform: uppercase;
                   padding: 8px 10px; border-bottom: 1px solid var(--border); }
    table.tbl td { padding: 8px 10px; border-bottom: 1px solid rgba(51,65,85,.55);
                   color: var(--teks); vertical-align: middle; }
    table.tbl tr:hover td { background: rgba(148,163,184,.07); }
    table.tbl td.num, table.tbl th.num { text-align: right;
                   font-family: "Source Sans 3", ui-monospace, monospace !important;
                   font-variant-numeric: tabular-nums; }

    .note { background: rgba(193,91,60,.10); border-left: 3px solid var(--aksen); border-radius: 8px;
            padding: 10px 14px; color: var(--aksen-terang); font-size: 13px; margin: 6px 0 12px; }
    .warn { background: rgba(251,191,36,.08); border-left: 3px solid var(--amber); border-radius: 8px;
            padding: 10px 14px; color: #FDE68A; font-size: 13px; margin: 6px 0 12px; }
    .small { color: var(--abu); font-size: 12px; }
    div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 10px;
                                     font-variant-numeric: tabular-nums; }
    [data-testid="stExpander"] details { border-color: var(--border); border-radius: 10px; }

    button:focus-visible, [role="tab"]:focus-visible, a:focus-visible {
        outline: 2px solid var(--aksen); outline-offset: 2px; }
    ::-webkit-scrollbar { width:10px; height:10px; }
    ::-webkit-scrollbar-track { background:transparent; }
    ::-webkit-scrollbar-thumb { background:var(--border); border-radius:8px; border:2px solid var(--bg); }
    ::-webkit-scrollbar-thumb:hover { background:#475569; }
    ::selection { background: rgba(193,91,60,.35); color: var(--teks); }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { transition-duration:.01ms !important; animation-duration:.01ms !important; }
    }
    /* --- Mobile: layar <= 640px (sidebar otomatis jadi bar atas) --- */
    @media (max-width: 640px) {
      .block-container { padding-left: .75rem; padding-right: .75rem; }
      header [data-testid="stStatusWidget"], header [data-testid="stDeployButton"] {
          display: none !important; }
      h1 { font-size: 1.35rem; }
      h2 { font-size: 1.12rem; }
      h3, h4 { font-size: .95rem; }
      [data-testid="stMain"] [data-testid="stHorizontalBlock"] { flex-wrap: wrap; row-gap: .75rem; }
      [data-testid="stMain"] [data-testid="stColumn"] { min-width: 100% !important; flex-basis: 100% !important; }
      .bars-row { grid-template-columns: 110px 1fr auto; gap: 8px; }
      .bars-label { font-size: 12px; }
      table.tbl { font-size: 12px; }
      table.tbl th, table.tbl td { padding: 6px 8px; }
      .note, .warn { font-size: 12px; padding: 8px 10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def load_data() -> dict:
    return prepare_all(write=True)


def style_fig(fig: go.Figure, height: int = 360, legend: bool = True) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=8, r=36, t=38, b=8),
        separators=",.",
        font=dict(family="Source Sans 3, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                  size=12, color=SLATE),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="closest",
        dragmode=False,
        hoverlabel=dict(
            bgcolor="#1E293B",
            bordercolor="#475569",
            font=dict(family="Source Sans 3, system-ui, Segoe UI, Roboto, sans-serif",
                      size=12, color="#F1F5F9"),
        ),
    )
    # Noninteraktif: tanpa zoom, pan, atau seleksi; hover tetap aktif.
    fig.update_xaxes(fixedrange=True, showgrid=False, linecolor="#334155")
    fig.update_yaxes(fixedrange=True, gridcolor="#334155", zeroline=False)
    return fig


def kpi(
    label: str,
    value: str,
    sub: str = "",
    accent: str = "",
    delta: str | None = None,
    direction: str = "up",
) -> None:
    """Kartu stats native Streamlit (st.metric): font default, delta ▲ hijau / ▼ merah."""
    _ = accent  # dipertahankan demi kompatibilitas pemanggil lama; nilai tidak diwarnai
    kwargs: dict = {}
    if delta:
        kwargs["delta"] = delta
        kwargs["delta_arrow"] = "up" if direction == "up" else "down"
        kwargs["delta_color"] = "inverse" if direction == "down" else "normal"
    st.metric(label, value, **kwargs)
    if sub:
        st.caption(sub)


def badge(text: str) -> str:
    """Pill badge semantik: tinggi (merah bata), sedang (amber), baik (hijau), netral."""
    kelas = {
        "tinggi": "tinggi",
        "kritis": "tinggi",
        "sedang": "sedang",
        "perhatian": "sedang",
        "sering tapi ringan": "sedang",
        "jarang tapi berat": "sedang",
        "baik": "baik",
        "terverifikasi": "baik",
        "monitor": "netral",
    }.get(str(text).strip().lower(), "netral")
    return f'<span class="badge {kelas}">{text}</span>'


def css_bars(rows: list[tuple[str, float, str]], key: str) -> None:
    """Bar chart CSS murni (tanpa library): kategori + bar + angka.

    `rows` berisi (label, nilai_proporsi, angka_tampil). `key` mengatur
    delay animasi bar bertahap.
    """
    maxv = max((v for _, v, _ in rows), default=0) or 1
    parts = ['<div class="bars">']
    for i, (label, val, disp) in enumerate(rows):
        pct = max(2, round(val / maxv * 100))
        delay = f"animation-delay:{i * 0.06:.2f}s;"
        parts.append(
            f'<div class="bars-row"><div class="bars-label">{label}</div>'
            f'<div class="bars-track"><div class="bars-fill" style="width:{pct}%;{delay}"></div></div>'
            f'<div class="bars-value">{disp}</div></div>'
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)
    _ = key  # disimpan untuk penandaan elemen di masa depan


def html_table(
    headers: list[str],
    rows: list[list[str]],
    num_cols: tuple[int, ...] = (),
    badge_cols: tuple[int, ...] = (),
) -> None:
    """Tabel HTML: hover baris, kolom angka rata kanan, badge di kolom status."""
    head = "".join(
        f'<th class="{"num" if i in num_cols else ""}">{h}</th>'
        for i, h in enumerate(headers)
    )
    body_rows = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cls = "num" if i in num_cols else ""
            val = badge(cell) if i in badge_cols else str(cell)
            cells.append(f'<td class="{cls}">{val}</td>')
        body_rows.append(f"<tr>{''.join(cells)}</tr>")
    st.markdown(
        f'<table class="tbl"><thead><tr>{head}</tr></thead>'
        f'<tbody>{"".join(body_rows)}</tbody></table>',
        unsafe_allow_html=True,
    )


def chart(fig: go.Figure, key: str) -> None:
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False},
        key=key,
    )


def fmt_int(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.0f}".replace(",", ".")


def fmt_dec(value: float | int | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:.{digits}f}".replace(".", ",")


def fmt_rp(value: float | int | None) -> str:
    """Rupiah penuh dengan pemisah ribuan titik: Rp2.500.000."""
    if value is None or pd.isna(value):
        return "-"
    return f"Rp{fmt_int(value)}"


def fmt_offer(lo: float | int | None, hi: float | int | None, satuan: str) -> str:
    if lo is None or pd.isna(lo):
        return "-"
    if satuan.startswith("persen"):
        suffix = satuan.replace("persen", "", 1).strip()
        if hi is None or pd.isna(hi) or hi == lo:
            body = f"{fmt_dec(lo, 0)}%"
        else:
            body = f"{fmt_dec(lo, 0)}-{fmt_dec(hi, 0)}%"
        return f"{body} {suffix}".strip()
    if hi is None or pd.isna(hi) or hi == lo:
        return f"{fmt_rp(lo)} {satuan}"
    return f"{fmt_rp(lo)} sampai {fmt_rp(hi)} {satuan}"


def render_industri(df: pd.DataFrame, key: str, baseline: pd.DataFrame) -> None:
    if df.empty:
        st.info("Tidak ada industri pada filter ini.")
        return
    fig = px.scatter(
        df,
        x="akses_dan_sales_cycle",
        y="skor_tertimbang",
        size="ukuran_pasar",
        color="prioritas",
        hover_name="industri",
        hover_data={
            "pertumbuhan": True,
            "belanja_digital": True,
            "kompetisi_rendah": True,
            "margin_retainer": True,
            "catatan": True,
        },
        size_max=44,
        color_discrete_map={
            "Prioritas inti": AKSEN,
            "Prioritas": "#E29B7E",
            "Potensial": "#94A3B8",
        },
        labels={
            "akses_dan_sales_cycle": "Akses & siklus penjualan",
            "skor_tertimbang": "Skor daya tarik",
        },
    )
    fig.add_vline(x=3, line_dash="dot", line_color="#475569")
    fig.add_hline(y=3.6, line_dash="dot", line_color="#475569")
    fig.update_traces(marker=dict(line=dict(width=1, color="#0F172A")))
    chart(style_fig(fig, 450), f"{key}_scatter")

    col_a, col_b = st.columns([1.05, 1])
    with col_a:
        st.markdown("#### Peringkat industri")
        view = df[
            ["peringkat", "industri", "skor_tertimbang", "prioritas", "catatan"]
        ].rename(
            columns={
                "peringkat": "#",
                "industri": "Industri",
                "skor_tertimbang": "Skor",
                "prioritas": "Prioritas",
                "catatan": "Catatan",
            }
        )
        st.dataframe(
            view,
            hide_index=True,
            width="stretch",
            height=520,
            column_config={
                "Skor": st.column_config.ProgressColumn(
                    "Skor", min_value=3.0, max_value=5.0, format="%.2f"
                )
            },
        )

    with col_b:
        st.markdown("#### Profil industri terpilih")
        pilih = st.selectbox(
            "Pilih industri",
            options=list(df["industri"]),
            index=0,
            label_visibility="collapsed",
            key=f"{key}_pick",
        )
        row = df[df["industri"] == pilih].iloc[0]
        criteria = {
            "ukuran_pasar": "Ukuran pasar",
            "pertumbuhan": "Pertumbuhan",
            "belanja_digital": "Belanja digital",
            "kompetisi_rendah": "Kompetisi rendah",
            "akses_dan_sales_cycle": "Akses",
            "margin_retainer": "Margin retainer",
        }
        labels = list(criteria.values())
        values = [float(row[k]) for k in criteria]
        avg = [float(baseline[k].mean()) for k in criteria]
        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                name=pilih,
                line=dict(color=AKSEN, width=2),
                fillcolor="rgba(193,91,60,.18)",
            )
        )
        fig.add_trace(
            go.Scatterpolar(
                r=avg + [avg[0]],
                theta=labels + [labels[0]],
                name="Rata-rata",
                line=dict(color="#64748B", width=1, dash="dot"),
                fill="none",
            )
        )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickvals=[1, 2, 3, 4, 5]),
                bgcolor="rgba(0,0,0,0)",
            )
        )
        chart(style_fig(fig, 350), f"{key}_radar")


data = load_data()
makro = data["makro"]
kota = data["kota"]
industri = data["industri"]
kompetitor = data["kompetitor"]
platform = data["platform"]
ecommerce = data["ecommerce"]
adcost = data["adcost"]
pain = data["pain"]
persepsi = data["persepsi"]
sumber = data["sumber"]
channel = data["channel"]
matrix = data["service_matrix"]
prices = data["prices"]
layanan = data["layanan"]
layanan_industri = data["layanan_industri"]
layanan_addon = data["layanan_addon"]
impost = data["impost"]
metrics = data["metrics"]

st.markdown(
    '<div class="warn"><b>Status data:</b> kumpulan data diperluas dari sumber publik, tetapi '
    "pain point, persepsi, skor industri, dan benchmark biaya iklan masih berlabel "
    "<b>hipotesis/estimasi</b>. Validasi lapangan belum dijalankan; data masih dari internet.</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Navigasi")
    page = st.radio(
        "Halaman",
        PAGES,
        label_visibility="collapsed",
        key="nav_halaman",
    )
    st.divider()

    with st.expander("Filter data"):
        provinsi_all = list(makro["provinsi"])
        provinsi_sel = st.multiselect("Provinsi", provinsi_all, default=provinsi_all)
        industri_all = list(industri["industri"])
        industri_sel = st.multiselect("Industri", industri_all, default=industri_all)
        tipe_sel = st.radio(
            "Tipe kompetitor",
            ["Semua", "Lokal", "Nasional"],
            horizontal=True,
        )
        dasar_skor = st.radio(
            "Dasar skor industri",
            ["Hipotesis analis", "Terukur data kompetitor"],
            horizontal=True,
            help=(
                "Terukur data kompetitor menghitung ulang kriteria kompetisi rendah "
                "dari 50 agency Kalimantan, bukan dari penilaian manual."
            ),
        )

    st.divider()
    st.markdown("### Cakupan data")
    st.caption(f"{metrics['n_kota']} kota · {metrics['n_industri']} industri")
    st.caption(f"{metrics['n_kompetitor']} kompetitor · {metrics['n_sumber']} sumber")
    st.caption(metrics.get("data_status", "-"))
    st.caption(f"Terakhir diperbarui: {metrics.get('generated_at', '-')}")

    st.divider()
    st.markdown("### Unduh")
    st.download_button(
        "metrics.json",
        data=json.dumps(metrics, ensure_ascii=False, indent=2),
        file_name="metrics.json",
        mime="application/json",
        width="stretch",
    )
    for fname, label in [
        ("kota_clean.csv", "Data kota"),
        ("industri_rank.csv", "Peringkat industri"),
        ("kompetitor_clean.csv", "Data kompetitor"),
        ("pain_priority.csv", "Prioritas pain point"),
        ("sumber_clean.csv", "Daftar sumber"),
    ]:
        path = OUT_DIR / fname
        if path.exists():
            st.download_button(
                label,
                data=path.read_bytes(),
                file_name=fname,
                mime="text/csv",
                width="stretch",
                key=f"dl_{fname}",
            )
    st.divider()
    st.caption("Sumber: BPS, BI, APJII 2025, DataReportal 2026, Dukcapil, website kompetitor.")

industri_f = industri[industri["industri"].isin(industri_sel)].copy()
if dasar_skor == "Terukur data kompetitor":
    industri_f = industri_f.drop(
        columns=["skor_tertimbang", "peringkat", "prioritas"]
    ).rename(
        columns={
            "skor_tertimbang_terukur": "skor_tertimbang",
            "peringkat_terukur": "peringkat",
            "prioritas_terukur": "prioritas",
        }
    )
industri_baseline = industri.copy()
if dasar_skor == "Terukur data kompetitor":
    industri_baseline["kompetisi_rendah"] = industri_baseline["kompetisi_terukur"]
komp_source = kompetitor
if tipe_sel == "Semua":
    komp_f = komp_source.copy()
else:
    komp_f = komp_source[komp_source["tipe_sederhana"] == tipe_sel].copy()

# ===========================================================================
# HALAMAN: PASAR KOTA
# ===========================================================================
if page == "Pasar Kota":
    st.markdown("#### Peta pasar kota")
    st.caption(
        "Ukuran gelembung mengikuti jumlah penduduk, warna menunjukkan provinsi. Data kota "
        "berasal dari BPS, Dukcapil, dan publikasi pemerintah daerah; status tiap baris ada di tabel."
    )
    try:
        kota_map = kota.copy()
        kota_map["umk_rp_fmt"] = [fmt_rp(v) for v in kota_map["umk_rp"]]
        kota_map["penduduk_fmt"] = [fmt_int(v) for v in kota_map["penduduk"]]
        kota_map["umkm_fmt"] = [
            "-" if pd.isna(v) else fmt_int(v) for v in kota_map["umkm_unit"]
        ]
        fig = px.scatter_map(
            kota_map,
            lat="lat",
            lon="lon",
            size="penduduk",
            color="provinsi",
            hover_name="kota",
            hover_data={
                "penduduk_fmt": True,
                "umk_rp_fmt": True,
                "umkm_fmt": True,
                "sektor_utama": True,
                "lat": False,
                "lon": False,
                "penduduk": False,
                "umk_rp": False,
                "umkm_unit": False,
            },
            zoom=4.3,
            center={"lat": 0.2, "lon": 113.8},
            size_max=42,
            map_style="carto-darkmatter",
            color_discrete_sequence=PALETTE,
            labels={
                "penduduk_fmt": "Penduduk",
                "umk_rp_fmt": "UMK",
                "umkm_fmt": "UMKM",
                "sektor_utama": "Sektor utama",
            },
        )
        chart(style_fig(fig, 480), "city_map")
    except Exception as exc:  # pragma: no cover
        st.warning(f"Peta tidak dapat dimuat: {exc}")

    a, b = st.columns([1, 1])
    with a:
        st.markdown("#### Penduduk kota")
        kota_pop = kota.sort_values("penduduk")
        fig = px.bar(
            kota_pop,
            x="penduduk",
            y="kota",
            orientation="h",
            text=[fmt_int(v) for v in kota_pop["penduduk"]],
            color="provinsi",
            color_discrete_sequence=PALETTE,
            labels={"penduduk": "jiwa", "kota": ""},
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 350, legend=False), "city_pop")

    with b:
        st.markdown("#### UMK 2025/2026 (Rp juta)")
        umk_sorted = kota.sort_values("umk_juta")
        fig = px.bar(
            umk_sorted,
            x="umk_juta",
            y="kota",
            orientation="h",
            text=[fmt_dec(v) for v in umk_sorted["umk_juta"]],
            color="umk_juta",
            color_continuous_scale=["#5C2E22", AKSEN],
            labels={"umk_juta": "Rp juta", "kota": ""},
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 350, legend=False), "city_umk")

    st.markdown("#### UMKM yang terdata")
    umkm = kota.dropna(subset=["umkm_unit"]).sort_values("umkm_unit")
    if len(umkm):
        fig = px.bar(
            umkm,
            x="umkm_unit",
            y="kota",
            orientation="h",
            text=[fmt_int(v) for v in umkm["umkm_unit"]],
            color="umkm_per_1000_penduduk",
            color_continuous_scale=["#78350F", AMBER],
            labels={"umkm_unit": "unit UMKM", "kota": ""},
        )
        chart(style_fig(fig, 300, legend=False), "city_umkm")
    else:
        st.info("Belum ada data UMKM kota.")

    st.markdown("#### Tabel kota")
    kota_table = kota[
        [
            "kota",
            "provinsi",
            "penduduk",
            "umk_rp",
            "umkm_unit",
            "internet_provinsi_persen",
            "sektor_utama",
            "status_data",
            "catatan",
        ]
    ].rename(
        columns={
            "kota": "Kota",
            "provinsi": "Provinsi",
            "penduduk": "Penduduk",
            "umk_rp": "UMK (Rp)",
            "umkm_unit": "UMKM",
            "internet_provinsi_persen": "Internet prov. (%)",
            "sektor_utama": "Sektor utama",
            "status_data": "Status data",
            "catatan": "Catatan",
        }
    )
    kota_table["UMK (Rp)"] = [fmt_rp(v) for v in kota_table["UMK (Rp)"]]
    kota_table["Penduduk"] = [fmt_int(v) for v in kota_table["Penduduk"]]
    kota_table["UMKM"] = [
        "-" if pd.isna(v) else fmt_int(v) for v in kota_table["UMKM"]
    ]
    st.dataframe(
        kota_table,
        hide_index=True,
        width="stretch",
        height=360,
    )

# ===========================================================================
# HALAMAN: INDUSTRI WINNING
# ===========================================================================
if page == "Industri Winning":
    winning = industri_f[
        industri_f["prioritas"].isin(["Prioritas inti", "Prioritas"])
    ].copy()
    top_win = (
        winning.sort_values("skor_tertimbang", ascending=False).iloc[0]
        if len(winning)
        else None
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Industri winning", str(len(winning)), "prioritas inti + prioritas")
    with c2:
        kpi(
            "Skor tertinggi",
            f"{fmt_dec(top_win['skor_tertimbang'])}/5" if top_win is not None else "-",
            top_win["industri"] if top_win is not None else "-",
            accent=AMBER,
        )
    with c3:
        kpi(
            "Prioritas inti",
            str(int((winning["prioritas"] == "Prioritas inti").sum())),
            "fokus utama",
            accent=VIOLET,
        )

    st.caption(
        "Kategori prioritas inti dan prioritas. Skor adalah penilaian analis, "
        "belum hasil validasi lapangan."
    )
    if dasar_skor == "Terukur data kompetitor":
        st.info(
            "Skor di halaman ini memakai kriteria kompetisi yang dihitung dari data 32 "
            "agency Kalimantan. Kriteria lain tetap penilaian analis."
        )
    else:
        st.caption(
            "Kriteria kompetisi masih penilaian analis. Bandingkan dengan versi "
            "terukur di blok berikut."
        )

    st.markdown("#### Dampak data kompetitor pada peringkat industri")
    st.caption(
        "Skor kompetisi dihitung dari jumlah dan kekuatan agency yang menjual "
        "layanan inti tiap industri. Kekuatan agency = 1 + 0,5 (terverifikasi) + "
        "0,5 (jumlah layanan / 5). Skor 5 berarti persaingan paling longgar."
    )
    d1, d2, d3 = st.columns(3)
    with d1:
        kpi(
            "Naik peringkat",
            str(metrics["n_industri_naik"]),
            "industri",
            accent=AKSEN,
        )
    with d2:
        kpi(
            "Turun peringkat",
            str(metrics["n_industri_turun"]),
            "industri",
            accent=AMBER,
        )
    with d3:
        kpi(
            "Prioritas inti",
            str(metrics["n_prioritas_inti_terukur"]),
            "versi terukur",
            accent=VIOLET,
        )

    movers = industri[industri["delta_peringkat"] != 0].copy()
    movers = movers.sort_values("delta_peringkat")
    if len(movers):
        fig = px.bar(
            movers,
            x="delta_peringkat",
            y="industri",
            orientation="h",
            text="delta_peringkat",
            color="delta_peringkat",
            color_continuous_scale=["#F59E0B", "#334155", AKSEN],
            color_continuous_midpoint=0,
            labels={"delta_peringkat": "selisih peringkat", "industri": ""},
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        fig.add_vline(x=0, line_color="#475569")
        chart(style_fig(fig, 560, legend=False), "industri_delta")
    else:
        st.info("Tidak ada perubahan peringkat pada filter ini.")

    banding = industri[
        [
            "industri",
            "kompetisi_rendah",
            "kompetisi_terukur",
            "skor_tertimbang",
            "skor_tertimbang_terukur",
            "peringkat",
            "peringkat_terukur",
            "delta_peringkat",
        ]
    ].sort_values("peringkat_terukur")
    st.dataframe(
        banding.rename(
            columns={
                "industri": "Industri",
                "kompetisi_rendah": "Kompetisi (hipotesis)",
                "kompetisi_terukur": "Kompetisi (terukur)",
                "skor_tertimbang": "Skor lama",
                "skor_tertimbang_terukur": "Skor baru",
                "peringkat": "Peringkat lama",
                "peringkat_terukur": "Peringkat baru",
                "delta_peringkat": "Selisih",
            }
        ),
        hide_index=True,
        width="stretch",
        height=420,
    )

    st.divider()
    render_industri(winning, "win", industri_baseline)

# ===========================================================================
# HALAMAN: INDUSTRI POTENSIAL
# ===========================================================================
if page == "Industri Potensial":
    potensial = industri_f[industri_f["prioritas"] == "Potensial"].copy()
    top_pot = (
        potensial.sort_values("skor_tertimbang", ascending=False).iloc[0]
        if len(potensial)
        else None
    )
    c1, c2 = st.columns(2)
    with c1:
        kpi("Industri potensial", str(len(potensial)), "di bawah ambang prioritas")
    with c2:
        kpi(
            "Skor tertinggi potensial",
            f"{fmt_dec(top_pot['skor_tertimbang'])}/5" if top_pot is not None else "-",
            top_pot["industri"] if top_pot is not None else "-",
            accent=BLUE,
        )

    st.caption(
        "Kategori potensial, yaitu industri dengan skor di bawah ambang prioritas "
        "tetapi masih layak dipantau."
    )
    if dasar_skor == "Terukur data kompetitor":
        st.info(
            "Skor di halaman ini memakai kriteria kompetisi yang dihitung dari data 32 "
            "agency Kalimantan. Kriteria lain tetap penilaian analis."
        )
    render_industri(potensial, "pot", industri_baseline)

# ===========================================================================
# HALAMAN: KOMPETITOR AGENCY
# ===========================================================================
if page == "Kompetitor Agency":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Total", str(len(komp_f)), "terpetakan")
    with c2:
        kpi("Lokal", str(int((komp_f["tipe_sederhana"] == "Lokal").sum())), "agency Kalimantan", accent=AKSEN)
    with c3:
        kpi("Nasional", str(int((komp_f["tipe_sederhana"] == "Nasional").sum())), "jaringan nasional", accent=BLUE)
    with c4:
        kpi("Harga terbuka", str(int(komp_f["harga_transparan"].sum())), "publik/pricelist", accent=AMBER)

    st.write("")
    st.caption(
        "Kriteria masuk: agency yang berkantor di Kalimantan, atau agency nasional "
        "yang punya halaman layanan khusus kota Kalimantan. Agency luar Kalimantan "
        "tanpa jejak di pasar ini tidak dimasukkan."
    )
    city_pool = komp_f.loc[
        komp_f["lokasi_terverifikasi"].str.contains("Kalimantan", na=False),
        "kota_utama",
    ]
    city_options = ["Semua"] + sorted(city_pool.unique().tolist())
    city_pick = st.selectbox("Filter kota kompetitor", city_options, index=0)
    komp_view = komp_f if city_pick == "Semua" else komp_f[komp_f["kota_utama"] == city_pick].copy()
    if komp_view.empty:
        st.info(
            "Tidak ada kompetitor pada kombinasi filter ini. Longgarkan filter "
            "kota di atas atau ubah tipe kompetitor di sidebar."
        )

    city_view = komp_view[
        komp_view["lokasi_terverifikasi"].str.contains("Kalimantan", na=False)
    ]
    by_city_v = (
        city_view.groupby("kota_utama")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah")
    )
    by_type_v = (
        komp_view.groupby("tipe_sederhana").size().reset_index(name="jumlah")
    )
    svc_cols = [c for c in matrix.columns if c != "Total layanan"]
    svc_v = komp_view[svc_cols].sum().sort_values().reset_index()
    svc_v.columns = ["layanan", "jumlah"]
    matrix_v = komp_view.set_index("nama")[svc_cols].copy()
    matrix_v["Total layanan"] = matrix_v.sum(axis=1)
    matrix_v = matrix_v.sort_values("Total layanan", ascending=False)

    a, b = st.columns([1.15, 1])
    with a:
        st.markdown("#### Sebaran kota di Kalimantan")
        if len(by_city_v):
            fig = px.bar(
                by_city_v,
                x="jumlah",
                y="kota_utama",
                orientation="h",
                text_auto=True,
                color="jumlah",
                color_continuous_scale=["#5C2E22", AKSEN],
                labels={"jumlah": "jumlah agency", "kota_utama": ""},
            )
            fig.update_layout(coloraxis_showscale=False)
            chart(style_fig(fig, 320, legend=False), "comp_city")
        else:
            st.info("Tidak ada data kota pada filter ini.")

    with b:
        st.markdown("#### Lokal vs nasional")
        if len(by_type_v):
            fig = px.pie(
                by_type_v,
                names="tipe_sederhana",
                values="jumlah",
                hole=0.58,
                color="tipe_sederhana",
                color_discrete_map={
                    "Lokal": AKSEN,
                    "Nasional": "#94A3B8",
                },
            )
            fig.update_traces(textinfo="label+percent", textposition="inside")
            chart(style_fig(fig, 320, legend=False), "comp_type")
        else:
            st.info("Tidak ada data kompetitor pada filter ini.")

    st.markdown("#### Layanan yang paling sering dijual")
    if len(svc_v):
        svc_top = svc_v.sort_values("jumlah", ascending=False)
        css_bars(
            [(r["layanan"], float(r["jumlah"]), fmt_int(r["jumlah"])) for _, r in svc_top.iterrows()],
            key="svc_counts",
        )
    else:
        st.info("Tidak ada layanan terdata pada filter ini.")

    st.markdown("#### Matrix layanan (top 25 berdasarkan jumlah layanan)")
    st.caption("Angka 1 berarti layanan ditawarkan, 0 berarti tidak. Dihitung dari deskripsi layanan publik.")
    heat = matrix_v.head(25).drop(columns=["Total layanan"])
    if len(heat):
        fig = px.imshow(
            heat,
            aspect="auto",
            color_continuous_scale=[[0, "#1E293B"], [1, AKSEN]],
            text_auto=True,
            labels=dict(color=""),
        )
        fig.update_xaxes(side="top")
        chart(style_fig(fig, 620, legend=False), "svc_heat")
    else:
        st.info("Tidak ada kompetitor untuk ditampilkan pada matrix layanan.")

    st.markdown("#### Database kompetitor")
    st.caption(
        "Basis lokasi sudah dicek satu per satu. Kolom Lokasi terverifikasi berisi "
        "kota dan provinsi hasil pengecekan situs, LinkedIn, atau profil resmi."
    )
    st.dataframe(
        komp_view[
            [
                "nama",
                "lokasi_terverifikasi",
                "tipe_sederhana",
                "positioning",
                "sinyal_harga",
                "kekuatan",
                "celah",
                "status_verifikasi",
            ]
        ].rename(
            columns={
                "nama": "Nama",
                "lokasi_terverifikasi": "Lokasi terverifikasi",
                "tipe_sederhana": "Tipe",
                "positioning": "Positioning",
                "sinyal_harga": "Sinyal harga",
                "kekuatan": "Kekuatan",
                "celah": "Celah",
                "status_verifikasi": "Verifikasi",
            }
        ),
        hide_index=True,
        width="stretch",
        height=420,
    )

    st.markdown("#### Sinyal harga publik")
    if len(prices):
        st.dataframe(prices, hide_index=True, width="stretch", height=250)
    else:
        st.info("Tidak ada sinyal harga publik pada filter ini.")

    st.markdown(
        '<div class="note"><b>Catatan:</b> IMPOST Media sengaja dikecualikan karena '
        "kami yang melakukan riset ini. Harga adalah sinyal publik, bukan penawaran resmi.</div>",
        unsafe_allow_html=True,
    )

# ===========================================================================
# HALAMAN: LAYANAN WINNING
# ===========================================================================
if page == "Layanan Winning":
    st.caption(
        "Paket dan harga adalah usulan dari riset layanan, bukan penawaran resmi. "
        "Harga pasar kompetitor ada di halaman Kompetitor Agency."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Paket", str(metrics["n_paket"]), "tangga produk")
    with c2:
        kpi(
            "Entry per bulan",
            fmt_rp(metrics["harga_entry_rp"]),
            metrics["paket_entry"],
            accent=AKSEN,
        )
    with c3:
        kpi(
            "Growth per bulan",
            fmt_rp(metrics["harga_growth_rp"]),
            "paket inti",
            accent=AMBER,
        )

    st.markdown("#### Tangga paket")
    paket_view = layanan.copy()
    paket_view["Harga"] = [
        fmt_offer(lo, hi, satuan)
        for lo, hi, satuan in zip(
            paket_view["harga_min_rp"],
            paket_view["harga_max_rp"],
            paket_view["satuan"],
        )
    ]
    st.dataframe(
        paket_view[["tier", "target", "Harga", "isi", "tujuan"]].rename(
            columns={
                "tier": "Paket",
                "target": "Target",
                "isi": "Isi",
                "tujuan": "Tujuan",
            }
        ),
        hide_index=True,
        width="stretch",
    )

    st.markdown("#### Paket per industri")
    industri_view = layanan_industri.copy()
    industri_view["Harga"] = [
        fmt_offer(lo, hi, satuan)
        for lo, hi, satuan in zip(
            industri_view["harga_min_rp"],
            industri_view["harga_max_rp"],
            industri_view["satuan"],
        )
    ]
    st.dataframe(
        industri_view[
            ["paket", "industri", "Harga", "komponen", "kpi", "alasan_menang"]
        ].rename(
            columns={
                "paket": "Paket",
                "industri": "Industri",
                "komponen": "Komponen",
                "kpi": "KPI",
                "alasan_menang": "Alasan menang",
            }
        ),
        hide_index=True,
        width="stretch",
        height=260,
    )

    st.markdown("#### Add-on")
    addon_view = layanan_addon.copy()
    addon_view["Harga"] = [
        fmt_offer(lo, hi, satuan)
        for lo, hi, satuan in zip(
            addon_view["harga_min_rp"],
            addon_view["harga_max_rp"],
            addon_view["satuan"],
        )
    ]
    st.dataframe(
        addon_view[["layanan", "Harga"]].rename(columns={"layanan": "Layanan"}),
        hide_index=True,
        width="stretch",
    )

    st.markdown("#### Layanan yang paling sering dijual kompetitor")
    st.caption(
        f"Dihitung dari deskripsi layanan publik {len(kompetitor)} kompetitor. Layanan dengan jumlah "
        "tinggi berarti paling banyak dijual, bukan otomatis paling menguntungkan."
    )
    svc = data["service_counts"].sort_values("jumlah", ascending=False)
    css_bars(
        [(r["layanan"], float(r["jumlah"]), fmt_int(r["jumlah"])) for _, r in svc.iterrows()],
        key="layanan_svc",
    )

    st.markdown("#### Benchmark retainer")
    retainer = adcost[adcost["objective"].str.lower() == "retainer"]
    if len(retainer):
        st.dataframe(
            retainer[["kanal", "metrik", "rentang", "satuan"]].rename(
                columns={
                    "kanal": "Kanal",
                    "metrik": "Metrik",
                    "rentang": "Rentang",
                    "satuan": "Satuan",
                }
            ),
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("Belum ada benchmark retainer.")

# ===========================================================================
# HALAMAN: LAYANAN IMPOST
# ===========================================================================
if page == "Layanan IMPOST":
    st.markdown(
        '<div class="warn"><b>Harga ideal masih hipotesis.</b> Harga pasar '
        "disusun dari sinyal publik kompetitor, benchmark pasar, dan laporan "
        "industri (GroupM, Dentsu, PwC). Skor demand diturunkan dari sinyal "
        "pencarian per wilayah (scraping) ditambah pasokan kompetitor, bukan "
        "survei. Validasi lapangan belum dijalankan.</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi(
            "Layanan IMPOST",
            str(metrics["n_impost_layanan"]),
            "harga + demand dipetakan",
        )
    with c2:
        kpi(
            "Demand tertinggi Kalsel",
            metrics["impost_demand_tertinggi_kalsel"],
            delta=f"skor {fmt_dec(metrics['impost_demand_kalsel_skor'])}/5",
            direction="up",
            accent=AMBER,
        )
    with c3:
        kpi(
            "Demand tertinggi nasional",
            metrics["impost_demand_tertinggi_nasional"],
            delta=f"skor {fmt_dec(metrics['impost_demand_nasional_skor'])}/5",
            direction="up",
            accent=BLUE,
        )
    with c4:
        kpi(
            "Demand terendah Kalimantan",
            metrics["impost_demand_terendah_kalimantan"],
            delta=f"skor {fmt_dec(metrics['impost_demand_kalimantan_skor'])}/5",
            direction="down",
            accent=RED,
        )

    st.markdown("#### Peta demand layanan per wilayah (skor 1-5)")
    st.caption(
        "Demand = 1 + 4 × (0,6 × normalisasi sinyal pencarian dalam wilayah + "
        "0,4 × normalisasi pasokan kompetitor). Sinyal pencarian diambil dari "
        "scraping 'jasa <layanan> <wilayah>'; skor 5 berarti permintaan relatif "
        "paling tinggi dibanding layanan lain di wilayah yang sama."
    )
    heat_imp = impost.set_index("layanan")[
        ["demand_kalsel", "demand_kalimantan", "demand_nasional"]
    ]
    heat_imp.columns = ["Kalsel", "Kalimantan", "Nasional"]
    fig = px.imshow(
        heat_imp,
        aspect="auto",
        color_continuous_scale=["#1E293B", "#E8B39E", AKSEN],
        text_auto=True,
        zmin=1,
        zmax=5,
        labels=dict(color="demand"),
    )
    fig.update_xaxes(side="top")
    chart(style_fig(fig, 560, legend=False), "impost_demand_heat")

    a, b = st.columns([1.1, 1])
    with a:
        st.markdown("#### Sinyal pencarian per wilayah")
        st.caption(
            "Jumlah domain unik hasil pencarian 'jasa <layanan> <wilayah>'. "
            "Proxy interest pasar, bukan volume pencarian resmi."
        )
        sig = impost.melt(
            id_vars=["layanan"],
            value_vars=["sinyal_cari_kalsel", "sinyal_cari_kalimantan", "sinyal_cari_nasional"],
            var_name="Wilayah",
            value_name="Domain unik",
        )
        sig["Wilayah"] = sig["Wilayah"].map(
            {
                "sinyal_cari_kalsel": "Kalsel",
                "sinyal_cari_kalimantan": "Kalimantan",
                "sinyal_cari_nasional": "Nasional",
            }
        )
        fig = px.bar(
            sig,
            x="Domain unik",
            y="layanan",
            color="Wilayah",
            barmode="group",
            orientation="h",
            text_auto=True,
            color_discrete_map={"Kalsel": AKSEN, "Kalimantan": AMBER, "Nasional": BLUE},
            labels={"layanan": "", "Domain unik": "domain unik"},
        )
        chart(style_fig(fig, 560), "impost_signal")

    with b:
        st.markdown("#### Pasokan kompetitor")
        st.caption(
            "Jumlah kompetitor (dari 50 agency teraudit) yang menjual layanan "
            "terkait. Pasokan tinggi = pasar ramai; pasokan rendah = celah "
            "atau demand yang belum tergarap."
        )
        sup = impost[["layanan", "pasokan_kompetitor"]].sort_values("pasokan_kompetitor")
        fig = px.bar(
            sup,
            x="pasokan_kompetitor",
            y="layanan",
            orientation="h",
            text_auto=True,
            color="pasokan_kompetitor",
            color_continuous_scale=["#78350F", AMBER],
            labels={"pasokan_kompetitor": "jumlah kompetitor", "layanan": ""},
        )
        fig.update_layout(coloraxis_showscale=False)
        chart(style_fig(fig, 560, legend=False), "impost_supply")

    st.markdown("#### Harga pasar vs harga ideal")
    st.caption(
        "Garis abu-abu = rentang harga pasar (sinyal publik & benchmark). "
        "Garis hijau = harga ideal usulan untuk IMPOST. Skala log karena "
        "rentang antar layanan lebar (per sesi sampai per proyek)."
    )
    fig = go.Figure()
    for _, r in impost.iterrows():
        mid = r["tengah_pasar_rp"]
        fig.add_trace(
            go.Scatter(
                x=[mid],
                y=[r["layanan"]],
                mode="markers",
                marker=dict(size=9, color="#94A3B8"),
                error_x=dict(
                    type="data",
                    symmetric=False,
                    array=[r["harga_pasar_max_rp"] - mid],
                    arrayminus=[mid - r["harga_pasar_min_rp"]],
                    color="#94A3B8",
                    thickness=3,
                ),
                name="Harga pasar",
                showlegend=False,
                customdata=[
                    [
                        fmt_rp(r["harga_pasar_min_rp"]),
                        fmt_rp(r["harga_pasar_max_rp"]),
                        r["satuan_pasar"],
                    ]
                ],
                hovertemplate=(
                    f"<b>{r['layanan']}</b><br>Pasar: "
                    f"%{{customdata[0]}} - %{{customdata[1]}} %{{customdata[2]}}"
                    "<extra></extra>"
                ),
            )
        )
    for _, r in impost.iterrows():
        mid = r["tengah_ideal_rp"]
        fig.add_trace(
            go.Scatter(
                x=[mid],
                y=[r["layanan"]],
                mode="markers",
                marker=dict(size=12, color=AKSEN, symbol="diamond"),
                error_x=dict(
                    type="data",
                    symmetric=False,
                    array=[r["harga_ideal_max_rp"] - mid],
                    arrayminus=[mid - r["harga_ideal_min_rp"]],
                    color=AKSEN,
                    thickness=4,
                ),
                name="Harga ideal",
                showlegend=False,
                customdata=[
                    [
                        fmt_rp(r["harga_ideal_min_rp"]),
                        fmt_rp(r["harga_ideal_max_rp"]),
                        r["satuan_ideal"],
                    ]
                ],
                hovertemplate=(
                    f"<b>{r['layanan']}</b><br>Ideal: "
                    f"%{{customdata[0]}} - %{{customdata[1]}} %{{customdata[2]}}"
                    "<extra></extra>"
                ),
            )
        )
    fig.update_xaxes(type="log", title="Rp (skala log)")
    fig.update_yaxes(title="")
    chart(style_fig(fig, 520, legend=False), "impost_price")

    st.markdown("#### Tabel harga & demand layanan IMPOST")
    st.caption(
        "Posisi ideal vs pasar = titik tengah harga ideal dibagi titik tengah "
        "harga pasar. Di bawah 1 berarti ideal lebih murah dari pasar, di "
        "atas 1 berarti premium."
    )
    imp_view = impost.copy()
    imp_view["Harga pasar"] = [
        fmt_offer(lo, hi, sat)
        for lo, hi, sat in zip(
            imp_view["harga_pasar_min_rp"],
            imp_view["harga_pasar_max_rp"],
            imp_view["satuan_pasar"],
        )
    ]
    imp_view["Harga ideal (usulan)"] = [
        fmt_offer(lo, hi, sat)
        for lo, hi, sat in zip(
            imp_view["harga_ideal_min_rp"],
            imp_view["harga_ideal_max_rp"],
            imp_view["satuan_ideal"],
        )
    ]
    st.dataframe(
        imp_view[
            [
                "layanan",
                "kategori",
                "Harga pasar",
                "Harga ideal (usulan)",
                "posisi_vs_pasar",
                "pasokan_kompetitor",
                "demand_kalsel",
                "demand_kalimantan",
                "demand_nasional",
                "sumber_harga_pasar",
                "dasar_harga_ideal",
                "status_harga_ideal",
            ]
        ].rename(
            columns={
                "layanan": "Layanan",
                "kategori": "Kategori",
                "posisi_vs_pasar": "Ideal vs pasar (×)",
                "pasokan_kompetitor": "Pasokan",
                "demand_kalsel": "Demand Kalsel",
                "demand_kalimantan": "Demand Kalimantan",
                "demand_nasional": "Demand Nasional",
                "sumber_harga_pasar": "Sumber harga pasar",
                "dasar_harga_ideal": "Dasar harga ideal",
                "status_harga_ideal": "Status",
            }
        ),
        hide_index=True,
        width="stretch",
        height=430,
        column_config={
            "Demand Kalsel": st.column_config.ProgressColumn(
                "Demand Kalsel", min_value=1, max_value=5, format="%.2f"
            ),
            "Demand Kalimantan": st.column_config.ProgressColumn(
                "Demand Kalimantan", min_value=1, max_value=5, format="%.2f"
            ),
            "Demand Nasional": st.column_config.ProgressColumn(
                "Demand Nasional", min_value=1, max_value=5, format="%.2f"
            ),
        },
    )

    st.markdown(
        '<div class="note"><b>Konteks demand nasional:</b> belanja iklan '
        "Indonesia diproyeksikan tumbuh 9,5% menjadi US$6,4 miliar pada 2025 "
        "dengan 75% dikuasai kanal digital (GroupM), sementara Dentsu "
        "memproyeksikan pertumbuhan 5,1%. Artinya permintaan layanan digital "
        "marketing nasional tetap tumbuh; skor demand di atas hanya "
        "membandingkan layanan satu sama lain.</div>",
        unsafe_allow_html=True,
    )

# ===========================================================================
# HALAMAN: SOSIAL MEDIA
# ===========================================================================
if page == "Sosial Media":
    a, b = st.columns([1.15, 1])
    with a:
        st.markdown("#### Jangkauan platform (juta)")
        plat = platform.sort_values("jangkauan_iklan_juta")
        fig = px.bar(
            plat,
            x="jangkauan_iklan_juta",
            y="platform",
            orientation="h",
            text_auto=".0f",
            color="kategori",
            color_discrete_sequence=PALETTE,
            labels={"jangkauan_iklan_juta": "juta pengguna", "platform": ""},
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 380), "soc_platform")

    with b:
        st.markdown("#### E-commerce & social commerce")
        fig = px.bar(
            ecommerce.sort_values("mau_juta"),
            x="mau_juta",
            y="platform",
            orientation="h",
            text_auto=".0f",
            color="jenis",
            color_discrete_sequence=PALETTE,
            labels={"mau_juta": "estimasi MAU (juta)", "platform": ""},
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 380), "ecommerce")

    st.markdown("#### Benchmark biaya iklan & retainer")
    st.caption(
        "Angka ini adalah rentang pasar, bukan penawaran resmi. Garis menunjukkan batas bawah "
        "sampai atas, titik menandai nilai tengah. Gunakan untuk memeriksa kewajaran anggaran, "
        "belum sebagai patokan final."
    )
    color_map = {
        "Awareness": AKSEN,
        "Traffic": BLUE,
        "Lead": AMBER,
        "Konten": VIOLET,
        "Retainer": RED,
        "Produksi": "#0891B2",
        "Konversi": "#65A30D",
    }
    fig = go.Figure()
    for _, r in adcost.iterrows():
        mid = r["titik_tengah_rp"]
        low = r["batas_bawah_rp"]
        high = r["batas_atas_rp"]
        color = color_map.get(r["objective"], AKSEN)
        fig.add_trace(
            go.Scatter(
                x=[mid],
                y=[r["kanal"]],
                mode="markers",
                marker=dict(size=10, color=color),
                error_x=dict(
                    type="data",
                    symmetric=False,
                    array=[high - mid],
                    arrayminus=[mid - low],
                    color=color,
                    thickness=3,
                ),
                name=r["objective"],
                showlegend=False,
                hovertemplate=(
                    f"<b>{r['kanal']}</b><br>{r['metrik']} · {r['objective']}<br>"
                    f"{r['rentang']} {r['satuan']}<extra></extra>"
                ),
            )
        )
    fig.update_xaxes(type="log", title="Rp (skala log)")
    fig.update_yaxes(title="")
    chart(style_fig(fig, 400, legend=False), "adcost")

    st.markdown("#### Prioritas kanal per industri")
    st.caption(
        "Skor 1-5 (5 = paling penting). Rekomendasi strategi disusun dari pola industri, "
        "belum dari survei penggunaan."
    )
    channel_top = channel.drop(columns=["rata_rata"]).head(18)
    fig = px.imshow(
        channel_top,
        aspect="auto",
        color_continuous_scale=["#1E293B", "#E8B39E", AKSEN],
        text_auto=True,
        labels=dict(color="prioritas"),
    )
    fig.update_xaxes(side="top")
    chart(style_fig(fig, 640, legend=False), "channel_heat")

    st.markdown("#### Tabel prioritas kanal")
    st.dataframe(channel, width="stretch", height=360)

# ===========================================================================
# HALAMAN: PAIN POINT OWNER
# ===========================================================================
if page == "Pain Point Owner":
    st.markdown(
        '<div class="warn"><b>Skor ini masih hipotesis, belum data survei.</b> Pain point '
        "masih penilaian awal. Validasi lapangan belum dijalankan, jadi jangan dipakai "
        "untuk keputusan final.</div>",
        unsafe_allow_html=True,
    )
    top_pain_row = pain.iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Pain point", str(len(pain)), "lintas segmen")
    with c2:
        kpi(
            "Kritis",
            str(int((pain["kuadran"] == "Kritis").sum())),
            "kuadran kritis",
            accent=RED,
        )
    with c3:
        kpi(
            "Skor tertinggi",
            f"{fmt_dec(top_pain_row['skor_prioritas'])}/5",
            top_pain_row["segmen"],
            accent=AMBER,
        )

    segmen_all = sorted(pain["segmen"].unique().tolist())
    segmen_sel = st.multiselect("Segmen", segmen_all, default=segmen_all)
    pain_f = pain[pain["segmen"].isin(segmen_sel)].copy()

    st.markdown("#### Peta pain point")
    if len(pain_f):
        fig = px.scatter(
            pain_f,
            x="frekuensi",
            y="dampak",
            size="kesiapan_bayar",
            color="segmen",
            hover_name="pain_point",
            hover_data={"skor_prioritas": ":.2f", "kuadran": True},
            size_max=34,
            color_discrete_sequence=PALETTE,
            labels={
                "frekuensi": "Seberapa sering (1-5)",
                "dampak": "Dampak ke bisnis (1-5)",
            },
        )
        fig.add_vline(x=4, line_dash="dot", line_color="#475569")
        fig.add_hline(y=4, line_dash="dot", line_color="#475569")
        fig.update_traces(marker=dict(line=dict(width=1, color="#0F172A")))
        chart(style_fig(fig, 440), "pain_bubble")

        st.markdown("#### 12 prioritas tertinggi")
        top = pain_f.head(12).sort_values("skor_prioritas")
        fig = px.bar(
            top,
            x="skor_prioritas",
            y="pain_point",
            orientation="h",
            text=[fmt_dec(v) for v in top["skor_prioritas"]],
            color="segmen",
            color_discrete_sequence=PALETTE,
            labels={"skor_prioritas": "skor prioritas", "pain_point": ""},
            range_x=[3.8, 5.1],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 430, legend=False), "pain_top")
    else:
        st.info(
            "Tidak ada segmen terpilih. Pilih minimal satu segmen pada filter di atas."
        )

    st.markdown("#### Tabel prioritas pain point")
    st.caption("Kuadran: Kritis = sering + berat; badge mengikuti tingkat urgensi.")
    pain_rows = pain_f[
        [
            "peringkat",
            "segmen",
            "pain_point",
            "frekuensi",
            "dampak",
            "kesiapan_bayar",
            "skor_prioritas",
            "kuadran",
        ]
    ]
    html_table(
        ["#", "Segmen", "Pain point", "Frekuensi", "Dampak", "Kesiapan bayar", "Skor", "Kuadran"],
        [
            [str(int(r["peringkat"])), r["segmen"], r["pain_point"],
             fmt_dec(r["frekuensi"], 1), fmt_dec(r["dampak"], 1),
             fmt_dec(r["kesiapan_bayar"], 1), fmt_dec(r["skor_prioritas"]), r["kuadran"]]
            for _, r in pain_rows.iterrows()
        ],
        num_cols=(0, 3, 4, 5, 6),
        badge_cols=(7,),
    )

# ===========================================================================
# HALAMAN: PERSEPSI TERHADAP AGENCY
# ===========================================================================
if page == "Persepsi Agency":
    st.markdown(
        '<div class="warn"><b>Skor persepsi masih hipotesis, belum data survei.</b> '
        "Kesenjangan kepentingan dan kinerja masih penilaian awal. Validasi lapangan "
        "belum dijalankan, jadi jangan dipakai untuk keputusan final.</div>",
        unsafe_allow_html=True,
    )
    gap_top = persepsi.sort_values("gap", ascending=False).iloc[0]
    c1, c2 = st.columns(2)
    with c1:
        kpi("Dimensi dinilai", str(len(persepsi)), "kepentingan vs kinerja")
    with c2:
        kpi(
            "Gap terbesar",
            fmt_dec(gap_top["gap"]),
            gap_top["dimensi"],
            accent=RED,
        )

    st.caption(
        "Gap adalah selisih antara kepentingan klien dan kinerja agency. "
        "Semakin besar, semakin prioritas untuk diperbaiki."
    )

    st.markdown("#### Kesenjangan kepercayaan: kepentingan vs kinerja")
    gap = persepsi.sort_values("gap")
    melt = gap.melt(
        id_vars=["dimensi"],
        value_vars=["kepentingan", "kinerja_agency"],
        var_name="Variabel",
        value_name="Skor",
    )
    melt["Variabel"] = melt["Variabel"].map(
        {"kepentingan": "Kepentingan klien", "kinerja_agency": "Kinerja agency"}
    )
    fig = px.bar(
        melt,
        x="Skor",
        y="dimensi",
        color="Variabel",
        barmode="group",
        orientation="h",
        color_discrete_map={
            "Kepentingan klien": AKSEN,
            "Kinerja agency": AMBER,
        },
        labels={"dimensi": "", "Skor": "skor (1-5)"},
        range_x=[0, 5.3],
    )
    chart(style_fig(fig, 520), "trust_gap")

    st.markdown("#### Tabel kesenjangan")
    st.caption("Badge tingkat dihitung dari gap: ≥1,00 tinggi, ≥0,50 sedang, di bawahnya baik.")

    def tingkat_gap(g: float) -> str:
        if g >= 1.0:
            return "tinggi"
        if g >= 0.5:
            return "sedang"
        return "baik"

    html_table(
        ["Prioritas", "Dimensi", "Kepentingan", "Kinerja agency", "Gap", "Tingkat"],
        [
            [str(int(r["prioritas_perbaikan"])), r["dimensi"],
             fmt_dec(r["kepentingan"]), fmt_dec(r["kinerja_agency"]),
             fmt_dec(r["gap"]), tingkat_gap(float(r["gap"]))]
            for _, r in persepsi.iterrows()
        ],
        num_cols=(0, 2, 3, 4),
        badge_cols=(5,),
    )

# ===========================================================================
# HALAMAN: METODOLOGI
# ===========================================================================
if page == "Metodologi":
    st.markdown("#### Alur analisis")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            """
            **1. Kumpulkan**
            - BPS, BI, APJII, DataReportal
            - Dukcapil & pemerintah kota
            - Website/pricelist kompetitor
            - Direktori & media lokal
            """
        )
    with s2:
        st.markdown(
            """
            **2. Olah**
            - Validasi kolom & tipe data
            - Skoring industri berbobot
            - Prioritas pain point
            - Kesenjangan kepercayaan & agregasi kompetitor
            """
        )
    with s3:
        st.markdown(
            """
            **3. Keluaran**
            - Dashboard 10 halaman
            - CSV turunan & `metrics.json`
            - Rekomendasi di folder `research/`
            """
        )

    st.markdown("#### Data dictionary")
    ddict = pd.DataFrame(
        [
            ["makro-kalimantan.csv", "Pertumbuhan, PDRB, penduduk, UMP, IPM, internet", "BPS/APJII/Kemnaker", "Desk research"],
            ["kota-kalimantan.csv", "9 kota: penduduk, UMK, UMKM, koordinat", "BPS/Dukcapil", "Desk research"],
            ["skor-industri.csv", "30 industri × 6 kriteria", "Penilaian analis", "Hipotesis"],
            ["industri-layanan.csv", "30 industri × 2-3 layanan inti", "Penilaian analis + data kompetitor", "Hipotesis"],
            ["kompetitor.csv", "50 agency Kalimantan: layanan, kanal, harga, lokasi terverifikasi", "Website/profil publik", "Desk research"],
            ["platform-indonesia.csv", "10 platform & kategori", "DataReportal 2026", "Desk research/estimasi"],
            ["ecommerce-indonesia.csv", "6 marketplace/social commerce", "Estimasi industri", "Estimasi"],
            ["biaya-iklan.csv", "14 benchmark CPM/CPC/CPL/retainer", "Rentang pasar", "Estimasi"],
            ["channel-matrix.csv", "30 industri × 10 kanal", "Penilaian analis", "Hipotesis"],
            ["pain-point.csv", "53 pain point × 3 skor", "Desk research", "Hipotesis"],
            ["persepsi.csv", "14 dimensi kepentingan vs kinerja", "Desk research", "Hipotesis"],
            ["layanan-winning.csv", "5 paket layanan + harga bulanan", "Riset layanan", "Usulan"],
            ["layanan-industri.csv", "4 paket per industri + KPI", "Riset layanan", "Usulan"],
            ["layanan-addon.csv", "5 add-on + harga", "Riset layanan", "Usulan"],
            ["impost-layanan.csv", "11 layanan IMPOST: harga pasar vs harga ideal + demand per wilayah", "Kompetitor + benchmark industri + scraping + penilaian analis", "Campuran (harga ideal = hipotesis)"],
            ["sumber.csv", "30 sumber & status verifikasi", "Publik", "Campuran"],
        ],
        columns=["File", "Isi", "Sumber", "Status"],
    )
    with st.expander("Buka data dictionary (jarang dibuka)"):
        st.dataframe(ddict, hide_index=True, width="stretch")

    st.markdown("#### Sumber & status verifikasi")
    with st.expander("Buka daftar 42 sumber & status verifikasi"):
        st.dataframe(
            sumber[
                ["id", "topik", "sumber", "tahun", "jenis_data", "status", "url"]
            ],
            hide_index=True,
            width="stretch",
            height=420,
            column_config={"url": st.column_config.LinkColumn("URL")},
        )

    st.markdown("#### Jalankan ulang analisis")
    st.caption(
        "Jika CSV di `research/data/` berubah, klik tombol ini atau jalankan "
        "`python dashboard/analysis.py`."
    )
    if st.button("Jalankan ulang analisis", type="primary"):
        with st.spinner("Menghitung ulang metrik..."):
            st.cache_data.clear()
            prepare_all(write=True)
        st.success("Analisis diperbarui.")
        st.rerun()

    st.markdown("#### Metrics JSON")
    with st.expander("Buka detail metrics.json (jarang dibuka)"):
        st.json(metrics)

st.markdown("---")
st.caption(
    "Riset Pasar Agency Digital Marketing Kalimantan · Dashboard internal · "
    f"Terakhir diperbarui {metrics.get('generated_at', '-')} · Status: {metrics.get('data_status', '-')}"
)
