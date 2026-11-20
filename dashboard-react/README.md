# Dashboard Analisis Riset Pasar Kalimantan (React)

Versi React/Vite dari dashboard Streamlit di `../dashboard-streamlit/`. Data dibaca dari hasil pipeline Python
yang sudah ada (`dashboard-streamlit/data/derived/`), dikonversi ke JSON statis, lalu dibundel saat build.
Tidak ada backend, tidak ada environment variable, dan tidak ada API key yang dibutuhkan saat deploy.

## Daftar halaman

1. Industri Winning
2. Pain Point Owner
3. Industri Potensial
4. Kompetitor Agency
5. Layanan Winning
6. Layanan IMPOST
7. Sosial Media
8. Persepsi Agency
9. Pasar Kota
10. Metodologi

## Menjalankan lokal

```bash
cd dashboard-react
npm install
npm run dev
```

Buka `http://localhost:5173`.

## Menyegarkan data

Dashboard memakai **hasil analisis yang sudah dihitung**, bukan CSV mentah. Setelah CSV di
`research/data/` berubah:

```bash
# 1. hitung ulang derived data
python dashboard-streamlit/analysis.py          # Windows: .venv-win\Scripts\python dashboard-streamlit\analysis.py

# 2. salin derived data ke src/data/
cd dashboard-react
npm run sync:data

# 3. cek hasil
npm run build
```

`npm run sync:data` membaca 21 CSV dan `metrics.json` dari `dashboard-streamlit/data/derived/`, lalu
menulis JSON ke `dashboard-react/src/data/`. Script ini aman dijalankan berulang.

## Deploy ke Vercel

Cara tercepat: import repository lewat Vercel.

1. Buka [vercel.com/new](https://vercel.com/new) dan import repository GitHub ini.
2. Vercel akan mendeteksi Vite secara otomatis. Jika tidak, isi manual:
   - **Root Directory**: `dashboard-react`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Klik **Deploy**. Tidak perlu environment variable.

Dari CLI:

```bash
cd dashboard-react
npm i -g vercel   # sekali saja
vercel            # preview
vercel --prod     # produksi
```

`vercel.json` sudah berisi rewrite SPA sehingga navigasi dan refresh langsung pada URL apa pun
tetap merender aplikasi.

## Struktur

```text
dashboard-react/
├── index.html              # font Noto Sans dan meta
├── vercel.json             # konfigurasi deploy
├── vite.config.js          # chunk charts dipisah dari app
├── scripts/
│   └── sync-data.mjs       # CSV derived -> JSON statis
└── src/
    ├── app.jsx             # navigasi 10 halaman + header
    ├── styles.css          # sistem visual monokrom
    ├── data/               # hasil sync-data (jangan edit manual)
    ├── lib/format.js       # formatter id-ID
    └── components/
        ├── ui.jsx          # Panel, KPI, Table, Heatmap, RangePlot, dll.
        └── tabs/           # 10 halaman dashboard
```

## Catatan desain

Satu font untuk seluruh antarmuka: **Noto Sans**. Hierarki dibangun dari ukuran, opasitas,
dan ruang, bukan dari campuran jenis huruf.

Tema memakai latar putih dengan teks gelap. Palet sengaja monokrom: satu warna dinyatakan
sebagai tangga `--ink` di `src/styles.css`, dengan opasitas sebagai pembeda. Status dan kategori dibedakan lewat terang/gelap dan garis solid atau
putus-putus, bukan lewat warna. Kisi 12 kolom dipakai untuk KPI dan langkah kerja; setiap panel
grafik atau tabel memakai satu kolom penuh agar datanya lapang. Animasi masuk hanya sekali saat
halaman dibuka dan tidak berjalan saat pengguna memilih `prefers-reduced-motion`.

Setiap halaman punya URL sendiri, misalnya `/kota` atau `/metodologi`, memakai History API.
Refresh dan tombol back/forward tetap membuka halaman yang sama. `vercel.json` sudah meneruskan
semua rute ke `index.html`.

Di desktop, sidebar mulai sebagai rel sempit yang benar-benar kosong, hanya tombol panah.
Buka/tutup hanya lewat tombol itu; tidak ada hover, tidak ada nomor, tidak ada penanda active.
Perubahan lebar terjadi seketika tanpa animasi supaya tidak tersendat. Saat melebar, label menu
muncul.
Di layar sempit, sidebar menjadi laci menu dengan label lengkap. Isi tabel memakai
`white-space: nowrap`, sehingga tabel lebar bisa digeser horizontal di dalam wadahnya.
