# 03 - Kompetitor Agency Kalimantan

> **Update dataset (Nov 2026):** database kompetitor berisi **50 agency** (38 lokal Kalimantan, 12 nasional yang menyasar Kalimantan) di 9 kota. Setiap baris punya kolom `lokasi_terverifikasi` dan `bukti_lokasi`; agency luar Kalimantan tanpa jejak di pasar ini sudah dikeluarkan. Profil di dokumen ini adalah ringkasan; data terbaru ada di `data/kompetitor.csv`, `data/sumber.csv`, dan dashboard tab **Kompetitor Agency**.

> **Metode:** audit website, profil publik, Instagram/TikTok/LinkedIn, dan halaman pencarian. Harga adalah **sinyal publik**, bukan quotation. Beberapa pemain "lokal" ternyata berbasis di Jawa tetapi menargetkan kota Kalimantan lewat halaman SEO.
>
> **Pengecualian:** IMPOST Media (Banjarbaru) tidak dimasukkan sebagai kompetitor karena merupakan entitas yang melakukan riset ini. Analisis kompetitor difokuskan pada pemain lain yang bersaing di pasar yang sama.

---

## 1. Peta kompetitor: 4 lapis

| Lapis | Ciri | Contoh | Ancaman |
|---|---|---|---|
| **A. Agency lokal boutique** | 1-15 orang, kuat relasi, produksi konten, harga fleksibel | Up & Away, Codezy, Fannan, EastKreatif, DNA Indonesia | Langsung (rebutan klien lokal) |
| **B. Agency nasional dengan landing page kota** | HQ Jawa, jual "jasa digital marketing [kota]", pricelist terbuka | Karya Studio, Digital360, Publish Agency, Toekang Digital | Tidak langsung, tapi menang SEO & kepercayaan |
| **C. Freelancer & marketplace** | Harga murah, cepat, kualitas bervariasi | Fastwork, Sribu, freelancer IG | Menekan harga bawah |
| **D. In-house / tim internal** | Owner hire 1-2 orang admin/desainer | UMKM naik kelas | "Kompetitor" utama: keputusan make-or-buy |

**Wawasan:** kompetitor terbesar bukan agency lain, tetapi **"biar admin saja yang handle"**. Agency yang menang adalah yang bisa menunjukkan biaya peluang (opportunity cost) dari in-house.

---

## 2. Matrix kompetitor

| # | Nama | Basis | Posisi | Layanan utama | Kanal yang dijual | Sinyal harga | Kekuatan | Celah |
|---|---|---|---|---|---|---|---|---|
| 1 | **Up & Away Digital** | Balikpapan | "Bayar satu, dapat satu tim" | Digital ads, SMM, website, desain, foto/video, logo | IG, TikTok, Meta/Google Ads, WhatsApp | Konten mulai **Rp700 rb** | Paket bundling, CTA kuat, waiting list, gratis audit | Positioning masih umum; tidak ada spesialisasi industri |
| 2 | **Codezy** | Balikpapan | Tech-led digital agency | Website, app, cyber security, UI/UX, branding, SMM | IG, LinkedIn, website | Tidak publik | Kapabilitas teknis (Laravel/Next/Flutter), cybersecurity | Marketing performance & konten kurang menonjol |
| 3 | **Wemember Digital** | Banjarmasin | Creative agency lokal | Branding, konten, foto/video, SMM, web | IG, website, WhatsApp | Tidak publik | Portofolio brand lokal Kalsel, paket jelas | Belum ada performance/CRM |
| 4 | **EastKreatif** | Samarinda | Strategic branding & digital | SMM, foto/video, visual identity, konsultasi bisnis digital | IG, LinkedIn | Tidak publik | Pemain Samarinda, grup Cipta Kreatif, dekat komunitas | Skala kecil; kapasitas terbatas |
| 5 | **DNA Indonesia** | Pontianak | Social media agency pertama di Pontianak | IG/TikTok handling, foto produk, influencer, logo, web, ads | IG, website, WhatsApp | Tidak publik | Fokus social media, portofolio brand lokal, edukasi | Terlalu bergantung IG; tidak ada performance/CRM |
| 6 | **Karya Studio** | Banyuwangi (nasional) | Software house + digital marketing per kota | SEO, SEM, SMM, ads, web, software, analitik | Website + landing page kota, WhatsApp | Tidak publik (paket via konsultasi) | Kredibilitas software house; halaman kota; konten edukasi | Bukan agency marketing murni; eksekusi remote |
| 7 | **Vodeco** | Semarang (nasional) | Web dan SEO murah, harga terpampang | Web dev, SEO, company profile, branding, digital marketing | Website + pricelist | **Rp100 rb-700 rb** per item; SEO Rp500 rb | Harga sangat terbuka, halaman layanan 8 kota Kalimantan | Bukan lokal; kualitas eksekusi remote |
| 8 | **Lenteraweb** | Kediri (nasional) | Jasa website + digital marketing nasional | Website, landing page, SEO, Meta/Google Ads | Website + halaman kota | Tidak publik | Cakupan nasional, banyak halaman kota | Bukan lokal; positioning generik |
| 9 | **ATERA** | Palangka Raya | Agency digital Kalteng | Website, landing page, social media, no-code | Website, WhatsApp | Tidak publik | Satu-satunya pemain terverifikasi di Palangka Raya | Skala kecil; konten terbatas |
| 10 | **Banjar Creative** | Banjarmasin | Social media content | SMM, konten | IG | Tidak publik | Konten ringan, engagement | Bukan performance |
| 11 | **Beaztex** | Pontianak | Digital agency | Web, desain, digital | Website | Tidak publik | Presence lokal | Informasi layanan minim |
| 12 | **Debiner** | Pontianak | Creative digital agency | Web design/dev, graphic, branding | Behance, LinkedIn | Tidak publik | Desain & web | Tidak fokus marketing performance |
| 13 | **Kreassi Team** | Pontianak | Creative & branding | SMM, konten, branding | IG | Tidak publik | Kreatif, komunitas | Kapasitas kecil |
| 14 | **Toekang Digital** | Solo (nasional) | SMM murah bergaransi | SMM, web, ads, marketplace | Website + halaman kota | Via WA | SEO kota, garansi, konten | Eksekusi remote; bukan lokal |

**Catatan:** tabel di atas hanya 14 pemain paling relevan. Daftar lengkap 50 agency ada di `data/kompetitor.csv`. "Borneo Digital Agency" (Tarakan) muncul di direktori AI-generated dan **belum terverifikasi**; jangan dijadikan acuan tanpa cek langsung.

**Perluasan Nov 2026:** 18 agency baru ditambahkan memakai Bright Data (Google Maps lewat scraping browser), Tavily, dan Firecrawl. Sebaran berubah menjadi Pontianak 13, Balikpapan 9, Samarinda 7, Banjarmasin 5, Palangka Raya 2, Singkawang 1, Tarakan 1. Daftar "Top 10" dari direktori seperti AAMAX tidak dipakai karena isinya template AI, bukan perusahaan nyata.

---

## 3. Profil mendalam

### 3.1 Up & Away Digital (Balikpapan) - kompetitor paling agresif di entry-level

- **Positioning:** "bukan sekedar bikin feed cantik - kami pastikan konten kamu cari cuan."
- **Paket:** digital ads, SMM, website, desain, foto/video, logo.
- **Harga:** konten mulai Rp700 ribuan; paket lain via konsultasi.
- **Kekuatan:** CTA jelas (free audit, waiting list), bahasa sederhana, bukti sosial di IG.
- **Celah:** belum punya produk per industri; janji "cuan" belum didukung dashboard revenue.

### 3.2 Codezy (Balikpapan) - kompetitor teknis

- **Positioning:** digital partner untuk transformasi bisnis.
- **Layanan:** website, mobile app, cybersecurity, UI/UX, branding, SMM.
- **Kekuatan:** kapabilitas engineering & security; cocok untuk korporat.
- **Celah:** marketing performance bukan core; tidak ada paket retainer konten yang jelas.

### 3.3 Wemember Digital (Banjarmasin) - creative agency Kalsel

- **Positioning:** creative & digital agency Banjarmasin, "Let's Make It #BARENGJADIBEDA".
- **Layanan:** branding & visual, produksi konten, SMM/KOL, web & digital experience.
- **Kekuatan:** portofolio brand lokal (kuliner, klinik, properti, pendidikan di Banjarmasin dan Tanah Laut).
- **Celah:** belum menjual performance, CRM, dan bukti lead sebagai paket.

### 3.4 DNA Indonesia (Pontianak) - spesialis social media

- **Positioning:** "The First Hub of Creative & Digital Marketing Agency" di Pontianak.
- **Layanan:** IG handling, TikTok/Reels, foto produk, influencer, logo, web, ads.
- **Kekuatan:** fokus sosial media, klien brand lokal, konten edukasi.
- **Celah:** belum ada CRM/lead tracking; paket masih custom.

### 3.5 Karya Studio (nasional, software house yang menyerang SEO lokal)

- **Posisi:** enterprise IT consultant & software house, tetapi membuat halaman "Jasa Digital Marketing [kota]" untuk hampir semua kota di Indonesia, termasuk Balikpapan, Samarinda, Banjarmasin, Pontianak.
- **Layanan:** software custom, website, aplikasi, SEO, SEM, SMM, ads, analitik.
- **Kekuatan:** kredibilitas teknis/software house; konten panjang; CTA WhatsApp; halaman kota.
- **Celah:** bukan agency marketing murni; eksekusi remote; klaim "lokal" tanpa tim lokal.

### 3.6 Benchmark harga di luar pasar Kalimantan

Dua pemain berikut **bukan** kompetitor Kalimantan dan tidak ada di `data/kompetitor.csv`, tetapi pricelist publiknya dipakai sebagai pembanding harga.

- **Kreatifindo (Semarang):** Starter Rp750 rb, Growth Rp1,5 jt, Premium Rp3 jt, Professional Rp5 jt, Enterprise Rp10 jt, Custom mulai Rp15 jt/bulan. Ads fee Meta/IG Rp2 jt, Google Rp2,5 jt, TikTok Rp2 jt, multi-platform Rp3,5-5 jt + 3% ad spend. SEO Rp3-10 jt/bulan, kontrak 6 bulan.
- **Uraga (Jakarta/Malang):** B2B Ads Rp2,9 jt/bln (all-in iklan, kreatif, CRM); Design Rp1,5 jt; E-commerce Rp2,9 jt; Logo Rp3 jt; SMM Jakarta Rp4,9 jt.

**Implikasi:** keduanya jadi *anchor* harga yang dilihat calon klien saat membandingkan, meski tidak bersaing langsung di Kalimantan.

---

## 4. Benchmark harga pasar

### Social Media Management (per bulan)

| Segmen | Range harga | Contoh |
|---|---|---|
| Freelancer/marketplace | Rp250 rb-1 jt | Fastwork, Sribu |
| Entry UMKM | Rp700 rb-1,8 jt | Up & Away, Kreatifindo Starter, Resolusiweb, Tampil Silver |
| Growth SME | Rp2,9-4,9 jt | Kreatifindo Premium, Tampil Platinum, Uraga SMM, Bramasta |
| Korporat | Rp5-10 jt | Kreatifindo Professional/Enterprise |
| Premium/custom | Rp15-40 jt | Kreatifindo Custom, SHIELD |

> Catatan: Kreatifindo dan Uraga hanya dipakai sebagai *anchor* harga. Keduanya tidak masuk database kompetitor karena tidak menyasar kota Kalimantan.

### Ads management

| Item | Range |
|---|---|
| Fee Meta/IG | Rp2-2,5 jt/bln |
| Fee Google | Rp2,5-3 jt/bln |
| Fee TikTok | Rp2 jt/bln |
| Multi-platform | Rp3,5-5 jt/bln |
| Persentase ad spend | 3-5% |
| Minimum ad spend | Rp3 jt/bln per platform |

### Project

| Item | Range |
|---|---|
| Logo/brand identity | Rp1,5-15 jt |
| Company profile | Rp3-15 jt |
| Website company profile | Rp5-25 jt |
| E-commerce | Rp15-75 jt |
| Video company profile | Rp5-30 jt |

> **Kesimpulan harga:** pasar Kalimantan sangat sensitif di bawah Rp2 jt, tapi mulai terbuka di Rp4-8 jt **jika** ada bukti lead/revenue. Harga premium >Rp15 jt hanya masuk untuk korporat, properti, dan B2B.

---

## 5. Pola persaingan & celah

### Pola yang terlihat

1. **Hampir semua agency lokal menyembunyikan harga.** Ini menciptakan friksi dan memberi ruang bagi pemain nasional yang transparan.
2. **Positioning homogen:** "digital marketing agency", "creative agency", "all-in-one". Hampir tidak ada yang bilang "khusus properti" atau "khusus klinik".
3. **Kanal jual utama Instagram + WhatsApp.** SEO lokal masih lemah; hanya pemain nasional yang serius.
4. **Bukti yang dijual masih estetika** (feed cantik, logo, video), bukan angka bisnis.
5. **Tidak ada yang menjual CRM/WhatsApp automation** sebagai bagian paket.
6. **B2B industrial hampir kosong.** Tidak ada agency lokal yang menonjol untuk employer branding, SEO B2B, atau dokumentasi proyek tambang/konstruksi.
7. **Tidak ada garansi/pilot.** Semua minta kontrak 3-6 bulan tanpa uji coba berbasis KPI.

### Celah yang bisa dimenangkan

| Celah | Produk | Mengapa sulit ditiru |
|---|---|---|
| Transparansi harga | Pricelist publik + kalkulator | Butuh disiplin operasional & margin jelas |
| Spesialisasi industri | Paket "Property Lead Engine", "Clinic Booking System" | Butuh studi kasus & pemahaman industri |
| Bukti revenue | Dashboard lead → closing, biaya per lead | Butuh integrasi CRM & akses data klien |
| Kecepatan respons | SLA balas DM <15 menit, lead <5 menit | Butuh tim & proses |
| B2B/industrial | Employer branding + SEO + dokumentasi | Butuh kemampuan menulis teknis |
| Hybrid Kalsel | Radio/outdoor + digital + komunitas | Butuh jaringan lokal, bukan remote |

---

## 6. Peta positioning

```
Harga tinggi
    │
    │   Karya Studio / Digital360 (nasional, remote)
    │
    │   Publish Agency / Etnicode DS (nasional, transparan)
    │
    │        ★ CELAH: mid-price + spesialisasi industri + bukti revenue
    │
    │   Wemember / Codezy (lokal, korporat)
    │   DNA / EastKreatif (lokal, mid)
    │
    │   Up & Away / freelancer (entry)
    └──────────────────────────────────────── Spesialisasi tinggi
```

**Rekomendasi:** jangan bersaing di harga terendah. Ambil posisi **"growth partner untuk industri tertentu, dengan harga transparan dan bukti lead"** - di antara agency lokal yang murah dan agency nasional yang remote.

---

## 7. Implikasi untuk penawaran

1. **Publikasikan harga mulai dari.** Ini langsung membedakan dari 90% kompetitor lokal.
2. **Buat 1 halaman per industri + per kota** (contoh: `/agency-properti-balikpapan`). Ini menyerang strategi Karya Studio dengan keunggulan lokal.
3. **Jual audit 360° berbayar (Rp1,5-3 jt)** sebagai pintu masuk, bukan gratis. Audit gratis menarik bargain hunter.
4. **Tawarkan pilot 60 hari** dengan KPI biaya per lead - kontrak 6 bulan setelah terbukti.
5. **Bangun bukti dalam format angka:** "biaya per lead turun 42%", "waktu respons 4 menit", "ROAS 5,8x".

---

## Sumber

- Up & Away Digital - https://upaway.id/
- Codezy - https://codezy.id/services
- Wemember Digital - https://wememberdigital.id
- EastKreatif - https://www.instagram.com/eastkreatif.id/ ; https://id.linkedin.com/company/eastkreatif-indonesia
- DNA Indonesia - https://dnaindonesia.id/
- ATERA - https://atera.web.id
- Karya Studio (contoh halaman kota) - https://karyastudio.com/jasa-digital-marketing-banjarmasin
- Vodeco - https://vodeco.co.id
- Lenteraweb - https://lenteraweb.com
- Toekang Digital - https://toekangdigital.com/jasa-kelola-akun-instagram-tiktok-pontianak-terbaik-dan-bergaransi/
- Beaztex - https://beaztex.com/about
- Debiner - https://www.behance.net/debiner
- Bramasta - https://www.bramasta.id/jasa-social-media-management/
- Tampil Digital - https://www.tampildigital.com/jasa-social-media-marketing-manajemen/
- Fastwork - https://fastwork.id/social-media-management
- Redcomm (benchmark biaya) - https://redcomm.co.id/knowledges/biaya-jasa-digital-marketing-agency
- Kreatifindo (benchmark harga, bukan kompetitor Kalimantan) - https://kreatifindo.co.id/pricelist
- Uraga (benchmark harga, bukan kompetitor Kalimantan) - https://uraga.co.id/
