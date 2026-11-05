"""Streamlit dashboard: Riset Pasar Agency Digital Marketing Kalimantan."""

from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import NATIONAL_INTERNET, OUT_DIR, prepare_all

st.set_page_config(
    page_title="Riset Pasar Kalimantan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEAL = "#2DD4BF"
SLATE = "#CBD5E1"
AMBER = "#FBBF24"
RED = "#F87171"
BLUE = "#60A5FA"
VIOLET = "#A78BFA"
PALETTE = ["#2DD4BF", "#FBBF24", "#60A5FA", "#F87171", "#A78BFA", "#22D3EE", "#A3E635"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
    *, body { font-family: "Fira Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif !important; }
    .kpi-value, div[data-testid="stDataFrame"] {
        font-family: "Fira Code", ui-monospace, "Cascadia Mono", monospace !important; }
    header[data-testid="stHeader"] { background: #0F172A; }
    [data-testid="stMain"] { margin-top: 3.75rem; height: calc(100% - 3.75rem); }
    h1, h2, h3, h4 { color: #F1F5F9; letter-spacing: -0.01em; }
    h2 { font-size: 1.3rem; margin-top: .3rem; letter-spacing: -0.02em; }
    h3 { font-size: 1.02rem; letter-spacing: -0.02em; }
    .kpi { background:#1E293B; border:1px solid #334155; border-radius:14px;
           padding:14px 16px; box-shadow:0 1px 2px rgba(0,0,0,.35); min-height:102px;
           transition:border-color .18s ease, box-shadow .18s ease; }
    .kpi:hover { border-color:#475569; box-shadow:0 4px 14px rgba(0,0,0,.4); }
    .kpi-label { color:#94A3B8; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
    .kpi-value { font-size:23px; font-weight:750; line-height:1.2; margin-top:4px;
                 font-variant-numeric:tabular-nums; }
    .kpi-sub { color:#94A3B8; font-size:12px; margin-top:3px; }
    .note { background:rgba(45,212,191,.08); border-left:3px solid #2DD4BF; border-radius:8px;
            padding:10px 14px; color:#99F6E4; font-size:13px; margin:6px 0 12px; }
    .warn { background:rgba(251,191,36,.08); border-left:3px solid #FBBF24; border-radius:8px;
            padding:10px 14px; color:#FDE68A; font-size:13px; margin:6px 0 12px; }
    .small { color:#94A3B8; font-size:12px; }
    div[data-testid="stDataFrame"] { border:1px solid #334155; border-radius:10px;
                                     font-variant-numeric:tabular-nums; }
    section[data-testid="stSidebar"] { background:#0F172A; border-right:1px solid #334155; }
    [role="tablist"] { gap: 10px; flex-wrap: wrap !important; overflow: visible !important; }
    [role="tab"] { border-radius:8px 8px 0 0; padding:10px 16px; cursor:pointer;
                   transition:background-color .18s ease, color .18s ease; }
    [role="tab"]:hover { background:rgba(148,163,184,.1); }
    [role="tab"] p { font-weight:600; font-size:.92rem; }
    button:focus-visible, [role="tab"]:focus-visible, a:focus-visible {
        outline:2px solid #2DD4BF; outline-offset:2px; }
    ::-webkit-scrollbar { width:10px; height:10px; }
    ::-webkit-scrollbar-track { background:transparent; }
    ::-webkit-scrollbar-thumb { background:#334155; border-radius:8px; border:2px solid #0F172A; }
    ::-webkit-scrollbar-thumb:hover { background:#475569; }
    ::selection { background:rgba(45,212,191,.35); color:#F1F5F9; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { transition-duration:.01ms !important; animation-duration:.01ms !important; }
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
        font=dict(family="Fira Sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                  size=12, color=SLATE),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#1E293B",
            bordercolor="#475569",
            font=dict(family="Fira Sans, system-ui, Segoe UI, Roboto, sans-serif",
                      size=12, color="#F1F5F9"),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#334155")
    fig.update_yaxes(gridcolor="#334155", zeroline=False)
    return fig


def kpi(label: str, value: str, sub: str = "", accent: str = TEAL) -> None:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value" style="color:{accent}">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def chart(fig: go.Figure, key: str) -> None:
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, key=key)


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
            "Prioritas inti": TEAL,
            "Prioritas": "#5EEAD4",
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
                line=dict(color=TEAL, width=2),
                fillcolor="rgba(15,118,110,.18)",
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
kaltim_row = makro.loc[makro["provinsi"] == "Kalimantan Timur"].iloc[0]

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
    st.markdown("### Filter data")
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

makro_f = makro[makro["provinsi"].isin(provinsi_sel)].copy()
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

(
    tab_industri_winning,
    tab_pain,
    tab_industri_potensial,
    tab_kompetitor,
    tab_layanan,
    tab_impost,
    tab_sosmed,
    tab_persepsi,
    tab_ringkasan,
    tab_kota,
    tab_metodologi,
) = st.tabs(
    [
        "Industri Winning",
        "Pain Point Owner",
        "Industri Potensial",
        "Kompetitor Agency",
        "Layanan Winning",
        "Layanan IMPOST",
        "Sosial Media",
        "Persepsi Agency",
        "Ringkasan",
        "Pasar Kota",
        "Metodologi",
    ]
)

# ===========================================================================
# TAB: RINGKASAN
# ===========================================================================
with tab_ringkasan:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi("Provinsi", str(metrics["n_provinsi"]), "Kalimantan Timur → Utara")
    with c2:
        kpi("Kota", str(metrics["n_kota"]), "kota besar dipetakan", accent=BLUE)
    with c3:
        kpi(
            "Kompetitor",
            str(metrics["n_kompetitor"]),
            f"{metrics['n_kompetitor_lokal']} lokal · {metrics['n_kompetitor_nasional']} nasional",
            accent=VIOLET,
        )
    with c4:
        kpi("Industri", str(metrics["n_industri"]), "dinilai 6 kriteria", accent=AMBER)
    with c5:
        kpi("Sumber", str(metrics["n_sumber"]), "data & benchmark", accent=TEAL)

    st.write("")
    a, b, c, d = st.columns(4)
    with a:
        kpi(
            "Tumbuh tercepat",
            f"{fmt_dec(metrics['pertumbuhan_tercepat'])}%",
            f"{metrics['provinsi_tumbuh_tercepat']} ({metrics['tahun_pertumbuhan_tercepat']})",
            accent=TEAL,
        )
    with b:
        kpi(
            "Internet tertinggi",
            f"{fmt_dec(metrics['internet_tertinggi'])}%",
            metrics["provinsi_internet_tertinggi"],
            accent=BLUE,
        )
    with c:
        kpi(
            "Industri prioritas",
            metrics["industri_prioritas"].split(" & ")[0],
            f"Skor {fmt_dec(metrics['skor_industri_prioritas'])}/5",
            accent=AMBER,
        )
    with d:
        kpi(
            "Pain point #1",
            "Lead follow-up",
            f"Skor {fmt_dec(metrics['skor_pain_prioritas'])}/5",
            accent=RED,
        )

    st.write("")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("#### Pertumbuhan ekonomi")
        if len(makro_f):
            growth = makro_f.melt(
                id_vars=["provinsi"],
                value_vars=["pertumbuhan_2024_persen", "pertumbuhan_2025_persen"],
                var_name="Tahun",
                value_name="Pertumbuhan",
            )
            growth["Tahun"] = growth["Tahun"].map(
                {"pertumbuhan_2024_persen": "2024", "pertumbuhan_2025_persen": "2025"}
            )
            growth = growth.dropna(subset=["Pertumbuhan"])
            fig = px.bar(
                growth,
                x="provinsi",
                y="Pertumbuhan",
                color="Tahun",
                barmode="group",
                text=[fmt_dec(v) for v in growth["Pertumbuhan"]],
                color_discrete_map={"2024": "#64748B", "2025": TEAL},
                labels={"provinsi": "", "Pertumbuhan": "% (yoy)"},
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            chart(style_fig(fig, 340), "growth")
        else:
            st.info("Pilih minimal satu provinsi pada filter sidebar.")
        st.markdown(
            f'<div class="note"><b>Baca:</b> di antara angka terbaru tiap provinsi, '
            f'{metrics["provinsi_tumbuh_tercepat"]} tertinggi '
            f'({fmt_dec(metrics["pertumbuhan_tercepat"])}%, '
            f'{metrics["tahun_pertumbuhan_tercepat"]}). Kaltim turun dari '
            f'{fmt_dec(kaltim_row["pertumbuhan_2024_persen"])}% (2024) ke '
            f'{fmt_dec(kaltim_row["pertumbuhan_2025_persen"])}% (2025). '
            "<b>Interpretasi:</b> pelemahan Kaltim bertepatan dengan periode setelah puncak IKN; "
            "klaim ini belum diuji dengan data investasi.</div>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### Penetrasi internet 2025")
        if len(makro_f):
            net = makro_f.sort_values("penetrasi_internet_2025_persen")
            fig = px.bar(
                net,
                x="penetrasi_internet_2025_persen",
                y="provinsi",
                orientation="h",
                text=[fmt_dec(v) for v in net["penetrasi_internet_2025_persen"]],
                color="kelas_penetrasi",
                color_discrete_map={
                    "Tinggi": TEAL,
                    "Menengah": "#5EEAD4",
                    "Menengah-rendah": "#F59E0B",
                },
                labels={"penetrasi_internet_2025_persen": "% populasi", "provinsi": ""},
                range_x=[0, 100],
            )
            fig.add_vline(
                x=NATIONAL_INTERNET,
                line_dash="dash",
                line_color=SLATE,
                annotation_text=f"Nasional {fmt_dec(NATIONAL_INTERNET)}%",
                annotation_position="top",
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            chart(style_fig(fig, 340, legend=False), "net")
        else:
            st.info("Pilih minimal satu provinsi pada filter sidebar.")
        st.markdown(
            f'<div class="note"><b>Baca:</b> {metrics["provinsi_internet_tertinggi"]} '
            f'({fmt_dec(metrics["internet_tertinggi"])}%) dan Kaltim '
            f'({fmt_dec(kaltim_row["penetrasi_internet_2025_persen"])}%) di atas rata-rata '
            f'nasional ({fmt_dec(metrics["internet_nasional"])}%), sedangkan '
            f'<b>{metrics["provinsi_internet_terendah"]} '
            f'{fmt_dec(metrics["internet_terendah"])}%</b>. '
            "<b>Interpretasi:</b> di wilayah dengan jangkauan terendah, rencana kampanye "
            "perlu menimbang kanal luring, bukan hanya kanal digital.</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    left2, right2 = st.columns([1, 1.15])
    with left2:
        st.markdown("#### Platform terbesar (juta)")
        plat = platform.head(8).sort_values("jangkauan_iklan_juta")
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
        chart(style_fig(fig, 330), "platform")
        st.caption("WhatsApp & Google Search adalah estimasi, bukan ad reach resmi.")

    with right2:
        st.markdown("#### Skor industri (0-5)")
        top = industri_f.sort_values("skor_tertimbang").tail(12)
        fig = px.bar(
            top,
            x="skor_tertimbang",
            y="industri",
            orientation="h",
            text=[fmt_dec(v) for v in top["skor_tertimbang"]],
            color="prioritas",
            color_discrete_map={
                "Prioritas inti": TEAL,
                "Prioritas": "#5EEAD4",
                "Potensial": "#94A3B8",
            },
            labels={"skor_tertimbang": "skor", "industri": ""},
            range_x=[3.0, 4.5],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        chart(style_fig(fig, 330, legend=False), "industry_rank")

# ===========================================================================
# TAB: PASAR KOTA
# ===========================================================================
with tab_kota:
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
            color_continuous_scale=["#134E4A", TEAL],
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
# TAB: INDUSTRI WINNING
# ===========================================================================
with tab_industri_winning:
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
            "Skor di tab ini memakai kriteria kompetisi yang dihitung dari data 32 "
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
            accent=TEAL,
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
            color_continuous_scale=["#F59E0B", "#334155", TEAL],
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
# TAB: INDUSTRI POTENSIAL
# ===========================================================================
with tab_industri_potensial:
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
            "Skor di tab ini memakai kriteria kompetisi yang dihitung dari data 32 "
            "agency Kalimantan. Kriteria lain tetap penilaian analis."
        )
    render_industri(potensial, "pot", industri_baseline)

# ===========================================================================
# TAB: KOMPETITOR AGENCY
# ===========================================================================
with tab_kompetitor:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Total", str(len(komp_f)), "terpetakan")
    with c2:
        kpi("Lokal", str(int((komp_f["tipe_sederhana"] == "Lokal").sum())), "agency Kalimantan", accent=TEAL)
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
                color_continuous_scale=["#134E4A", TEAL],
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
                    "Lokal": TEAL,
                    "Nasional": "#94A3B8",
                },
            )
            fig.update_traces(textinfo="label+percent", textposition="inside")
            chart(style_fig(fig, 320, legend=False), "comp_type")
        else:
            st.info("Tidak ada data kompetitor pada filter ini.")

    st.markdown("#### Layanan yang paling sering dijual")
    if len(svc_v):
        fig = px.bar(
            svc_v,
            x="jumlah",
            y="layanan",
            orientation="h",
            text_auto=True,
            color="jumlah",
            color_continuous_scale=["#334155", TEAL],
            labels={"jumlah": "jumlah kompetitor", "layanan": ""},
        )
        fig.update_layout(coloraxis_showscale=False)
        chart(style_fig(fig, 380, legend=False), "svc_counts")
    else:
        st.info("Tidak ada layanan terdata pada filter ini.")

    st.markdown("#### Matrix layanan (top 25 berdasarkan jumlah layanan)")
    st.caption("Angka 1 berarti layanan ditawarkan, 0 berarti tidak. Dihitung dari deskripsi layanan publik.")
    heat = matrix_v.head(25).drop(columns=["Total layanan"])
    if len(heat):
        fig = px.imshow(
            heat,
            aspect="auto",
            color_continuous_scale=[[0, "#1E293B"], [1, TEAL]],
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
# TAB: LAYANAN WINNING
# ===========================================================================
with tab_layanan:
    st.caption(
        "Paket dan harga adalah usulan dari riset layanan, bukan penawaran resmi. "
        "Harga pasar kompetitor ada di tab Kompetitor Agency."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Paket", str(metrics["n_paket"]), "tangga produk")
    with c2:
        kpi(
            "Entry per bulan",
            fmt_rp(metrics["harga_entry_rp"]),
            metrics["paket_entry"],
            accent=TEAL,
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
    svc = data["service_counts"].sort_values("jumlah")
    fig = px.bar(
        svc,
        x="jumlah",
        y="layanan",
        orientation="h",
        text_auto=True,
        color="jumlah",
        color_continuous_scale=["#334155", TEAL],
        labels={"jumlah": "jumlah kompetitor", "layanan": ""},
    )
    fig.update_layout(coloraxis_showscale=False)
    chart(style_fig(fig, 420, legend=False), "layanan_svc")

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
# TAB: LAYANAN IMPOST
# ===========================================================================
with tab_impost:
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
            f"skor {fmt_dec(metrics['impost_demand_kalsel_skor'])}/5",
            accent=AMBER,
        )
    with c3:
        kpi(
            "Demand tertinggi nasional",
            metrics["impost_demand_tertinggi_nasional"],
            f"skor {fmt_dec(metrics['impost_demand_nasional_skor'])}/5",
            accent=BLUE,
        )
    with c4:
        kpi(
            "Demand terendah Kalimantan",
            metrics["impost_demand_terendah_kalimantan"],
            f"skor {fmt_dec(metrics['impost_demand_kalimantan_skor'])}/5",
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
        color_continuous_scale=["#1E293B", "#99F6E4", TEAL],
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
            color_discrete_map={"Kalsel": TEAL, "Kalimantan": AMBER, "Nasional": BLUE},
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
                marker=dict(size=12, color=TEAL, symbol="diamond"),
                error_x=dict(
                    type="data",
                    symmetric=False,
                    array=[r["harga_ideal_max_rp"] - mid],
                    arrayminus=[mid - r["harga_ideal_min_rp"]],
                    color=TEAL,
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
# TAB: SOSIAL MEDIA
# ===========================================================================
with tab_sosmed:
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
        "Awareness": TEAL,
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
        color = color_map.get(r["objective"], TEAL)
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
        color_continuous_scale=["#1E293B", "#99F6E4", TEAL],
        text_auto=True,
        labels=dict(color="prioritas"),
    )
    fig.update_xaxes(side="top")
    chart(style_fig(fig, 640, legend=False), "channel_heat")

    st.markdown("#### Tabel prioritas kanal")
    st.dataframe(channel, width="stretch", height=360)

# ===========================================================================
# TAB: PAIN POINT OWNER
# ===========================================================================
with tab_pain:
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
    st.dataframe(
        pain_f[
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
        ].rename(
            columns={
                "peringkat": "#",
                "segmen": "Segmen",
                "pain_point": "Pain point",
                "frekuensi": "Frekuensi",
                "dampak": "Dampak",
                "kesiapan_bayar": "Kesiapan bayar",
                "skor_prioritas": "Skor",
                "kuadran": "Kuadran",
            }
        ),
        hide_index=True,
        width="stretch",
        height=420,
    )

# ===========================================================================
# TAB: PERSEPSI TERHADAP AGENCY
# ===========================================================================
with tab_persepsi:
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
            "Kepentingan klien": TEAL,
            "Kinerja agency": AMBER,
        },
        labels={"dimensi": "", "Skor": "skor (1-5)"},
        range_x=[0, 5.3],
    )
    chart(style_fig(fig, 520), "trust_gap")

    st.markdown("#### Tabel kesenjangan")
    st.dataframe(
        persepsi[
            [
                "prioritas_perbaikan",
                "dimensi",
                "kepentingan",
                "kinerja_agency",
                "gap",
                "status",
            ]
        ].rename(
            columns={
                "prioritas_perbaikan": "Prioritas",
                "dimensi": "Dimensi",
                "kepentingan": "Kepentingan",
                "kinerja_agency": "Kinerja agency",
                "gap": "Gap",
                "status": "Status",
            }
        ),
        hide_index=True,
        width="stretch",
        height=420,
    )

# ===========================================================================
# TAB: METODOLOGI
# ===========================================================================
with tab_metodologi:
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
            - Dashboard 10 tab
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
    st.dataframe(ddict, hide_index=True, width="stretch")

    st.markdown("#### Sumber & status verifikasi")
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
    st.json(metrics)

st.markdown("---")
st.caption(
    "Riset Pasar Agency Digital Marketing Kalimantan · Dashboard internal · "
    f"Terakhir diperbarui {metrics.get('generated_at', '-')} · Status: {metrics.get('data_status', '-')}"
)
