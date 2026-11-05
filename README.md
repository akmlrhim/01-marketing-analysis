# Riset Pasar Agency Digital Marketing Kalimantan

Repositori ini berisi riset pasar dan dashboard interaktif untuk membantu keputusan digital marketing di Kalimantan.

Isi utama:

- `research/` - laporan riset dan dataset mentah CSV
- `dashboard/` - aplikasi Streamlit + pipeline analisis
- `graphify-out/` - knowledge graph proyek

Dashboard mencakup **11 tab dan 27 grafik**: Industri Winning, Pain Point Owner, Industri Potensial, Kompetitor Agency, Layanan Winning, Layanan IMPOST, Sosial Media, Persepsi Agency, Ringkasan, Pasar Kota, dan Metodologi.

---

## 1. Prasyarat

- Python **3.12**
- `uv` (direkomendasikan) atau `python3.12 -m venv`
- Browser modern
- Koneksi internet untuk tile peta OpenStreetMap

Cek Python:

```bash
python3.12 --version
```

Jika `python3.12` belum ada, gunakan `uv` untuk mengunduh Python secara otomatis.

---

## 2. Menjalankan cepat

### WSL / Linux

`.venv` yang ada di project ini adalah virtual environment **Linux/WSL**. Dari terminal WSL:

```bash
cd /mnt/e/DataAnalyst/marketing-analysis
.venv/bin/streamlit run dashboard/app.py
```

Buka `http://localhost:8501`. Hentikan dengan `Ctrl+C`.

### Windows CMD / PowerShell

Jangan memakai `.venv/bin/...` dari CMD. Buat venv Windows terpisah:

```bat
cd /d E:\DataAnalyst\marketing-analysis
py -3.12 -m venv .venv-win
.venv-win\Scripts\activate
python -m pip install --upgrade pip
pip install -r dashboard\requirements.txt
streamlit run dashboard\app.py
```

Buka `http://localhost:8501`.

> Penting: `.venv` (tanpa `-win`) dibuat di WSL/Linux, sehingga tidak bisa dipakai dari Windows CMD. Gunakan `.venv-win` untuk Windows.

### Deploy ke Streamlit Community Cloud

Repositori ini siap deploy tanpa perubahan tambahan:

1. Push repo ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io) > **Create app** > pilih repo ini.
3. Isi konfigurasi:
   - **Main file path**: `dashboard/app.py`
   - **Python version**: 3.12 (sudah dikunci lewat file `.python-version`)
4. Klik **Deploy**.

Dependensi dibaca otomatis dari `dashboard/requirements.txt`, tema dari
`.streamlit/config.toml` di root repo. Pipeline analisis (`dashboard/analysis.py`)
dijalankan otomatis oleh aplikasi saat pertama kali dimuat, jadi tidak perlu
langkah build tambahan.

---

## 3. Setup pertama kali

Jika `.venv` belum ada atau dependencies berubah:

```bash
cd /mnt/e/DataAnalyst/marketing-analysis

# buat virtual environment Python 3.12
uv venv --python 3.12 .venv

# install dependencies
uv pip install --python .venv/bin/python -r dashboard/requirements.txt
```

Alternatif tanpa `uv`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

---

## 4. Menjalankan di WSL

Jika memakai WSL dan browser Windows tidak terbuka otomatis:

```bash
.venv/bin/streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```

Lalu buka `http://localhost:8501` di browser Windows.

Jika masih tidak bisa diakses, cek IP WSL:

```bash
hostname -I
```

Buka `http://<IP-WSL>:8501`.

---

## 5. Menjalankan di Windows (tanpa WSL)

Gunakan virtual environment terpisah bernama `.venv-win`, karena `.venv` yang ada adalah milik WSL/Linux.

Dari PowerShell atau CMD di root project:

```bat
cd /d E:\DataAnalyst\marketing-analysis
py -3.12 -m venv .venv-win
.venv-win\Scripts\activate
python -m pip install --upgrade pip
pip install -r dashboard\requirements.txt
streamlit run dashboard\app.py
```

Buka `http://localhost:8501`.

Jika `py` tidak tersedia:

```bat
python --version
python -m venv .venv-win
.venv-win\Scripts\activate
pip install -r dashboard\requirements.txt
streamlit run dashboard\app.py
```

---

## 6. Alur analisis data

Dashboard membaca CSV dari `research/data/`, lalu pipeline `dashboard/analysis.py`:

1. Memvalidasi kolom wajib.
2. Membersihkan tipe data.
3. Menghitung skor industri berbobot.
4. Menghitung prioritas pain point.
5. Menghitung trust gap persepsi.
6. Mengagregasi kompetitor, kota, platform, dan benchmark iklan.
7. Menulis output ke `dashboard/data/derived/`.

Jalankan manual:

```bash
# WSL / Linux
.venv/bin/python dashboard/analysis.py
```

```bat
:: Windows
.venv-win\Scripts\python dashboard\analysis.py
```

Output utama:

```text
dashboard/data/derived/
├── metrics.json
├── kota_clean.csv
├── industri_rank.csv
├── kompetitor_clean.csv
├── harga_kompetitor.csv
├── pain_priority.csv
├── trust_gap.csv
├── layanan_winning.csv
├── layanan_industri.csv
├── layanan_addon.csv
├── impost_layanan.csv
├── biaya_iklan_clean.csv
└── sumber_clean.csv
```

Setelah data berubah, dashboard juga bisa dihitung ulang lewat tombol **Jalankan ulang analisis** di tab **Metodologi**.

---

## 7. Metodologi dan asal data

Dashboard memakai dua lapis data yang harus dibaca dengan cara berbeda.

### 7.1 Data sekunder (bisa dilacak)

| Dataset | Metode | Sumber | Status |
|---|---|---|---|
| Makro 5 provinsi | Desk research | BPS, APJII, Kemnaker, DataReportal | Terverifikasi atau Desk |
| 9 kota | Desk research | BPS, Dukcapil, pemerintah daerah | Terverifikasi atau Desk |
| 50 kompetitor Kalimantan | Audit publik | Website, profil, LinkedIn, halaman kota | Terverifikasi |
| Platform dan e-commerce | Kajian laporan publik | DataReportal 2026, APJII 2025 | Desk atau estimasi |
| Benchmark biaya iklan | Range pasar | Benchmark publik 2025 | Estimasi |
| Paket layanan | Sintesis riset internal | `research/06-layanan-winning.md` | Usulan |

Setiap baris di CSV menyimpan asal datanya di kolom `sumber`, `status_data`, atau `status_verifikasi`. Daftar 40 sumber lengkap dengan URL ada di `research/data/sumber.csv`.

#### Kriteria masuk data kompetitor

`research/data/kompetitor.csv` hanya memuat agency yang lolos salah satu dari dua syarat:

1. **Lokal Kalimantan**: kantor, domisili pendiri, atau basis operasi berada di Kalimantan. Dicek lewat halaman kontak, LinkedIn, atau bio profil resmi.
2. **Nasional yang menyasar Kalimantan**: punya halaman layanan khusus kota Kalimantan (mis. `/jasa-digital-marketing-banjarmasin`), jadi benar-benar bersaing di pasar ini.

Agency luar Kalimantan yang tidak punya jejak di pasar Kalimantan dikeluarkan. Setiap baris menyimpan `lokasi_terverifikasi` dan `bukti_lokasi` supaya klaim lokasinya bisa dicek ulang. Script auditnya ada di `scripts/verify_kompetitor.py`.

##### Sumber dan alat pencarian

Perluasan dataset dari 32 ke 50 agency memakai tiga jalur:

| Alat | Dipakai untuk | Catatan |
|---|---|---|
| **Bright Data** | Google Maps lewat scraping browser, Google SERP, scrape halaman | Dataset Google Maps terstruktur gagal total (6 error, 0 rekaman), jadi dipakai browser langsung |
| **Tavily** | Verifikasi lokasi, LinkedIn, Instagram, Facebook | Paling andal untuk memastikan kota dan badan usaha |
| **Firecrawl** | Scrape situs yang menolak fetch biasa | Dipakai lewat REST API dengan kunci dari `.env` |

Direktori pihak ketiga seperti daftar "Top 10" dari AAMAX **tidak dipakai**. Isinya template AI: nama "agency" yang muncul hanya kategori generik seperti "Balikpapan Digital Solutions" dan "Energy Sector Marketing", bukan perusahaan nyata.

##### Tingkat keyakinan

Kolom `status_verifikasi` membedakan tiga tingkat:

| Status | Arti | Jumlah |
|---|---|---|
| **Terverifikasi** | Ada situs atau badan usaha dengan alamat dan layanan yang bisa dibaca | 26 |
| **Profil publik** | Ada profil resmi (Instagram, Facebook, Google Maps) dengan kota yang jelas | 19 |
| **Perlu verifikasi** | Jejak publik minim; lokasi dari direktori atau profil karyawan | 5 |

Baris berstatus **Perlu verifikasi** sebaiknya dicek ulang sebelum dipakai untuk keputusan harga atau positioning.

Contoh kasus yang pernah salah masuk: Vodeco (Slawi/Semarang, Jawa Tengah) dan Lenteraweb (Kediri, Jawa Timur) sebelumnya diberi label lokal Banjarmasin dan Pontianak. Keduanya tetap dimasukkan, tetapi sekarang berstatus **nasional** karena memang menyasar kota Kalimantan. Peter&Co (Singapura, Jakarta, Bandung) dan Rocket Digital (Jakarta) dikeluarkan karena tidak menyasar Kalimantan sama sekali.

### 7.2 Data hipotesis (skor analis)

Angka 1 sampai 5 pada dataset berikut bukan hasil survei. Metodenya adalah desk research terstruktur ditambah penilaian analis (expert judgment).

- **Skor industri**: enam kriteria dinilai 1 sampai 5, lalu ditimbang:
  `0.20 ukuran pasar + 0.20 pertumbuhan + 0.20 belanja digital + 0.15 kompetisi rendah + 0.15 akses + 0.10 margin retainer`.
  Ambang prioritas: 3,50 ke bawah potensial, di atas 3,50 sampai 3,80 prioritas, di atas 3,80 prioritas inti.
- **Pain point**: tiga skor 1 sampai 5, lalu ditimbang:
  `0.4 frekuensi + 0.4 dampak + 0.2 kesiapan bayar`.
  Kuadran kritis jika frekuensi dan dampak sama-sama 4 atau lebih.
- **Persepsi agency**: skor kepentingan dan kinerja 1 sampai 5, lalu `gap = kepentingan - kinerja`.
- **Channel matrix**: 30 industri x 10 kanal, masing-masing dinilai 1 sampai 5.
- **Paket layanan**: usulan harga dari riset layanan, bukan hasil survei harga.

Rumus di atas dijalankan di `dashboard/analysis.py`. Setiap baris diberi label `Hipotesis` atau `status_data = Hipotesis analis`.

### 7.3 Kriteria kompetisi versi terukur

Kriteria `kompetisi_rendah` punya dua versi yang bisa dipilih di sidebar lewat **Dasar skor industri**.

**Versi hipotesis** (default): angka 1-5 di `skor-industri.csv`, penilaian analis.

**Versi terukur**: dihitung dari 50 agency Kalimantan dan tidak memakai penilaian manual.

1. Setiap agency diberi bobot kekuatan:
   `1 + 0,5 (status terverifikasi) + 0,5 (jumlah layanan ÷ 5)`.
2. Setiap kategori layanan dihitung pasokannya: jumlah bobot agency yang menjual layanan itu.
   Contoh: SMM/Konten 26 agency, Website 20, Ads 15, Cyber Security 1.
3. Setiap industri punya 2-3 layanan inti di `research/data/industri-layanan.csv`.
4. `cakupan_pesaing` = rata-rata pasokan layanan inti ÷ pasokan terbesar.
5. `kompetisi_terukur` = `1 + 4 × (1 - cakupan_pesaing)`.
   Skor 5 berarti paling sedikit pesaing, skor 1 berarti paling padat.
6. Skor akhir dihitung ulang dengan bobot yang sama, hanya kolom kompetisi yang diganti.

Hasilnya: 10 industri naik peringkat, 15 turun, 5 tetap. Perubahan terbesar adalah Elektronik & gadget naik 6 peringkat dan Properti komersial & coworking turun 10 peringkat. Prioritas inti menyusut dari 5 menjadi 4 industri.

Yang masih penilaian analis di versi ini: pemetaan industri ke layanan inti (`industri-layanan.csv`) dan lima kriteria lainnya. Hanya kriteria kompetisi yang benar-benar dihitung dari data kompetitor.

### 7.4 Cara membaca skor hipotesis

Skor 5 pada frekuensi berarti "menurut penilaian analis, ini sangat sering", bukan "5 dari 5 responden mengatakan sering". Tidak ada responden, sampling acak, uji signifikansi, atau uji reliabilitas antar-penilai. Data ini hanya layak untuk prioritisasi awal, belum layak menjadi klaim pasar.

Label hipotesis di dashboard, kolom status di CSV, dan `data_status` di `metrics.json` sengaja dipertahankan sampai ada data lapangan.

### 7.5 Menaikkan kualitas bukti

1. **Triangulasi data internet**: volume pencarian, ulasan Google Maps, diskusi forum dan komunitas, harga publik. Status bisa naik dari hipotesis menjadi indikasi awal, tetapi tetap tidak representatif.
2. **Validasi lapangan**: wawancara dan survei dengan responden nyata. Instrumen harus disusun ulang karena dokumen instrumen sudah dihapus.
3. **Bukti per baris**: tambahkan kolom `metode` dan `url_bukti` di CSV, lalu tampilkan di dashboard.

---

## 8. Mengubah data

Edit CSV di `research/data/`:

| File | Isi |
|---|---|
| `makro-kalimantan.csv` | Data makro 5 provinsi |
| `kota-kalimantan.csv` | 9 kota: penduduk, UMK, UMKM, koordinat |
| `skor-industri.csv` | 30 industri × 6 kriteria |
| `industri-layanan.csv` | 30 industri × 2-3 layanan inti (dasar skor kompetisi terukur) |
| `kompetitor.csv` | 50 agency Kalimantan + lokasi terverifikasi |
| `platform-indonesia.csv` | 10 platform |
| `ecommerce-indonesia.csv` | 6 marketplace/social commerce |
| `biaya-iklan.csv` | 14 benchmark biaya iklan |
| `channel-matrix.csv` | 30 industri × 10 kanal |
| `pain-point.csv` | 53 pain point |
| `persepsi.csv` | 14 dimensi trust gap |
| `layanan-winning.csv` | 5 paket layanan + harga |
| `layanan-industri.csv` | 4 paket per industri + KPI |
| `layanan-addon.csv` | 5 add-on + harga |
| `impost-layanan.csv` | 11 layanan IMPOST: harga pasar vs harga ideal + demand per wilayah |
| `sumber.csv` | 40 sumber |

Setelah edit:

```bash
.venv/bin/python dashboard/analysis.py
```

lalu refresh browser.

---

## 9. Struktur project

```text
marketing-analysis/
├── README.md
├── research/
│   ├── README.md
│   ├── 01-rancangan-riset.md
│   ├── 02-industri-winning-potensial.md
│   ├── 03-kompetitor-agency.md
│   ├── 04-pain-point-persepsi.md
│   ├── 05-media-sosial-kalimantan.md
│   ├── 06-layanan-winning.md
│   ├── 08-deck-ringkas.md
│   └── data/
├── dashboard/
│   ├── app.py
│   ├── analysis.py
│   ├── requirements.txt
│   ├── README.md
│   └── data/derived/
└── graphify-out/
```

---

## 10. Troubleshooting

### `'.venv' is not recognized` di Windows CMD

Itu terjadi karena `.venv/bin/...` adalah path Linux/WSL. Di Windows gunakan:

```bat
.venv-win\Scripts\activate
streamlit run dashboard\app.py
```

atau langsung:

```bat
.venv-win\Scripts\streamlit run dashboard\app.py
```

### `'run' is not recognized`

Perintahnya kurang `streamlit`. Yang benar:

```bat
streamlit run dashboard\app.py
```

bukan:

```bat
run dashboard/app.py
```

### `streamlit: command not found`

Gunakan path venv:

```bash
.venv/bin/streamlit run dashboard/app.py
```

atau aktifkan venv dulu:

```bash
source .venv/bin/activate
streamlit run dashboard/app.py
```

### `ModuleNotFoundError: No module named 'plotly'`

Error di `dashboard/app.py` baris `import plotly.express as px` berarti package
`plotly` belum terpasang di Python yang dipakai Streamlit.

Pastikan Anda memakai venv Windows:

```bat
cd /d E:\DataAnalyst\marketing-analysis
py -3.12 -m venv .venv-win
.venv-win\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r dashboard\requirements.txt
```

Cek instalasi:

```bat
python -c "import streamlit, pandas, plotly, numpy; print('plotly', plotly.__version__)"
```

Lalu jalankan:

```bat
streamlit run dashboard\app.py
```

Prompt CMD harus menampilkan `(.venv-win)` sebelum menjalankan perintah.

### `ModuleNotFoundError` lainnya

Install ulang dependencies:

```bash
# WSL / Linux
uv pip install --python .venv/bin/python -r dashboard/requirements.txt
```

```bat
:: Windows
.venv-win\Scripts\python -m pip install -r dashboard\requirements.txt
```

### Port 8501 sudah dipakai

Pakai port lain:

```bash
.venv/bin/streamlit run dashboard/app.py --server.port 8502
```

lalu buka `http://localhost:8502`.

### Peta tidak muncul

Peta memakai tile OpenStreetMap dan membutuhkan koneksi internet. Grafik lain tetap berjalan tanpa peta.

### Data tidak berubah setelah CSV diedit

Klik **Jalankan ulang analisis** di tab **Metodologi**, atau restart:

```bash
# Ctrl+C, lalu
.venv/bin/streamlit run dashboard/app.py
```

### Dashboard menampilkan peringatan hipotesis

Itu memang disengaja. Pain point, persepsi, skor industri, dan channel matrix masih **hipotesis** sampai validasi lapangan dijalankan. Benchmark biaya iklan dan e-commerce juga **estimasi pasar**, bukan data akun campaign.

---

## 11. Catatan data

- **IMPOST Media tidak dimasukkan** sebagai kompetitor karena merupakan entitas yang melakukan riset.
- **Harga kompetitor** adalah sinyal publik, bukan quotation resmi.
- **UMKM kota** baru terdata untuk Balikpapan, Samarinda, Banjarmasin, dan Palangka Raya.
- **Validasi lapangan** belum dijalankan; fokus saat ini pengumpulan data dari internet.

Metodologi dan asal setiap dataset dijelaskan di bagian 7.

Untuk detail dashboard, lihat `dashboard/README.md`. Untuk detail riset, lihat `research/README.md`.
