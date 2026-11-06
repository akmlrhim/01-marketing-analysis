# KNOWLEDGE.md - Cara Angka, Bobot, dan Skor Hipotesis Dibuat

Dokumen ini menjelaskan **dari mana setiap angka berasal dan bagaimana angka itu dihitung**,
termasuk metode standar yang diadopsi untuk tiap rumus (dirangkum di bagian 11).
Target pembacanya: orang yang ingin mengecek, mempertahankan, atau mengkritik angka di
dashboard dan CSV tanpa harus menebak cara angkanya lahir.

**Proyek ini punya dua lapis angka yang tidak boleh dicampur.**

| Lapis                       | Contoh                                                               | Cara mendapatkan angka                                                                                   | Status                                                       |
| --------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Lapis 1: data sekunder**  | PDRB, penduduk, penetrasi internet, jumlah agency, harga kompetitor  | Kutip dari publikasi resmi (BPS, APJII, DataReportal) atau audit publik (website, Google Maps, LinkedIn) | Bisa dilacak ke URL                                          |
| **Lapis 2: skor hipotesis** | Skor 1-5 industri, pain point, persepsi, channel matrix, harga paket | Penilaian analis (expert judgment) di atas bukti desk research                                           | Tidak ada responden; label `Hipotesis` sengaja dipertahankan |

---

## 1. Proses umum: bagaimana sebuah angka hipotesis lahir

Setiap skor 1-5 di dataset ini dibuat lewat lima langkah yang sama. Tidak ada angka
yang "dikarang langsung" tanpa melewati langkah-langkah ini.

### Langkah 1 - Kumpulkan bukti desk research dulu

Sebelum menilai, semua yang bisa dikutip dikumpulkan dulu:

- Data makro: BPS (PDRB, pertumbuhan), APJII 2025 (penetrasi internet), DataReportal
  Digital 2026 (platform), Bank Indonesia (laporan perekonomian provinsi).
- Data kota: BPS, Dukcapil, situs pemda (penduduk, UMK, UMKM).
- Kompetitor: audit publik 50 agency lewat Google SERP, Google Maps (Bright Data),
  verifikasi lokasi/LinkedIn (Tavily), dan scrape situs yang menolak fetch biasa
  (Firecrawl). Direktori "Top 10" pihak ketiga **tidak dipakai** karena isinya template AI.
- Sinyal harga: pricelist publik kompetitor dan benchmark nasional.

Semua URL tersimpan di `research/data/sumber.csv` (42 sumber).

### Langkah 2 - Tentukan kriteria dan bobotnya

Kriteria dipilih hanya jika menjawab satu pertanyaan bisnis: _"industri/pain point ini
layak diprioritaskan atau tidak untuk agency kecil di Kalimantan?"_
Bobot ditetapkan sekali di awal (rasionalenya di bagian 2 dan 4), lalu **tidak diubah
per industri** - supaya perbandingan antar baris adil.

### Langkah 3 - Definisikan anchor skala 1-5

Angka 1-5 bukan perasaan bebas. Setiap kriteria punya definisi "1 artinya apa, 5 artinya
apa" (daftar lengkap di bagian 3). Anchor ini membuat dua orang berbeda berdebat tentang
bukti, bukan tentang makna angka.

### Langkah 4 - Nilai satu per satu dengan bukti sebagai pembatas

Saat menilai satu baris (misal industri "Logistik"), yang dibaca adalah bukti dari
langkah 1: sektor ini tumbuh berapa persen, ada berapa agency yang menyasar, siklus
jualnya B2B atau B2C, lalu angka 1-5 dipilih dengan anchor sebagai penggaris.
Kolom `catatan` di CSV adalah jejak alasan penilaian tersebut.

### Langkah 5 - Hitung skor akhir dengan rumus, bukan dengan perasaan

Skor gabungan selalu dihitung oleh kode (`dashboard/analysis.py`), bukan diketik manual.
CSV menyimpan skor mentah 1-5 per kriteria; dashboard menghitung skor tertimbang,
peringkat, dan kategori. Contoh perhitungan utuh ada di bagian 8.

### Kenapa metode ini dipakai (dan apa konsekuensinya)

- **Survei belum dijalankan.** Rancangan survei/wawancara sudah ada di
  `research/01-rancangan-riset.md` (3 lapis: desk → kualitatif → kuantitatif), tetapi
  baru Lapis 1 yang selesai.
- **Skor analis = hipotesis terstruktur.** Ia lebih baik dari tebakan karena ada bukti,
  anchor, dan rumus; tetapi ia **bukan** data pasar. Tidak ada sampling, tidak ada uji
  signifikansi, tidak ada uji reliabilitas antar-penilai (single rater).
- **Cara baca yang benar:** "skor 5 pada frekuensi berarti menurut penilaian analis atas
  bukti desk, pain ini sangat sering" - bukan "5 dari 5 responden mengatakan sering".

---

## 2. Skor industri: 6 kriteria × bobot

**Sumber data:** `research/data/skor-industri.csv` (30 industri).
**Perhitungan:** `score_industries()` di `dashboard/analysis.py`.

### 2.1 Rumus

```text
skor_tertimbang = 0.20 × ukuran_pasar
                + 0.20 × pertumbuhan
                + 0.20 × belanja_digital
                + 0.15 × kompetisi_rendah
                + 0.15 × akses_dan_sales_cycle
                + 0.10 × margin_retainer
```

Semua kriteria dinilai 1-5, sehingga skor akhir juga selalu berada di 1,00-5,00.

### 2.2 Kenapa bobotnya begitu (rasionalenya)

Total bobot dibagi tiga kelompok pertanyaan:

| Kelompok                | Kriteria                                   | Total bobot         | Pertanyaan yang dijawab                                 |
| ----------------------- | ------------------------------------------ | ------------------- | ------------------------------------------------------- |
| **Permintaan (demand)** | ukuran_pasar, pertumbuhan, belanja_digital | 3 × 0.20 = **0.60** | "Adakah uang di industri ini?"                          |
| **Gesekan (friction)**  | kompetisi_rendah, akses_dan_sales_cycle    | 2 × 0.15 = **0.30** | "Seberapa sulit masuk dan menutup deal?"                |
| **Kualitas pendapatan** | margin_retainer                            | **0.10**            | "Kalau menang, apakah klien bertahan dan margin sehat?" |

Alasan tiap bobot:

1. **Permintaan diberi 60%** karena bagi agency kecil, kematian terjadi karena "tidak ada
   yang beli", bukan karena kompetitor. Tiga indikator permintaan (besar, tumbuh, mau
   belanja digital) diberi bobot sama rata (0.20 masing-masing) karena tidak ada satu
   indikator pun yang cukup sendirian: pasar besar yang stagnant, pasar tumbuh tapi
   kecil, dan pasar mau digital tapi kecil - ketiganya jebakan yang berbeda.
2. **Gesekan 30%** membagi dua rintangan: dari sisi pesaing (`kompetisi_rendah`) dan dari
   sisi proses jual (`akses_dan_sales_cycle`). Bobot 0.15 masing-masing menandakan
   keduanya penting tapi bukan penentu utama - agency bisa hidup di pasar ramai kalau
   permintaannya besar (contoh: F&B).
3. **Margin/retainer hanya 10%** karena dampaknya muncul belakangan; industri bermargin
   tinggi tapi sulit diakses (tambang) tetap bukan titik masuk pertama. Bobot terkecil
   juga jujur pada fakta bahwa ini kriteria yang paling sulit diverifikasi dari luar.

### 2.3 Anchor skala 1-5 per kriteria

Tabel di bawah hanya mendefinisikan **skor 1, 3, dan 5** (metode BARS: dua ujung

- satu titik tengah). Skor **2 dan 4 tidak didefinisikan terpisah** karena
  artinya interpolasi: 2 = "di antara 1 dan 3, lebih dekat ke 1"; 4 = "di antara
  3 dan 5, lebih dekat ke 5". Tiga jangkar dipilih agar penilaian tetap konsisten
  tanpa tabel definisi yang panjang dan mudah tumpang tindih.

| Kriteria                | Skor 1                                                 | Skor 3                                  | Skor 5                                                                |
| ----------------------- | ------------------------------------------------------ | --------------------------------------- | --------------------------------------------------------------------- |
| `ukuran_pasar`          | Jumlah usaha & PDRB sektor kecil di Kalimantan         | Menengah; ada tapi tidak dominan        | Sektor PDRB besar + jumlah usaha sangat banyak (F&B, retail, tambang) |
| `pertumbuhan`           | Stagnan/menyusut                                       | Tumbuh ± sekitar rata-rata nasional     | Tumbuh jauh di atas nasional, ada pemicu jelas (IKN, hilirisasi)      |
| `belanja_digital`       | Marketing bukan prioritas; budget nol-minim            | Mulai belanja tapi kecil/per Epicentrum | Terbukti belanja iklan/konten rutin (klinik, kosmetik, properti)      |
| `kompetisi_rendah`      | Dibanjiri agency & freelancer                          | Ramai tapi masih ada celah nyata        | Hampir tak ada agency lokal yang serius menyasar                      |
| `akses_dan_sales_cycle` | Tender/procurement, gatekeeper banyak, siklus >6 bulan | Siklus sedang, perlu relasi             | B2C, keputusan owner sendiri, siklus mingguan                         |
| `margin_retainer`       | Proyek sekali, murah, churn tinggi                     | Retainer sedang                         | Retainer bulanan tinggi & sticky (klinik, properti, korporat)         |

Contoh membaca anchor: `akses_dan_sales_cycle = 1` untuk Jasa pertambangan karena
procurement-nya ketat dan decision maker bertingkat; `= 5` untuk F&B karena pemilik
warung memutuskan sendiri hari itu juga.

### 2.4 Ambang kategori prioritas

Setelah skor dihitung, dipotong dengan ambang tetap (di kode: `bins=[0, 3.5, 3.8, 5.0]`):

| Skor               | Kategori       | Makna praktis                  |
| ------------------ | -------------- | ------------------------------ |
| ≤ 3,50             | Potensial      | Pantau; belum layak jadi fokus |
| 3,50 < skor ≤ 3,80 | Prioritas      | Layak ditembus kedua           |
| > 3,80             | Prioritas inti | Fokus sumber daya utama        |

Ambang 3,50 dan 3,80 dipilih karena memisahkan distribusi skor secara alami (ada
"lompatan" di sekitar angka itu) dan sekaligus membatasi prioritas inti pada 5 industri -
jumlah yang realistis untuk kapasitas satu agency kecil.

---

## 3. Kompetisi terukur: mengganti satu angka tebakan dengan angka data

Kriteria `kompetisi_rendah` adalah satu-satunya yang punya versi hipotesis (angka 1-5
buatan analis) **dan** versi terukur (dihitung dari 50 agency). Versi terukur ada supaya
pembaca bisa melihat seberapa besar efek penilaian manual. Kode: `competitor_supply()`
dan `measured_competition()`.

### 3.1 Rumus, langkah demi langkah

**Langkah A - Bobot kekuatan tiap agency** (agency besar/terverifikasi dihitung lebih
dari satu "pesaing"):

```text
bobot_agency = 1
             + 0.5 × [status_verifikasi == "Terverifikasi"]   (0 atau 1)
             + 0.5 × (jumlah_layanan / 5)                     (dipotong maks 5)
```

Contoh: agency terverifikasi dengan 5 kategori layanan → bobot 2,0.
Agency tak terverifikasi dengan 1 layanan → bobot 1,1.

**Langkah B - Pasokan per kategori layanan.** Layanan tiap agency dideteksi dari teks
`layanan_utama` memakai regex `SERVICE_RULES` (15 kategori: SMM/Konten, Ads, Website,
Branding, dst.). Pasokan = jumlah bobot semua agency yang menjual kategori itu.
Hasilnya antara lain: SMM/Konten ±26 agency, Website ±20, Ads ±15, Cyber Security 1.

**Langkah C - Cakupan pesaing per industri.** Setiap industri punya 2-3 layanan inti di
`research/data/industri-layanan.csv` (pemetaan ini masih penilaian analis - satu-satunya
input manual yang tersisa di versi terukur):

```text
cakupan_pesaing = (rata-rata pasokan layanan inti industri) / (pasokan tertinggi)
```

Bernilai 0-1. Mendekati 1 = layanan inti industri ini dijual hampir semua agency
(pasar padat); mendekati 0 = hampir tak ada yang menjualnya.

**Langkah D - Skor kompetisi terukur:**

```text
kompetisi_terukur = 1 + 4 × (1 - cakupan_pesaing)
```

Skor 5 = paling sedikit pesaing, skor 1 = paling padat. Transformasi ini sengaja
dibuat supaya hasilnya berada di skala 1-5 yang sama dengan versi hipotesis, sehingga
bisa langsung ditukar di dalam rumus bobot tanpa mengubah bobot lain.

**Langkah E -** Hitung ulang `skor_tertimbang` dengan bobot yang sama, hanya kolom
kompetisi yang diganti, lalu bandingkan peringkat lama vs baru.

### 3.2 Hasil pembandingnya

Dari pembandingan: 10 industri naik peringkat, 15 turun, 5 tetap. Elektronik & gadget
naik 6 peringkat; Properti komersial & coworking turun 10. Prioritas inti menyusut
dari 5 menjadi 4 industri. Perbedaan ini adalah ukuran seberapa sensitif peringkat
terhadap satu kolom penilaian manual - dan alasan kedua versi tetap ditampilkan.

---

## 4. Pain point: frekuensi × dampak × kesiapan bayar

**Sumber data:** `research/data/pain-point.csv` (57 pain point, 3 segmen: UMKM, SME,
Korporat/B2B, klinik, dll).
**Perhitungan:** `pain_priority()` di `dashboard/analysis.py`.

### 4.1 Rumus

```text
skor_prioritas = 0.4 × frekuensi + 0.4 × dampak + 0.2 × kesiapan_bayar
```

### 4.2 Kenapa bobotnya begitu

1. **Frekuensi = dampak = 0.4.** Pain yang jarang tapi mematikan dan pain yang harian
   tapi ringan sama-sama tidak layak jadi produk. Yang laku dijual adalah pain yang
   **sering terjadi DAN menyakitkan** - karena itu keduanya disetara di bobot tertinggi.
2. **Kesiapan bayar = 0.2.** Paling sering ditanya tapi paling sulit diverifikasi dari
   luar (tidak ada yang publikasi willingness to pay-nya). Diberi bobot ada - karena
   pain tanpa budget hanya jadi keluhan, bukan pasar - tapi kecil, karena tingkat
   keyakinannya paling rendah.

### 4.3 Anchor skala 1-5

| Kriteria         | 1                                        | 3                                    | 5                                                                        |
| ---------------- | ---------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| `frekuensi`      | Nyaris pernah terjadi di segmen itu      | Terjadi sesekali / di sebagian kecil | Hampir semua bisnis di segmen mengalaminya berulang                      |
| `dampak`         | Gangguan ringan, mudah diabaikan         | Menyita waktu/uang tapi bisnis jalan | Kehilangan omzet nyata / bisnis bisa mati                                |
| `kesiapan_bayar` | Tidak akan pernah bayar untuk solusi ini | Bayar kalau murah/ada bukti          | Sudah sedang membayar (alat, orang, agency lain) untuk masalah yang sama |

Contoh penilaian: _"Lead masuk tapi tidak di-follow up"_ (SME) dapat 5-5-5 karena bukti
desk-nya melimpah - WhatsApp penuh chat belum dibalas, agency lokal hampir tidak menjual
CRM/lead system (data 50 kompetitor: kategori CRM/Lead paling sedikit), dan bisnis jelas
sudah membayar untuk iklan yang menghasilkan lead itu sendiri.

### 4.4 Kuadran (aturan potong di kode)

Kuadran dihitung dari aturan tegas di dua kolom mentah, bukan dari skor gabungan:

| Kondisi                          | Kuadran            |
| -------------------------------- | ------------------ |
| frekuensi ≥ 4 **dan** dampak ≥ 4 | **Kritis**         |
| frekuensi ≥ 4 dan dampak < 4     | Sering tapi ringan |
| frekuensi < 4 dan dampak ≥ 4     | Jarang tapi berat  |
| lainnya                          | Monitor            |

Ambang 4 dipilih karena pada skala 1-5, angka 4 berarti "masalah nyata yang berulang",
bukan keluhan kecil.

---

## 5. Persepsi agency (trust gap)

**Sumber data:** `research/data/persepsi.csv` (14 dimensi).
**Perhitungan:** `trust_gap()` di `dashboard/analysis.py`.

### 5.1 Rumus

```text
gap = kepentingan - kinerja_agency
```

- `kepentingan` (1-5, boleh 0,5 karena perbandingan antar dimensi): seberapa penting
  dimensi ini menurut analis bagi keputusan owner memilih/menyalahkan agency.
- `kinerja_agency` (1-5): seberapa baik rata-rata agency Kalimantan (dari 50 yang
  diaudit) tampil pada dimensi itu.
- Gap positif besar = harapan tinggi tapi pasar kecewa = **peluang positioning**.

### 5.2 Cara penilaiannya

`kepentingan` dinilai dari pola keluhan yang berulang di desk research (ulasan, grup
bisnis lokal, pengalaman klien yang dipublikasikan). `kinerja_agency` dinilai dari
audit 50 kompetitor: apakah mereka mempublikasi laporan terukur, harga transparan,
studi kasus, kecepatan respons, dsb.

Contoh: **Bukti hasil yang terukur** kepentingan 5,0 vs kinerja 2,5 → gap **2,5** (terbesar), disusul **Akuntabilitas KPI** 4,7 vs 2,3 → gap **2,4**.
Kebalikannya, **Kehadiran lokal** 4,0 vs 3,8 → gap 0,2: agency lokal sudah kuat di sini,
tidak perlu dijadikan positioning utama.

---

## 6. Channel matrix: 30 industri × 11 kanal

**Sumber data:** `research/data/channel-matrix.csv`.
Perhitungan hanya agregasi sederhana (rata-rata per industri untuk mengurutkan).

### 6.1 Cara angkanya dibuat

Setiap sel dinilai 1-5 dengan satu pertanyaan: _"seberapa efektif kanal ini untuk
menjual ke industri ini di kota Kalimantan?"_ Tiga masukan yang dipakai:

1. **Perilaku kanal:** jangkauan platform (TikTok 180 jt, YouTube 151 jt, Facebook
   121 jt, Instagram 108 jt - DataReportal Digital 2026) dan penetrasi internet
   provinsi (APJII 2025).
2. **Sifat pembelian industri:** B2C cepat → skor tinggi di TikTok/IG/Maps; B2B
   relationship → skor tinggi di WhatsApp/LinkedIn/Google Search, rendah di TikTok.
3. **Pola kompetitor:** kanal yang aktif dipakai agency pemenang (dari audit 50 agency).

Anchor umum: **5** = kanal utama, wajib ada; **3** = pendukung; **1** = hampir tak
berguna. Contoh: Jasa pertambangan dapat `tiktok=1, whatsapp=5, linkedin=5`;
F&B dapat `tiktok=5, instagram=5, google_maps=5`.

Kanal `ai_search` (ditambahkan 2026-11-06) menangkap pencarian lewat asisten AI
(ChatGPT, AI Overviews, dsb) yang kini jadi pintu masuk calon klien menemukan
agency. Skornya diturunkan dari `google_search` dengan aturan tetap
`clamp(round(google_search × 0.8))`: perilaku dasarnya sama dengan pencarian
Google, tetapi didiskon 20% karena adopsi asisten AI oleh pemilik usaha di
Kalimantan masih awal (hipotesis; naikkan manual saat ada bukti adopsi lokal).

---

## 7. Harga paket layanan

**Sumber data:** `research/data/layanan-winning.csv`, `layanan-industri.csv`,
`layanan-addon.csv`. Status: **usulan**, bukan hasil survei harga.

### 7.1 Cara angka rupiahnya diturunkan

Harga disusun dengan tiga jangkar, lalu diposisikan di antaranya:

1. **Sinyal harga publik kompetitor.** Dari 50 agency, hanya ±5 yang membuka harga
   (kolom `harga_transparan` dideteksi otomatis dari teks `sinyal_harga`: mengandung
   "rp/rb/jt/juta" dan TIDAK mengandung "tidak publik/via wa/gaji").
2. **Benchmark biaya iklan nasional 2025** (`biaya-iklan.csv`, 14 baris CPM/CPC/CPL) -
   dipakai untuk menakar berapa volume kerja yang mampu dibeli budget tertentu.
3. **Daya beli kota:** UMK kota (`kota-kalimantan.csv`) dan struktur omzet target
   per tier (<50 jt, 50-250 jt, >250 jt per bulan).

Aturan praktis yang dipakai: retainer entry ±10-15% dari omzet bulanan target; paket
naik ±2,5× per tingkatan (Ignite 2,5 jt → Growth 6,5 jt → Market Leader 15 jt →
Enterprise 25 jt+). Angka dibulatkan ke "harga psikologis" pasar (2,5 / 6,5 / 15 / 25).

### 7.2 Status yang jujur

Ini **usulan harga yang harus diuji**, bukan titik ekuilibrium pasar. Rencana
validasinya sudah disiapkan: Van Westendorp Price Sensitivity Meter di survei
(`research/01-rancangan-riset.md` §4 dan §8).

### 7.3 Harga & demand layanan IMPOST per wilayah (scope tambahan)

**Sumber data:** `research/data/impost-layanan.csv` (13 layanan IMPOST),
`research/data/scraping/demand-ringkas.csv` (sinyal pencarian per wilayah).
Ditampilkan di dashboard tab **Layanan IMPOST**.

Dua kolom harga, dua status:

1. **Harga pasar** (`harga_pasar_min_rp`-`harga_pasar_max_rp`) - Lapis 1: dirangkai
   dari sinyal publik kompetitor (publish.co.id Rp980 rb, WebNesia Rp2,1 jt,
   etnicode Rp10-50 jt, corefreelancers Rp500 rb), benchmark `biaya-iklan.csv` dan
   `layanan-addon.csv`, plus validasi web via MCP/Tavily yang tersimpan sebagai
   sumber S31-S40 di `sumber.csv` (GroupM: belanja iklan Indonesia US$6,4 M
   tumbuh 9,5% di 2025, 75% digital; Dentsu; PwC; Depotkamera; EverHelp).
2. **Harga ideal** (`harga_ideal_min_rp`-`harga_ideal_max_rp`) - Lapis 2 hipotesis:
   usulan harga IMPOST dengan jangkar yang ditulis di kolom `dasar_harga_ideal`
   (kebanyakan dijangkarkan ke tangga paket internal Ignite 2,5 jt → Growth 6,5 jt
   → Market Leader 15 jt → Enterprise 25 jt+ dan menghindari perang harga bawah).

**Rumus demand per wilayah** (di `dashboard/analysis.py`, fungsi `impost_demand`):

```
sinyal_cari[wilayah]  = jumlah domain unik hasil pencarian "jasa <layanan> <wilayah>"
                        (dikumpulkan via MCP Tavily search API; hasil tersimpan
                        di data/scraping/demand-ringkas.csv)           → Lapis 1
pasokan_kompetitor    = jumlah kompetitor yang menjual layanan terkait
                        (maksimum antar-label SERVICE_RULES)           → Lapis 1
demand_skor           = 1 + 4 × (0,6 × sinyal ternormalisasi dalam wilayah
                              + 0,4 × pasokan ternormalisasi)          → Hipotesis
```

Wilayah: **Kalsel** (query Banjarmasin/Banjarbaru), **Kalimantan** (query
"kalimantan"/Balikpapan), **Nasional** (query "indonesia"/tanpa lokasi). Sinyal
pencarian adalah proxy interest, bukan volume pencarian resmi; karena dinormalisasi
dalam wilayah, skor membandingkan layanan satu sama lain di wilayah yang sama.

`posisi_vs_pasar` = titik tengah harga ideal ÷ titik tengah harga pasar
(<1 = lebih murah dari pasar, >1 = premium).

---

## 8. Contoh perhitungan utuh (dari data asli)

### 8.1 Skor industri - Properti & developer

Skor mentah di CSV: ukuran_pasar 4, pertumbuhan 5, belanja_digital 5,
kompetisi_rendah 3, akses 3, margin_retainer 5.

```text
= 0.20×4 + 0.20×5 + 0.20×5 + 0.15×3 + 0.15×3 + 0.10×5
= 0.80  + 1.00  + 1.00  + 0.45  + 0.45  + 0.50
= 4.20
```

Hasil **4,20 → Prioritas inti (peringkat 1)**. Cocok dengan kolom
`skor_tertimbang` di CSV dan dihitung ulang oleh `analysis.py` setiap run.

### 8.2 Skor industri - F&B (kontras)

5, 4, 3, 2, 5, 3:

```text
= 1.00 + 0.80 + 0.60 + 0.30 + 0.75 + 0.30 = 3.75 → Prioritas
```

Terlihat efek bobot: F&B menang telak di akses (5) dan ukuran (5), tapi kalah di
kompetisi (2) dan margin (3) - makanya tetap Prioritas, bukan Prioritas inti.

### 8.3 Pain point - "Lead masuk tapi tidak di-follow up" (SME)

5, 5, 5 → `0.4×5 + 0.4×5 + 0.2×5 = 5.00` → kuadran **Kritis**, peringkat 1.

### 8.4 Trust gap - Bukti hasil yang terukur

`5.0 - 2.5 = 2.5` → prioritas perbaikan #1 (disusul Akuntabilitas KPI `4.7 - 2.3 = 2.4`
di peringkat #2) → menjadi dasar janji positioning
"laporan revenue yang bisa diverifikasi".

---

## 9. Cara mereproduksi semua angka

```bash
# WSL/Linux
.venv/bin/python dashboard/analysis.py

# Windows
.venv-win\Scripts\python dashboard\analysis.py
```

Untuk data layanan IMPOST, sinyal pencarian dikumpulkan via **MCP Tavily search API**
(66 query awal: 11 layanan × 3 wilayah × 2 lokasi; ditambah 6 query 2 layanan baru pada 2026-11-06; scraping langsung dengan Python
dihapus karena mesin pencari memblokirnya sebagai bot). Hasilnya disimpan di
`research/data/scraping/demand-ringkas.csv`; untuk menyegarkan, jalankan ulang
kumpulan query MCP lalu tulis ulang file tersebut:

```bash
$env:PYTHONIOENCODING='utf-8'
python research\scraping\07-impost-csv.py       # regenerasi impost-layanan.csv (jika ubah harga)
python dashboard\analysis.py                    # hitung ulang demand + metrik
```

Pipeline membaca CSV mentah di `research/data/`, menghitung ulang **semua** skor
tertimbang, peringkat, prioritas, kuadran, gap, kompetisi terukur, dan menulis hasilnya
ke `dashboard/data/derived/` (termasuk `metrics.json`). Kolom `selisih_vs_file` pada
`industri_rank.csv` otomatis membuktikan apakah skor manual di CSV masih konsisten
dengan rumus (harus 0,00 semua).

Untuk menguji sensitivitas bobot: cukup edit `INDUSTRY_WEIGHTS` di
`dashboard/analysis.py` atau skor mentah di `skor-industri.csv`, jalankan ulang, dan
bandingkan peringkat.

---

## 10. Batasan yang harus diingat

1. **Single rater.** Semua skor 1-5 ditulis satu penilai (analis). Tidak ada uji
   reliabilitas antar-penilai. Dua penilai lain bisa menghasilkan ±1 poin per sel.
2. **Tidak ada responden.** Tidak ada sampling, tidak ada margin of error, tidak ada
   uji signifikansi. Label `Hipotesis` / `status_data = Hipotesis analis` dipertahankan
   di semua CSV dan dashboard secara sengaja.
3. **Yang sudah terukur vs belum:** hanya kompetisi (versi terukur) yang sepenuhnya
   dihitung dari data 50 agency. Pemetaan industri→layanan inti dan 5 kriteria lain
   masih penilaian analis.
4. **Harga dan benchmark iklan adalah estimasi pasar**, bukan data akun campaign.
   Harga ideal layanan IMPOST juga usulan analis; harga pasarnya dirangkai dari
   sinyal publik yang sebagian sudah terverifikasi (S31-S40).
5. **Jalur naik kualitas bukti** (sudah disiapkan, belum dijalankan):
   1. Triangulasi data internet (volume pencarian, ulasan Maps, forum) → status naik
      dari hipotesis ke _indikasi awal_.
   2. Wawancara + survei (150-200 responden, desain di `01-rancangan-riset.md`) →
      skor analisis diganti angka lapangan, Van Westendorp untuk harga.
   3. Tambah kolom `metode` + `url_bukti` per baris CSV agar setiap sel bisa diaudit.

---

## 11. Asal rumus: metode standar yang diadopsi dan penyesuaiannya

Tidak ada rumus di dokumen ini yang dikarang dari nol. Semuanya diadopsi dari metode
analisis keputusan yang baku, dengan penyesuaian kecil yang ditulis terbuka. Bagian
ini menjawab pertanyaan "rumus ini didapat dari mana".

### 11.1 Peta rumus ke metode asal

| Rumus (di bagian)                                                             | Didapat dari                                                                                                                                                             | Kenapa metode ini yang dipilih                                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skor_tertimbang = Σ bobot × skor` (bagian 2)                                 | **Simple Additive Weighting (SAW)**, teknik paling dasar dari keluarga **Multi-Criteria Decision Making (MCDM)**; standar di studi kelayakan dan pemilihan vendor        | Bisa dihitung ulang dengan kalkulator oleh siapa saja; sifatnya linear sehingga kontribusi tiap kriteria terlihat langsung (contoh utuh di bagian 8.1); metode MCDM lain seperti AHP menuntut perbandingan berpasangan dan TOPSIS perhitungan jarak ke solusi ideal - keduanya jauh lebih sulit diaudit tanpa menambah informasi baru |
| Skala 1-5 dengan anchor (bagian 2.3, 4.3)                                     | **BARS** (Behaviorally Anchored Rating Scale) dari psikologi organisasi/HR                                                                                               | Anchor "1 artinya apa, 5 artinya apa" membatasi perbedaan antar penilai; skor 2 dan 4 tidak didefinisikan terpisah karena sekadar interpolasi antar jangkar                                                                                                                                                                           |
| Bobot 0.60 permintaan / 0.30 gesekan / 0.10 margin (bagian 2.2)               | Keputusan bisnis eksplisit yang ditetapkan sekali sebelum melihat nilai per industri (praktik standar SAW: bobot ditetapkan pembuat keputusan, bukan dihitung dari data) | Regresi atau optimasi bobot butuh data hasil historis (omzet, closing) yang belum ada; bobot jujur dinyatakan sebagai pilihan manusia yang bisa dikritik dan diganti lewat uji sensitivitas (bagian 9)                                                                                                                                |
| `kompetisi_terukur = 1 + 4 × (1 - cakupan)` (bagian 3)                        | **Normalisasi min-max** ke 0-1 lalu regangan linear ke 1-5; arahnya dibalik (`1 - x`) karena pasokan tinggi berarti kompetisi tinggi berarti skor rendah                 | Regangan `1 + 4x` menjaga hasil tetap di skala 1-5 yang sama dengan versi hipotesis, sehingga kolomnya bisa ditukar di rumus bobot tanpa menyentuh bobot lain                                                                                                                                                                         |
| Bobot kekuatan agency `1 + 0.5 × verifikasi + 0.5 × layanan/5` (bagian 3.1)   | Confidence weighting: tiap "pesaing" ditimbang dari kualitas buktinya                                                                                                    | Agency yang hanya muncul di satu direktori tidak setara dengan agency bersitus terverifikasi dan lima kategori layanan                                                                                                                                                                                                                |
| `skor_prioritas = 0.4 × frekuensi + 0.4 × dampak + 0.2 × kesiapan` (bagian 4) | SAW yang sama dengan bagian 2; rasio 40/40/20 adalah keputusan bisnis dengan rasional tertulis (bagian 4.2)                                                              | Satu metode untuk seluruh dokumen supaya pembaca tidak perlu belajar dua rumus                                                                                                                                                                                                                                                        |
| `gap = kepentingan - kinerja` beserta kuadrannya (bagian 5)                   | **Importance-Performance Analysis (IPA)**, Martilla & James (1977), teknik klasik riset pemasaran yang masih jadi standar buku teks                                      | Framework yang persis menjawab "janji mana yang layak dijadikan positioning": harapan tinggi tapi kinerja pasar rendah = peluang                                                                                                                                                                                                      |
| `demand = 1 + 4 × (0.6 × sinyal + 0.4 × pasokan)` (bagian 7.3)                | **Indeks komposit**: tiap komponen dinormalisasi dibagi nilai maksimum wilayahnya, digabung tertimbang 60/40, lalu diregangkan dengan `1 + 4x` yang sama dengan bagian 3 | 60/40 memisahkan dua bukti yang sumbernya berbeda (permintaan dari sisi pencari, pasokan dari sisi penjual); normalisasi dalam wilayah wajib karena volume pencarian antar wilayah tidak sebanding; `1 + 4x` menjaga konsistensi skala 1-5                                                                                            |
| `posisi_vs_pasar` (bagian 7.3)                                                | Rasio harga sederhana (price positioning ratio)                                                                                                                          | Satu angka langsung terbaca: <1 lebih murah dari pasar, >1 premium                                                                                                                                                                                                                                                                    |
| Harga paket & harga ideal (bagian 7)                                          | **Anchoring**: harga diposisikan relatif terhadap jangkar yang bisa diverifikasi (pricelist publik kompetitor, benchmark biaya iklan) dan tangga paket internal          | Tanpa data willing-to-pay, jangkar publik adalah satu-satunya batas yang bisa dicek orang lain; aturan retainer 10-15% omzet bulanan adalah konvensi umum industri jasa                                                                                                                                                               |

### 11.2 Kenapa tidak memakai metode yang lebih canggih

- **Regresi dan machine learning butuh data hasil.** Belum ada historis omzet atau
  closing per industri untuk melatih model. Model canggih di atas data yang tidak ada
  hanya menghasilkan overfitting yang terlihat serius.
- **AHP/TOPSIS menambah presisi semu.** Perbandingan berpasangan tetap diisi penilai
  yang sama (single rater, lihat bagian 10), jadi presisinya naik di kertas saja
  sementara sumber bias tidak berubah.
- **SAW + BARS + IPA dipilih justru karena sederhana.** Setiap pembaca bisa mengaudit,
  mengkritik, dan mengganti angkanya tanpa memahami matematika di baliknya. Bagian
  paling rawan (bobot dan skor mentah) sengaja dibuat polos agar mudah diserang,
  dan dokumen ini adalah tempat menyerangnya.

---

## 12. Kamus dashboard untuk presentasi: arti istilah & cara baca tiap tab

Bagian ini disiapkan agar dashboard bisa dipresentasikan ke **orang awam** (pemilik
usaha, rekan non-marketing, calon investor). Bacakan dulu enam istilah kunci di
12.1, lalu saat berpindah tab gunakan kalimat pembuka "Tab ini menjawab
pertanyaan ..." di tiap subbab.

### 12.1 Enam istilah kunci (jelaskan dulu sebelum masuk tab)

| Istilah                          | Arti untuk orang awam                                                                                                                                                                                                                                                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lapis 1 / Terverifikasi**      | Data nyata yang bisa dicek ulang di internet: statistik BPS, harga yang dipajang kompetitor di website, laporan industri (GroupM, PwC). Ibarat "struk belanja" - ada buktinya.                                                                                                                                                         |
| **Lapis 2 / Hipotesis**          | Perkiraan analis yang masuk akal tapi belum diuji ke lapangan: skor 1-5, harga ideal usulan, prioritas pain point. Ibarat "dugaan cerdas" - perlu survei sebelum jadi keputusan final. Dashboard menandai mana kuning (hipotesis) dan mana hijau (terverifikasi).                                                                      |
| **Kompetitor lokal vs nasional** | Lokal = agency yang kantornya memang di Kalimantan. Nasional = agency besar berbasis di Jawa/luar yang "menjangkau" kota Kalimantan lewat halaman web khusus (contoh: halaman "Jasa Digital Marketing Banjarmasin" milik agency Surabaya).                                                                                             |
| **Retainer**                     | Langganan bulanan. Klien membayar tetap tiap bulan agar agency terus mengelola sosmed/iklan - seperti langganan kebersihan kantor, bukan bayar sekali.                                                                                                                                                                                 |
| **CPM / CPC / CPL**              | Tiga cara harga iklan digital diukur. CPM = biaya setiap 1.000 orang _melihat_ iklan (seperti biaya papan iklan disorot mata). CPC = biaya setiap satu orang _mengklik_ (masuk etalase). CPL = biaya setiap satu orang _meninggalkan kontak_ (calon pelanggan nyata). Semakin ke bawah, semakin mahal tapi semakin dekat ke penjualan. |
| **Demand vs pasokan**            | Demand = seberapa banyak pasar membutuhkan/mencari suatu layanan. Pasokan = seberapa banyak penyedia yang menawarkannya. Peluang bagus = demand tinggi + pasokan rendah (banyak yang cari, sedikit yang jual).                                                                                                                         |

### 12.2 Pembuka - "Bagaimana kondisi pasar Kalimantan?"

Dashboard saat ini **10 tab dan 25 grafik**; tab "Ringkasan" versi awal sudah tidak ada,
dan grafik makro per provinsi (pertumbuhan ekonomi, penetrasi internet) belum
ditampilkan di dashboard - angkanya ada di `research/data/makro-kalimantan.csv`
(kolom `pertumbuhan_2024_persen`, `pertumbuhan_2025_persen`, `penetrasi_internet_2025_persen`).

Untuk membuka presentasi, bacakan banner **Status data** di atas halaman (jujur: skor
masih hipotesis), lalu masuk ke tab **Pasar Kota** (bagian 12.3). Jika perlu angka makro
se-Kalimantan: ekonomi Kalimantan tumbuh 5,43% (2024) vs nasional 5,03%; Kaltim paling
agresif di 2024 (6,17%) lalu melambat di 2025 (4,53%); Kalbar tumbuh tertinggi di 2025
(5,39%); penetrasi internet tertinggi Kalteng (89,57%), terendah Kalsel (64,67%).

### 12.3 Tab PASAR KOTA - "Di kota mana kita bermain?"

| Yang tampil              | Menjelaskan apa & cara membacanya                                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Peta gelembung**       | Tiap gelembung = satu kota; makin besar gelembung makin banyak penduduk. Yang ditanya audiens biasanya "Balikpapan/Banjarmasin besar nggak?" - jawabannya lebar gelembung. |
| Grafik **Penduduk kota** | Peringkat kota berdasarkan jumlah jiwa. Pasar = orang; makin banyak jiwa makin besar kue.                                                                                  |
| Grafik **UMK**           | Upah Minimum Kota - proksi daya beli. Kota dengan UMK tinggi = bisnis di sana sanggup bayar jasa lebih mahal.                                                              |
| Grafik **UMKM**          | Jumlah usaha kecil yang terdata per kota = jumlah calon klien potensial di segmen bawah.                                                                                   |
| Tabel kota               | Detail lengkap per kota + status data (terverifikasi/estimasi) - tunjukkan ini kalau audiens bertanya "dari mana angkanya".                                                |

### 12.4 Tab INDUSTRI WINNING - "Klien dari industri apa yang kita kejar?"

Kalimat pembuka: _"Kita tidak bisa melayani semua orang. Data ini bilang industri
mana yang paling menguntungkan untuk digodok duluan."_

| Yang tampil                                            | Menjelaskan apa & cara membacanya                                                                                                                                                                                                                              |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KPI Industri winning / Skor tertinggi / Prioritas inti | Ada 10 industri "juara"; yang paling atas skornya (4,x dari 5) adalah target utama penjualan.                                                                                                                                                                  |
| **Bubble chart** (sebaran titik)                       | Tiap titik = satu industri. Sumbu kanan = seberapa mudah masuk & cepat closing; sumbu atas = skor daya tarik total; ukuran gelembung = besarnya pasar; warna = status prioritas. Titik besar di kanan-atas = emas: pasar besar, mudah dikejar, skornya tinggi. |
| Tabel **Peringkat industri**                           | Daftar lengkap skor dari atas ke bawah - versi rapi dari bubble chart.                                                                                                                                                                                         |
| **Radar** (sarang laba-laba)                           | Perbandingan satu industri vs rata-rata: makin lebar bentuknya di satu arah, makin kuat industri itu di kriteria tersebut (pasar besar, tumbuh, suka belanja digital, kompetisi longgar, mudah diakses, margin bagus).                                         |
| Grafik **Dampak data kompetitor** & tabel perbandingan | Bukti kejujuran metodologi: ketika skor kompetisi dihitung dari 50 agency nyata (bukan tebakan), peringkat beberapa industri naik/turun. Naik (hijau) = ternyata lebih longgar dari dugaan; turun (oranye) = lebih ramai.                                      |

### 12.5 Tab INDUSTRI POTENSIAL - "Yang belum utama tapi layak dipantau"

Industri dengan skor di bawah ambang juara. Sama persis grafiknya dengan tab
Industri Winning; pesannya: _"Ini cadangan - kalau tim punya sisa kapasitas,
industri ini bisa dicoba, tapi jangan utamakan budget."_

### 12.6 Tab KOMPETITOR AGENCY - "Siapa lawan kita dan seberapa kuat?"

| Yang tampil                              | Menjelaskan apa & cara membacanya                                                                                                                                    |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KPI Total/Lokal/Nasional/Harga terbuka   | 50 pesaing terpetakan; 38 lokal + 12 nasional; "harga terbuka" = pesaing yang berani memajang harga (makin sedikit, makin banyak yang main tawar-menawar).           |
| Grafik **Sebaran kota**                  | Di kota mana pesaing berkantor. Kota dengan batang pendek = pasar yang masih sepi pesaing lokal.                                                                     |
| Pie **Lokal vs nasional**                | Porsi lawan lokal vs jaringan luar. Nasional kuat di SEO/web; lokal kuat relasi tapi lemah laporan.                                                                  |
| Grafik **Layanan paling sering dijual**  | Layanan apa yang paling ramai ditawarkan pesaing. Yang paling panjang = paling ramai = paling sulit tampil beda.                                                     |
| **Matrix layanan** (kotak-kotak)         | Tiap baris = 1 agency, tiap kolom = 1 layanan; kotak hijau berarti agency itu menjualnya. Sekilas terlihat siapa "toko serba ada" dan siapa spesialis.               |
| Tabel database + **Sinyal harga publik** | Daftar pesaing dengan kekuatan/celah masing-masing - ini "buku catatan mata-mata" saat presentasi; harga yang terlihat adalah harga pajangan, bukan penawaran resmi. |

### 12.7 Tab LAYANAN WINNING - "Produk kita dijual bagaimana?"

| Yang tampil                                        | Menjelaskan apa & cara membacanya                                                                                                                                            |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KPI Entry/Growth per bulan                         | Harga pintu masuk (Rp2.500.000) dan paket inti (Rp6.500.000). Ini tangga harga kami sendiri, bukan pasar.                                                                    |
| Tabel **Tangga paket**                             | Lima anak tangga dari Audit 360 (produk cicip Rp1,5-3 jt sekali bayar) sampai Enterprise (Rp25 jt+). Analogi: dari cek kesehatan, langganan bulanan, sampai asisten pribadi. |
| **Paket per industri** & **Add-on**                | Versi kustom per industri + layanan tambahan di luar langganan (video, website, KOL).                                                                                        |
| Grafik **Layanan paling sering dijual kompetitor** | Pengingat pasar: banyak yang jual konten/website → kami membedakan diri lewat "terukur" (laporan & KPI), bukan lewat harga termurah.                                         |
| **Benchmark retainer**                             | Rentang langganan pasarnya - pembanding supaya tangga harga kami tidak jauh melenceng.                                                                                       |

### 12.8 Tab LAYANAN IMPOST - "Layanan kami sendiri: harga ideal & ramai tidaknya permintaan"

| Yang tampil                                                    | Menjelaskan apa & cara membacanya                                                                                                                                                                                                                                             |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KPI Demand tertinggi Kalsel/Nasional/Terendah                  | Layanan dengan permintaan terkuat di tiap wilayah (Kalsel: Social Media Management; nasional: Website/App) dan yang paling sepi (Customer Service → posisikan sebagai pelengkap, bukan pintu masuk).                                                                          |
| **Peta demand per wilayah** (kotak warna)                      | Tiap kotak = skor permintaan relatif 1-5 untuk satu layanan di satu wilayah; makin gelap makin ramai dicari. Bandingkan antar kotak pada kolom yang sama (antar layanan di wilayah yang sama).                                                                                |
| Grafik **Sinyal pencarian**                                    | Berapa banyak penyedia muncul saat dicari "jasa X di wilayah Y" - proxy ramai-nya permintaan, hasil pengumpulan otomatis via MCP.                                                                                                                                             |
| Grafik **Pasokan kompetitor**                                  | Berapa dari 50 pesaing yang menjual layanan itu. Pasokan rendah + demand tinggi = celah pasar.                                                                                                                                                                                |
| **Harga pasar vs harga ideal** (garis abu vs hijau, skala log) | Garis abu-abu = rentang harga yang dipajang pasar; belah ketupat hijau = harga ideal usulan kami. Skala log dipakai karena harganya melompat (ratusan ribu sampai puluhan juta) - jangan bacakan angkanya persis, bacakan posisinya: "ideal kami duduk di bagian mana pasar". |
| Tabel harga & demand                                           | Angka lengkap + kolom "Ideal vs pasar" (di bawah 1 = lebih murah dari pasar, di atas 1 = premium) + dasar pertimbangan harga. Tekankan label hipotesis: ini usulan yang harus diuji survei.                                                                                   |

### 12.9 Tab SOSIAL MEDIA - "Iklan digital itu mahal tidak?"

| Yang tampil                                          | Menjelaskan apa & cara membacanya                                                                                                                                                                             |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Grafik **Jangkauan platform**                        | Juta pengguna tiap platform - memilih panggung iklan.                                                                                                                                                         |
| Grafik **E-commerce**                                | Pengguna aktif marketplace/social commerce - menandakan kebiasaan belanja online.                                                                                                                             |
| **Benchmark biaya iklan** (garis-garis dengan titik) | Tiap garis = rentang harga wajar satu jenis iklan (CPM/CPC/CPL per kanal); titik = nilai tengah. Skala log agar semua muat. Untuk audiens: _"pasang iklan Rp1 juta bukan angka aneh - ini rentang pasarnya."_ |
| **Prioritas kanal per industri** (heatmap) & tabel   | Kotak makin gelap = kanal itu makin penting untuk industri tsb. Contoh baca: properti → Google & website; F&B → TikTok/Instagram.                                                                             |

### 12.10 Tab PAIN POINT OWNER - "Masalah apa yang paling menyiksa calon klien?"

Kalimat pembuka: _"Kami tidak menjual 'sosmed'; kami menjual obat untuk luka ini."_

| Yang tampil                                                         | Menjelaskan apa & cara membacanya                                                                                                                                                                                                                               |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bubble chart pain point**                                         | Tiap titik = satu masalah. Sumbu kanan = seberapa sering terjadi; sumbu atas = seberapa besar lukanya ke bisnis; ukuran = seberapa siap mereka bayar untuk disembuhkan. Titik besar di kanan-atas = masalah yang orang rela bayar segera (lead follow-up, dll). |
| Grafik **12 prioritas tertinggi**                                   | Peringkat masalah dari skor 0,4×frekuensi + 0,4×dampak + 0,2×kesiapan bayar.                                                                                                                                                                                    |
| Kuadran (Kritis / Sering tapi ringan / Jarang tapi berat / Monitor) | Sortir masalah: Kritis = sering + parah (prioritas obat); sisanya dipantau.                                                                                                                                                                                     |

### 12.11 Tab PERSEPSI AGENCY - "Kenapa klien tidak percaya agency?"

| Yang tampil                                            | Menjelaskan apa & cara membacanya                                                                                                                                         |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Grafik **Kepentingan vs kinerja** (batang berpasangan) | Batang hijau = apa yang paling diharapkan klien (mis. laporan transparan); batang oranye = penilaian kinerja agency pada umumnya. Selisih keduanya = **gap** kepercayaan. |
| KPI Gap terbesar & tabel kesenjangan                   | Dimensi dengan celah paling lebar = janji utama pemasaran kami (mis. "laporan yang bisa dipahami orang biasa").                                                           |

### 12.12 Tab METODOLOGI - "Dari mana semua angka ini?"

Untuk audiens awam cukup tiga kalimat: **(1)** data dikumpulkan dari sumber publik
resmi dan website kompetitor; **(2)** angka hipotesis diberi label jelas dan rumusnya
terbuka di `KNOWLEDGE.md`; **(3)** langkah validasi (survei 150-200 responden) sudah
dirancang. Tabel _data dictionary_ dipakai kalau ada yang bertanya file apa saja
yang ada; tombol **Jalankan ulang analisis** membuktikan semua angka bisa
dihitung ulang, bukan tempelan manual.
