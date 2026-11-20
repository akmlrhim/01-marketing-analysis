import React, { useState } from 'react'
import metrics from '../../data/metrics.json'
import sumber from '../../data/sumber.json'
import { Badge, Kpis, NoteLine, Panel, Table } from '../ui.jsx'

const LANGKAH = [
  'Validasi kolom wajib CSV',
  'Bersihkan tipe data & fallback kolom baru',
  'Hitung skor industri berbobot (SAW)',
  'Hitung prioritas pain point & trust gap',
  'Hitung kompetisi terukur dari 56 agency',
  'Agregasi kota, platform, harga iklan',
  'Tulis dashboard-streamlit/data/derived/*.json',
]

const KAMUS = [
  ['skor_tertimbang', '0,20 ukuran + 0,20 pertumbuhan + 0,20 belanja digital + 0,15 kompetisi rendah + 0,15 akses + 0,10 margin retainer'],
  ['prioritas', '≤ 3,50 potensial · 3,50–3,80 prioritas · > 3,80 prioritas inti'],
  ['kompetisi_terukur', '1 + 4 × (1 − cakupan pesaing); skor 5 = paling sedikit pesaing'],
  ['skor_prioritas pain', '0,4 frekuensi + 0,4 dampak + 0,2 kesiapan bayar'],
  ['kuadran kritis', 'frekuensi ≥ 4 dan dampak ≥ 4'],
  ['gap', 'kepentingan − kinerja agensi (Importance–Performance Analysis)'],
  ['demand_skor', '1 + 4 × (0,6 sinyal pencarian + 0,4 pasokan kompetitor), dinormalisasi per wilayah'],
  ['posisi_vs_pasar', 'titik tengah harga ideal ÷ titik tengah harga pasar; < 1 lebih murah, > 1 premium'],
]

export default function Metodologi() {
  const [showJson, setShowJson] = useState(false)
  const kpis = [
    { label: 'Sumber data', value: metrics.n_sumber, hint: 'dengan URL dan status verifikasi' },
    { label: 'Provinsi', value: metrics.n_provinsi, hint: 'seluruh Kalimantan' },
    { label: 'Kompetitor', value: metrics.n_kompetitor, hint: 'audit publik' },
    { label: 'Dihasilkan', value: '20 Nov 2026', hint: metrics.generated_at },
  ]

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel kicker="Reproducibility" title="Alur analisis" note="Pipeline Python: dashboard-streamlit/analysis.py → dashboard-streamlit/data/derived/ → JSON statis untuk React." className="span-2">
          <div className="steps">
            {LANGKAH.map((langkah, i) => (
              <div className="step" key={langkah}>
                <b>LANGKAH {i + 1}</b>
                <span>{langkah}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 16 }}>
            <NoteLine>
              Untuk menyegarkan data: jalankan <code>python dashboard-streamlit/analysis.py</code>, lalu{' '}
              <code>npm run sync:data</code> di folder <code>dashboard-react</code>.
            </NoteLine>
          </div>
        </Panel>

        <Panel kicker="Dua lapis angka" title="Cara membaca status data" note="Jangan mencampur data sekunder dengan skor hipotesis.">
          <div className="prose">
            <h4>Lapis 1: Terverifikasi</h4>
            <p>Statistik BPS, APJII, DataReportal, harga yang dipajang kompetitor. Bisa dilacak ke URL dan diberi label hijau di dashboard asli; di sini ditandai badge <Badge tone="solid">Solid</Badge>.</p>
            <h4>Lapis 2: Hipotesis</h4>
            <p>Skor 1–5, harga ideal, prioritas pain point. Penilaian analis di atas bukti desk research, tanpa responden. Ditandai badge <Badge tone="ghost">Garis putus</Badge>.</p>
            <h4>Konsekuensi</h4>
            <p>Tidak ada sampling, margin of error, uji signifikansi, atau reliabilitas antar-penilai. Angka ini layak untuk prioritisasi awal, bukan klaim pasar.</p>
          </div>
        </Panel>

        <Panel kicker="Rumus" title="Data dictionary" note="Ringkasan cara setiap angka dihitung.">
          <div className="prose">
            {KAMUS.map(([key, value]) => (
              <p key={key}><code>{key}</code><br />{value}</p>
            ))}
          </div>
        </Panel>

        <Panel kicker="Daftar" title="Sumber & status verifikasi" note="50 sumber dengan URL asli." className="span-2">
          <Table
            tall
            columns={[
              { key: 'id', label: 'ID' },
              { key: 'topik', label: 'Topik' },
              { key: 'sumber', label: 'Sumber', render: (r) => r.sumber },
              { key: 'url', label: 'URL', render: (r) => <a href={r.url} target="_blank" rel="noreferrer">Buka ↗</a> },
              { key: 'tahun', label: 'Tahun', align: 'right', render: (r) => r.tahun },
              { key: 'status', label: 'Status', render: (r) => <Badge tone={r.status === 'Terverifikasi' ? 'solid' : 'ghost'}>{r.status}</Badge> },
            ]}
            rows={sumber}
            rowKey={(r) => r.id}
          />
        </Panel>

        <Panel
          kicker="Mentah"
          title="Metrics JSON"
          note="Objek ringkasan yang dihasilkan pipeline dan dipakai KPI di seluruh dashboard."
          className="span-2"
          actions={
            <button className="seg-button" aria-pressed={showJson} onClick={() => setShowJson((v) => !v)}>
              {showJson ? 'Sembunyikan' : 'Tampilkan'}
            </button>
          }
        >
          {showJson ? (
            <pre className="json-view">{JSON.stringify(metrics, null, 2)}</pre>
          ) : (
            <p className="panel-note">{Object.keys(metrics).length} metrik tersedia. Klik “Tampilkan” untuk melihat semuanya.</p>
          )}
        </Panel>
      </div>
    </>
  )
}
