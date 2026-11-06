# Riset Pasar Agency Digital Marketing Kalimantan

**Status:** Fokus saat ini pengumpulan data dari internet (desk research). Riset primer (wawancara & survei) ditunda.
**Tanggal:** 4 November 2026
**Cakupan geografis:** Kalimantan Timur (Balikpapan, Samarinda, IKN), Kalimantan Selatan (Banjarmasin, Banjarbaru), Kalimantan Barat (Pontianak), Kalimantan Tengah (Palangka Raya), Kalimantan Utara (Tarakan, Tanjung Selor).

---

## 1. Deliverable

| File | Isi |
|---|---|
| `01-rancangan-riset.md` | Tujuan, pertanyaan riset, metode, sampling, timeline, budget, analisis |
| `02-industri-winning-potensial.md` | Data makro 5 provinsi, industri winning & potensial, skor prioritas |
| `03-kompetitor-agency.md` | Peta kompetitor, profil, matrix layanan-harga-channel, celah pasar |
| `04-pain-point-persepsi.md` | Hipotesis pain point per segmen + persepsi terhadap agency + rencana validasi |
| `05-media-sosial-kalimantan.md` | Data platform nasional & penetrasi internet Kalimantan, peran kanal per industri |
| `06-layanan-winning.md` | Paket layanan, harga, positioning, go-to-market 90 hari, KPI |
| `08-deck-ringkas.md` | Deck 12 slide untuk presentasi internal/klien |
| `data/kompetitor.csv` | Database **50 kompetitor** (38 lokal Kalimantan, 12 nasional yang menyasar Kalimantan) |
| `data/skor-industri.csv` | Skor attractiveness **30 industri** (bisa diubah bobotnya) |
| `data/industri-layanan.csv` | 30 industri × 2-3 layanan inti, dasar skor kompetisi terukur |
| `data/makro-kalimantan.csv` | Data makro 5 provinsi + penduduk, UMP, IPM |
| `data/kota-kalimantan.csv` | **9 kota**: penduduk, UMK, UMKM, koordinat |
| `data/platform-indonesia.csv` | **10 platform** + kategori & sumber |
| `data/ecommerce-indonesia.csv` | 6 marketplace/social commerce |
| `data/biaya-iklan.csv` | 14 benchmark CPM/CPC/CPL/retainer |
| `data/channel-matrix.csv` | 30 industri × 11 kanal |
| `data/pain-point.csv` | **57 pain point** (hipotesis) |
| `data/persepsi.csv` | 14 dimensi trust gap (hipotesis) |
| `data/layanan-winning.csv` | 5 paket layanan + harga bulanan |
| `data/layanan-industri.csv` | 4 paket layanan per industri + KPI |
| `data/layanan-addon.csv` | 5 add-on + harga |
| `data/sumber.csv` | 42 sumber + status verifikasi |

**Dashboard:** `dashboard/app.py` - Streamlit + Plotly, **10 tab, 25 grafik**. Cara menjalankan ada di `dashboard/README.md`.

---

## 2. Temuan kunci (ringkas)

1. **Kalimantan tumbuh di atas nasional, tapi tidak merata.** Ekonomi pulau tumbuh 5,43% (2024) vs nasional 5,03%; konstruksi melesat 15,82% karena IKN. Kaltim paling agresif di 2024 (6,17%) lalu melambat di 2025 (4,53%), Kalbar tumbuh tertinggi di 2025 (5,39%), Kalsel 5,22% (2025), Kalteng 4,80% (2025), Kaltara 4,56% (2025).
2. **Mesin pertumbuhan riil ada di 4 klaster:** (a) konstruksi-properti-infrastruktur IKN, (b) logistik & perdagangan, (c) F&B/retail/kuliner kota, (d) hilirisasi sawit & tambang. Jasa pendidikan, kesehatan, dan wisata ikut naik.
3. **Balikpapan adalah pasar UMKM terpadat:** ~98 ribu UMKM akhir 2025, hampir 40% kuliner. Ini pasar volume untuk paket entry, bukan paket korporat.
4. **TikTok = kanal dengan jangkauan terbesar** (180 juta akun 18+), disusul YouTube (151 juta), Facebook (121 juta), Instagram (108 juta). Untuk bisnis lokal, kombinasi realistis: **IG + TikTok + WhatsApp + Google Maps**, dengan Facebook masih relevan untuk segmen 35+.
5. **Penetrasi internet Kalimantan tidak identik dengan kualitas pasar.** Kalteng (89,57%) dan Kaltim (88,33%) masuk 10 besar nasional; Kalbar 79,37%; Kaltara 70,15%; **Kalsel justru 64,67% (peringkat 35 dari 38)**. Artinya Kalsel butuh pendekatan offline-hybrid, bukan digital-first murni.
6. **Kompetitor lokal kuat di relationship & produksi konten, lemah di strategi, pengukuran, dan transparansi harga.** Dari **50 kompetitor** yang dipetakan (38 lokal Kalimantan, 12 nasional yang menyasar Kalimantan), hanya **5 yang membuka sinyal harga publik**. Pemain nasional menyerang lewat halaman SEO "jasa digital marketing + nama kota" dan pricelist terbuka.
7. **Celah terbesar: performance + CRM/WhatsApp + pelaporan revenue, bukan sekadar konten.** Hampir tidak ada agency lokal yang menjual "lead ke closing" sebagai sistem. Ini peluang positioning yang sulit ditiru agency konten.
8. **Pasar kota terkonsentrasi di 4 kota:** Samarinda (893 rb jiwa), Balikpapan (757 rb), Pontianak (683 rb), Banjarmasin (682 rb). Balikpapan punya UMKM terdata terbesar (±98 ribu), tetapi UMK tertinggi ada di Tarakan (Rp4,74 jt).
9. **Persepsi negatif yang harus dilawan:** "agency cuma bikin feed cantik", "mahal tapi tidak ada penjualan", "laporan PDF tidak bisa diverifikasi", "agency Jakarta tidak paham lokal". Pemenang adalah yang bisa membuktikan **biaya per lead, waktu respons, dan kontribusi revenue**.

---

## 3. Rekomendasi eksekusi (30-90 hari)

1. **Fokus geografis:** Balikpapan + Samarinda dulu (IKN spillover, penetrasi internet tinggi, UMKM padat), lalu Banjarmasin dan Pontianak.
2. **Fokus industri:** properti/developer, F&B, klinik/kesehatan, pendidikan, dan B2B industrial (logistik, pertambangan, sawit).
3. **Produk unggulan:** "Local Growth System" - konten + iklan + WhatsApp CRM + dashboard lead, dengan pilot 60 hari dan KPI biaya per lead.
4. **Pricing:** entry 2,5-3,5 jt/bln; core 6-9 jt/bln; premium 15-30 jt/bln; ads fee 2-3 jt + 3-5% ad spend.
5. **Go-to-market:** audit gratis + workshop UMKM bersama Kadin/HIPMI/bank daerah + studi kasus lokal + landing page per kota/per industri.

---

## 4. Batasan data

- **Desk research only.** Pain point dan persepsi di dokumen `04` masih **hipotesis**. Validasi lapangan ditunda sampai pengumpulan data internet selesai.
- **Harga kompetitor** sebagian besar tidak dipublikasikan. Angka yang tercantum adalah sinyal harga publik (pricelist/website) atau benchmark nasional, bukan quotation resmi.
- **Bright Data MCP aktif** memakai `BRIGHTDATA_API_KEY` dari `.env`, sehingga scraping Google Maps/Instagram bisa dijalankan. Dataset awal tetap diperluas memakai **Tavily search/extract** untuk website kompetitor, direktori, dan data pemerintah; setiap baris diberi status verifikasi.
- **Sociality MCP sudah dihapus** dari konfigurasi, sehingga tidak ada sumber data social listening/analytics.
- **UMKM kota belum lengkap**: hanya Balikpapan, Samarinda, Banjarmasin, dan Palangka Raya yang punya angka terdata; kota lain dikosongkan, bukan diestimasi.
- **Benchmark biaya iklan & e-commerce adalah estimasi pasar**, bukan data akun campaign. Validasi dengan data aktual sebelum dipakai untuk pricing.
- Data BPS/BI antarprovinsi punya tahun berbeda (2024 vs 2025); setiap angka diberi label tahun agar tidak salah banding.

---

## 5. Dashboard

```bash
.venv/bin/streamlit run dashboard/app.py
```

Buka `http://localhost:8501`. Tab: **Industri Winning, Pain Point Owner, Industri Potensial, Kompetitor Agency, Layanan Winning, Layanan IMPOST, Sosial Media, Persepsi Agency, Pasar Kota, Metodologi**. Pipeline analisis ada di `dashboard/analysis.py` dan menghasilkan ulang CSV + `metrics.json` di `dashboard/data/derived/`.

Dashboard mencakup peta 9 kota, 50 kompetitor Kalimantan, 30 industri, 57 pain point, 14 benchmark biaya iklan, 10 platform, 6 marketplace, dan daftar 42 sumber dengan status verifikasi.

---

## 6. Sumber utama

- BPS Provinsi Kaltim, Kalsel, Kalteng, Kalbar, Kaltara (PDRB & pertumbuhan ekonomi)
- Bank Indonesia - Laporan Perekonomian Provinsi (2025)
- APJII - Survei Penetrasi Internet Indonesia 2025
- DataReportal/Kepios - Digital 2026: Indonesia
- NEXT Indonesia - Kinerja Ekonomi Kalimantan (Mei 2025)
- Pemerintah Provinsi/Kota (Balikpapan, Kaltim, Kalbar, Kalteng) dan pemberitaan lokal
- Website & profil publik kompetitor (Up & Away, Codezy, Wemember Digital, DNA Indonesia, EastKreatif, Karya Studio, Vodeco, Lenteraweb, dll.)
- **Catatan:** IMPOST Media tidak dimasukkan sebagai kompetitor karena merupakan entitas yang melakukan riset ini.

Daftar URL lengkap ada di bagian "Sumber" setiap dokumen.
