# -*- coding: utf-8 -*-
"""Tambah isu AI/GEO + layanan baru: pain point, impost, demand sinyal, sumber, kanal."""
import io
import sys
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ---------------------------------------------------------------- 1. pain point
PAIN = """SME,Kompetitor lebih cepat karena pakai AI,4,4,4,Hipotesis,Desk research (tren AI marketing 2025-2026); validasi survei belum
SME,Tim belum paham pakai AI untuk marketing,4,3,3,Hipotesis,Desk research (tren AI marketing 2025-2026); validasi survei belum
UMKM,Konten makin generik karena semua pakai AI,4,3,2,Hipotesis,Desk research (tren AI marketing 2025-2026); validasi survei belum
Korporat/B2B,Brand tidak muncul di jawaban pencarian AI,3,4,3,Hipotesis,Desk research (tren AI marketing 2025-2026); validasi survei belum
"""
with open("research/data/pain-point.csv", "a", encoding="utf-8", newline="") as f:
    f.write(PAIN)
print("pain-point.csv: +4 baris")

# ---------------------------------------------------------------- 2. impost layanan
IMPOST = """AI Search Optimization (GEO),Data & Strategi,SEO,8000000,30000000,per bulan,"GEO Indonesia mulai US$500/bln (GTMLab US$499-1.999, SingRank US$500, S41); Arfadia SEO+GEO mulai Rp15 jt/bln (S41)",5000000,15000000,per bulan,"Masuk di bawah pemain nasional; bundle dengan SEO/website; jangkar paket Market Leader Rp15 jt; pasar masih awal sehingga edukasi jadi bagian penjualan",Hipotesis (usulan analis)
Chatbot & WhatsApp API,Teknologi,CRM / Lead,3000000,12000000,per proyek setup,"Platform WABA Wablas Rp32-119 rb/bln; Barantum mulai Rp897 rb/bln (S42); tarif percakapan Meta terpisah; jasa setup marketplace mulai Rp3 jt",4000000,10000000,per proyek setup,"Setup chatbot + integrasi WA + skenario CS; retainer operasional Rp1,5-3 jt/bln; jangkar paket Growth Rp6,5 jt",Hipotesis (usulan analis)
"""
with open("research/data/impost-layanan.csv", "a", encoding="utf-8", newline="") as f:
    f.write(IMPOST)
print("impost-layanan.csv: +2 baris")

# ---------------------------------------------------------------- 3. demand ringkas
DEMAND = """AI Search Optimization (GEO),Kalsel,8,0,,"skema.co.id; thriveagency.com; artemisdigital.com; vulkancreative.com; gen3marketing.com; greenbananaseo.com; youtube.com; instagram.com",MCP Tavily/Firecrawl search API (2026-11-06)
AI Search Optimization (GEO),Kalimantan,8,0,,"yesoptimist.com; forthea.com; gen3marketing.com; thriveagency.com; npdigital.com; consultgroupc.com; artemisdigital.com; youtube.com",MCP Tavily/Firecrawl search API (2026-11-06)
AI Search Optimization (GEO),Nasional,8,0,,"percepture.com; geoready.id; interodigital.com; omnius.so; olakses.com; gtmlab.ai; youtube.com; pr.chestercounty.com",MCP Tavily/Firecrawl search API (2026-11-06)
Chatbot & WhatsApp API,Kalsel,8,0,,"fastwork.id; wazapbro.com; sribu.com; bisolusi.com; chatbot.warbis.id; top4marketing.co.id; youtube.com; instagram.com",MCP Tavily/Firecrawl search API (2026-11-06)
Chatbot & WhatsApp API,Kalimantan,8,0,,"whatsapp.resmi.id; gmcsco.com; fastwork.id; askeva.io; wazapbro.com; qontak.com; sribu.com; youtube.com",MCP Tavily/Firecrawl search API (2026-11-06)
Chatbot & WhatsApp API,Nasional,8,1,Rp3.000.000,"qontak.com; barantum.com; sleekflow.io; fastwork.id; qiscus.com; wati.io; jatismobile.com; instagram.com",MCP Tavily/Firecrawl search API (2026-11-06)
"""
with open("research/data/scraping/demand-ringkas.csv", "a", encoding="utf-8", newline="") as f:
    f.write(DEMAND)
print("demand-ringkas.csv: +6 baris")

# ---------------------------------------------------------------- 4. sumber
SUMBER = """S41,Harga layanan GEO Indonesia,GTMLab & SingRank & Arfadia,https://www.gtmlab.ai/blog/best-geo-agencies-indonesia,2026,Artikel industri,Terverifikasi,"GEO mulai US$499-1.999/bln (GTMLab); SingRank US$500; Arfadia SEO+GEO mulai Rp15 jt/bln"
S42,Harga platform WhatsApp API,Wablas & Barantum,https://wablas.com/pricing,2026,Website penyedia,Terverifikasi,"Wablas Lite-Large Rp32-119 rb/bln; Barantum WABA mulai Rp897 rb/bln; tarif percakapan Meta terpisah"
"""
with open("research/data/sumber.csv", "a", encoding="utf-8", newline="") as f:
    f.write(SUMBER)
print("sumber.csv: +2 baris (S41, S42)")

# ---------------------------------------------------------------- 5. channel matrix + ai_search
src = "research/data/channel-matrix.csv"
with open(src, encoding="utf-8", newline="") as f:
    rows = list(csv.reader(f))
header = rows[0]
if "ai_search" not in header:
    gi = header.index("google_search")
    for r in rows:
        if r is rows[0]:
            r.insert(gi + 1, "ai_search")
        else:
            gs = float(r[gi])
            r.insert(gi + 1, str(max(1, min(5, round(gs * 0.8)))))
    with open(src, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)
print("channel-matrix.csv: +kolom ai_search (aturan: clamp(round(google_search*0.8)))")
