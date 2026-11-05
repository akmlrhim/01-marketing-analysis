# Temuan Scraping Tambahan - Kompetitor yang Mengincar Kalimantan

> Catatan (Nov 2026): script scraping Python (01-06) sudah dihapus karena mesin
> pencari memblokir akses langsung. Pengumpulan data sinyal kini via **MCP Tavily
> search API**; file data di `research/data/scraping/` tetap dipakai pipeline.
> Dokumen ini dipertahankan sebagai catatan metode & temuan.

> Tanggal: 2026-11 (scraping otomatis) · Metode: Python + `ddgs` (multi-backend search) + `requests`/`BeautifulSoup` (probe sitemap & website)
> Status: **Lapis 1 - Terverifikasi** (semua bukti berupa URL publik yang dapat diakses ulang)

## 1. Metode

Dua jalur scraping independen, saling melengkapi:

| Script | Metode | Input | Output |
|---|---|---|---|
| `01-cari-agency.py` | Library `ddgs` (27 query × 9 kota; mesin pencari Bing/Brave/Ecosia/DuckDuckGo diblokir/degraded dari jaringan ini) | query per kota | `data/scraping/hasil-pencarian.csv` (61 domain) |
| `02-profil-agency.py` | Fetch homepage + landing page, ekstrak sinyal (kota, harga, WA, layanan) | 61 domain | `data/scraping/profil-agency.csv` |
| `03-sitemap-nasional.py` | Parse `sitemap.xml` / fallback link homepage 12 agency nasional | `kompetitor.csv` | `data/scraping/halaman-kota-nasional.csv` |
| `05-klasifikasi.py` | Klasifikasi URL: landing jasa vs event vs tag | hasil 03 | `data/scraping/halaman-kota-terklasifikasi.csv` |
| `04-agregasi.py` | Gabung & filter kualitas | semua di atas | `data/kompetitor-tambahan.csv`, `data/bukti-halaman-kota.csv` |

## 2. Temuan utama - jawaban atas "apakah agency Jawa mengincar Kalimantan?"

**Ya, hampir semuanya - dan skala jauh lebih besar dari estimasi audit manual sebelumnya.**

Audit manual lama (kolom `kanal_jual` di `kompetitor.csv`) hanya menandai **4 dari 12** agency nasional
sebagai pengincar kota Kalimantan. Scraping sitemap membuktikan **9 dari 12** punya landing page jasa
khusus kota Kalimantan:

| Agency | Landing jasa Kalimantan | Kota yang diincar |
|---|---|---|
| Publish Agency (Surabaya) | **164** + 76 halaman event komunitas | Balikpapan, Pontianak, Samarinda |
| WebNesia (Bekasi) | **34** | 11 wilayah (s/d Singkawang, Tarakan) |
| Karya Studio (Banyuwangi) | **30** | 10 kota (Banjarmasin → Tarakan) |
| Vodeco (Semarang) | **26** | Balikpapan, Banjarmasin, Pontianak, Samarinda |
| Lenteraweb (Kediri) | **22** | 11 wilayah (incl. Martapura) |
| Toekang Digital (Solo) | **20** | Balikpapan, Palangka Raya, Pontianak |
| Etnicode DS | **11** | 6 wilayah (incl. Banjarbaru, Kalteng) |
| Longetiv | **9** | 8 kota |
| Mierakigai | 2 | Balikpapan, Banjarmasin |
| Bima Creative | 0 (hanya tag) | - |
| Digital360 | 0 | - |
| GetFound | 0 | - |

Catatan Publish Agency: selain 164 landing jasa, situsnya memuat **76 halaman gathering komunitas
per kota** (`publish.co.id/community/gathering/pontianak` dll) - indikasi aktivitas offline nyata di
Kalimantan, bukan sekadar SEO.

## 3. Temuan kedua - 48 agency baru di luar basis `kompetitor.csv`

Dari 61 domain hasil pencarian, **48 belum terdaftar** di `kompetitor.csv`; **22 di antaranya eksplisit
mengincar kota Kalimantan**. Yang paling relevan (bukan direktori/portal):

| Agency | Mengincar | Sinyal harga publik |
|---|---|---|
| beemata.co.id | Balikpapan, Samarinda, Bontang | ada (perlu parse lanjut) |
| nuswalab.com | Balikpapan, Samarinda | Rp 3,5 jt |
| corefreelancers.id | Balikpapan, Bontang, Samarinda | Rp 500 rb |
| promptverse.id | Bontang, Balikpapan, Banjarmasin, Palangka Raya, Samarinda | Rp 8,8 jt |
| hanzdigital.com | Singkawang, Kalbar | Rp 700 rb |
| websitemurah.co.id | Balikpapan | murah (SEO) |
| crackincode.com | Balikpapan, Banjarbaru, Banjarmasin, Bontang | tidak publik |
| sinteniki.com | Balikpapan, Samarinda (SEO/AEO/GEO) | tidak publik |
| industrikreatif.co.id | Balikpapan (iklan Google, migas & logistik) | tidak publik |
| resolusiweb.com | Samarinda, Loa Janan, Balikpapan | Rp 300 rb |
| jasaseoweb.id | Samarinda | Rp 8 jt |
| jasamurahweb.com | Samarinda, Banjarmasin + lintas Kalimantan | Rp 62 rb (website) |
| juraganweb.co.id | Banjarmasin, Pontianak, Kalbar | tidak publik |
| jasaseo.id | Banjarmasin, Balikpapan, Kalsel, Palangkaraya | Rp 3,5 jt |
| ourweb.id | Banjarmasin (Google Ads) | mulai Rp 1, jt-an |
| hasbildev.shop | Pontianak, Balikpapan, Banjarmasin, Singkawang | Rp 18,5 jt |
| mastung.id | Pontianak, Singkawang, Kalbar | Rp 30 rb |

Sisanya (26) adalah domain tanpa kaitan Kalimantan eksplisit: direktori (topseos.com,
top10digitalagency.com), jasa umum lintas kota, dan portal non-agency - diberi flag
"Perlu verifikasi manual" di CSV.

## 4. Implikasi strategis

1. **Kanal `google_search` di kota Kalimantan jauh lebih kontested dari estimasi awal.**
   "Jasa digital marketing Banjarmasin" tidak hanya diperebutkan 4 agency - minimal 9 agency nasional
   membangun landing page SEO per-kota secara sistematis (Publish Agency saja 164 halaman).
2. **Kota kecil justru lebih longgar**: Tarakan, Singkawang, Bontang baru diincar 2-4 agency nasional.
   Peluang local SEO di kota tier-2 masih terbuka lebar.
3. **Perang harga bawah sudah ramai** di segmen SEO/website murah (Rp 30 rb-700 rb) - memperkuat
3. **Perang harga bawah sudah ramai** di segmen SEO/website murah (Rp 30 rb-700 rb) - memperkuat
   positioning "bukan yang termurah, tapi yang terukur" (pilar Terukur).
4. **Celah kompetitor tetap sama**: tidak ada yang berbasis fisik di Kalimantan selain 38 lokal
   (yang mayoritas tanpa performance ads & reporting terukur).

## 5. Keterbatasan

- `ddgs` kena rate-limit - beberapa query Balikpapan/Banjarmasin kembali hasil lebih sedikit dari ideal;
  cakupan pencarian tidak ekshaustif (61 domain, bukan seluruh pasar).
- Deteksi harga otomatis (regex `Rp`) bisa salah tangkap (contoh: "rp 500" = asumsi ribuan).
- Klasifikasi URL berbasis pola; landing jasa belum diverifikasi manual satu per satu.
- Bukti halaman = bukti *investasi SEO*, belum tentu bukti *klien aktif* di kota tersebut.

## File hasil

```
research/data/kompetitor-tambahan.csv      48 agency baru (struktur mengikuti kompetitor.csv)
research/data/bukti-halaman-kota.csv       9 agency nasional + bukti URL
research/data/scraping/hasil-pencarian.csv 61 domain mentah dari mesin pencari
research/data/scraping/profil-agency.csv   profil sinyal per domain
research/data/scraping/halaman-kota-nasional.csv        URL mentah per agency
research/data/scraping/halaman-kota-terklasifikasi.csv  terklasifikasi jasa/event/tag
research/scraping/log-*.txt                log eksekusi
```
