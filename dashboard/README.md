# Dashboard Riset Pasar Kalimantan

Dashboard Streamlit untuk membaca hasil riset pasar agency digital marketing Kalimantan:
9 kota, 30 industri, 50 kompetitor Kalimantan, 10 platform, 6 marketplace, 53 pain point, dan 30 sumber.

## 1. Jalankan

Dari root project:

```bash
# sekali saja
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r dashboard/requirements.txt

# jalankan dashboard
.venv/bin/streamlit run dashboard/app.py
```

Buka `http://localhost:8501`.

Jika memakai WSL dan browser Windows tidak otomatis terbuka:

```bash
.venv/bin/streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```

lalu buka `http://localhost:8501` di browser Windows.

## 2. Struktur

```
dashboard/
├── app.py                 # UI Streamlit (10 tab, 25 grafik)
├── analysis.py            # pipeline cleaning, scoring, agregasi
├── requirements.txt
├── .streamlit/config.toml
└── data/derived/          # output analisis (auto-generated)
    ├── metrics.json
    ├── kota_clean.csv
    ├── industri_rank.csv
    ├── kompetitor_clean.csv
    ├── kompetitor_by_city.csv
    ├── harga_kompetitor.csv
    ├── pain_priority.csv
    ├── trust_gap.csv
    ├── biaya_iklan_clean.csv
    └── sumber_clean.csv
```

Data mentah tetap di `research/data/`:

| File | Isi |
|---|---|
| `makro-kalimantan.csv` | Pertumbuhan, PDRB, penduduk, UMP, IPM, internet 5 provinsi |
| `kota-kalimantan.csv` | 9 kota: penduduk, UMK, UMKM, koordinat |
| `skor-industri.csv` | 30 industri × 6 kriteria attractiveness |
| `industri-layanan.csv` | 30 industri × 2-3 layanan inti untuk skor kompetisi terukur |
| `kompetitor.csv` | 50 agency Kalimantan: layanan, kanal, harga, lokasi terverifikasi |
| `platform-indonesia.csv` | 10 platform + kategori |
| `ecommerce-indonesia.csv` | 6 marketplace/social commerce |
| `biaya-iklan.csv` | 14 benchmark CPM/CPC/CPL/retainer |
| `channel-matrix.csv` | 30 industri × 10 kanal |
| `pain-point.csv` | 53 pain point (hipotesis) |
| `persepsi.csv` | 14 dimensi trust gap (hipotesis) |
| `sumber.csv` | 30 sumber + status verifikasi |

## 3. Alur analisis

```bash
.venv/bin/python dashboard/analysis.py
```

Pipeline akan:

1. Membaca CSV dan memvalidasi kolom wajib.
2. Membersihkan tipe data (numerik, teks, tanggal).
3. Menghitung skor industri berbobot:
   `0.20 ukuran pasar + 0.20 pertumbuhan + 0.20 belanja digital + 0.15 kompetisi rendah + 0.15 akses + 0.10 margin`.
4. Menghitung prioritas pain point:
   `0.4 frekuensi + 0.4 dampak + 0.2 kesiapan bayar`.
5. Menghitung trust gap: `kepentingan - kinerja agency`.
6. Mengagregasi kompetitor: kota, tipe, layanan, transparansi harga.
7. Menulis `dashboard/data/derived/*.csv` dan `metrics.json`.

## 4. Tab dashboard

| Tab | Isi |
|---|---|
| **Industri Winning** | Scatter attractiveness, ranking, radar, dan tabel industri prioritas inti + prioritas |
| **Pain Point Owner** | Bubble 53 pain point, 12 prioritas, tabel per segmen |
| **Industri Potensial** | Scatter, ranking, radar, dan tabel industri kategori potensial |
| **Kompetitor Agency** | Sebaran kota Kalimantan, lokal vs nasional, matrix layanan, 50 agency dengan lokasi terverifikasi, sinyal harga |
| **Layanan Winning** | Tangga paket, paket per industri, add-on, layanan terlaris, benchmark retainer |
| **Sosial Media** | Platform, e-commerce, benchmark biaya iklan, heatmap 10 kanal |
| **Persepsi Agency** | Trust gap 14 dimensi, gap terbesar, tabel prioritas perbaikan |
| **Ringkasan** | KPI, pertumbuhan ekonomi, penetrasi internet, platform, ranking industri |
| **Pasar Kota** | Peta 9 kota, penduduk, UMK, UMKM, tabel status data |
| **Metodologi** | Alur, data dictionary, 30 sumber, tombol re-run |

## 5. Catatan penting

- **Pain point, persepsi, skor industri, dan channel matrix masih hipotesis.** Dashboard menandainya secara eksplisit. Ganti dengan data lapangan saat validasi dijalankan.
- **Benchmark biaya iklan & e-commerce adalah estimasi pasar**, bukan data akun campaign.
- **Harga kompetitor adalah sinyal publik**, bukan quotation resmi.
- **UMKM kota belum lengkap**; hanya 4 kota yang punya angka terdata.
- **IMPOST Media dikecualikan** dari daftar kompetitor karena merupakan entitas yang melakukan riset.
- Untuk menambah kompetitor/kota/industri: edit CSV di `research/data/`, lalu klik **Jalankan ulang analisis** di tab Metodologi.

## 6. Deploy (opsional)

Streamlit Community Cloud:

1. Push repo ke GitHub.
2. Pilih `dashboard/app.py` sebagai entry point.
3. Set Python 3.12.
4. Tidak ada secret yang dibutuhkan.

Untuk server internal:

```bash
.venv/bin/streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```
