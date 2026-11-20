import React from 'react'
import {
  Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer,
  Tooltip, XAxis, YAxis,
} from 'recharts'
import kompetitor from '../../data/kompetitor.json'
import kotaCount from '../../data/kompetitor-kota.json'
import tipeCount from '../../data/kompetitor-tipe.json'
import layananCount from '../../data/layanan-count.json'
import serviceMatrix from '../../data/service-matrix.json'
import harga from '../../data/harga-kompetitor.json'
import metrics from '../../data/metrics.json'
import { Badge, BarList, ChartTooltip, Heatmap, Kpis, NoteLine, Panel, Table } from '../ui.jsx'
import { MONO, SURFACE_STROKE } from '../ui.jsx'

const LAYANAN = Object.keys(serviceMatrix[0] || {}).filter((k) => k !== 'nama' && k !== 'Total layanan')

export default function Kompetitor() {
  const kpis = [
    { label: 'Total kompetitor', value: metrics.n_kompetitor, hint: 'terpetakan di Kalimantan' },
    { label: 'Lokal', value: metrics.n_kompetitor_lokal, hint: 'agency berbasis Kalimantan' },
    { label: 'Nasional', value: metrics.n_kompetitor_nasional, hint: 'jaringan luar yang menyasar Kalimantan' },
    { label: 'Harga terbuka', value: metrics.n_harga_transparan, hint: 'berani memajang harga' },
    { label: 'Layanan terlaris', value: metrics.layanan_terlaris_jumlah, hint: metrics.layanan_terlaris },
  ]

  const matrixRows = [...serviceMatrix]
    .sort((a, b) => b['Total layanan'] - a['Total layanan'])
    .slice(0, 25)
    .map((row) => ({ name: row.nama, values: LAYANAN.map((k) => row[k] || 0) }))

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel kicker="Sebaran" title="Sebaran kota agensi" note="Kota dengan batang pendek = pasar sepi pesaing lokal.">
          <div className="chart" style={{ height: 330 }}>
            <ResponsiveContainer>
              <BarChart data={kotaCount} layout="vertical" margin={{ left: 6, right: 22 }}>
                <CartesianGrid strokeDasharray="2 4" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 10 }} allowDecimals={false} />
                <YAxis type="category" dataKey="kota_utama" width={106} tick={{ fontSize: 10 }} interval={0} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                <Bar dataKey="jumlah" name="Agensi" fill={MONO[1]} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Komposisi" title="Lokal vs nasional" note="Porsi lawan lokal dan jaringan luar.">
          <div className="chart" style={{ height: 250 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={tipeCount} dataKey="jumlah" nameKey="tipe_sederhana" innerRadius={58} outerRadius={94} paddingAngle={2} stroke={SURFACE_STROKE}>
                  {tipeCount.map((_, i) => <Cell key={i} fill={i === 0 ? MONO[0] : MONO[4]} />)}
                </Pie>
                <Tooltip content={<ChartTooltip />} />
                <Legend iconType="square" wrapperStyle={{ fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <NoteLine>Nasional kuat di SEO/web; lokal kuat di relasi tapi lemah di laporan terukur.</NoteLine>
        </Panel>

        <Panel kicker="Penawaran" title="Layanan paling sering dijual" note="Makin panjang, makin ramai. Makin sulit tampil beda.">
          <BarList
            data={[...layananCount].sort((a, b) => b.jumlah - a.jumlah).map((r) => ({ label: r.layanan, value: r.jumlah }))}
            format={(v) => `${v} agensi`}
          />
        </Panel>

        <Panel kicker="Peta layanan" title="Matrix layanan (top 25)" note="Baris = agency, kolom = kategori layanan. Kotak gelap = agency menjual layanan itu.">
          <Heatmap
            rows={matrixRows}
            cols={LAYANAN}
            valueAt={(row, col) => row.values[LAYANAN.indexOf(col)]}
            max={1}
            format={(v) => (v ? 'Ya' : 'Tidak')}
          />
        </Panel>

        <Panel kicker="Sinyal publik" title="Harga yang dipajang kompetitor" note="Harga pajangan, bukan penawaran resmi. Sumber: situs publik agency." className="span-2">
          <Table
            tall
            columns={[
              { key: 'nama', label: 'Agency' },
              { key: 'kota', label: 'Basis' },
              { key: 'tipe', label: 'Tipe', render: (r) => <Badge tone={r.tipe_sederhana === 'Lokal' ? 'solid' : 'dark'}>{r.tipe_sederhana}</Badge> },
              { key: 'sinyal', label: 'Sinyal harga', wrap: true, render: (r) => r.sinyal_harga },
              { key: 'url', label: 'Sumber', render: (r) => <a href={r.url} target="_blank" rel="noreferrer">Buka ↗</a> },
            ]}
            rows={harga}
            rowKey={(r) => r.nama}
          />
        </Panel>

        <Panel kicker="Database" title="Daftar kompetitor" note="Kekuatan dan celah tiap agency dari audit publik." className="span-2">
          <Table
            tall
            columns={[
              { key: 'nama', label: 'Agency' },
              { key: 'kota', label: 'Kota utama', render: (r) => r.kota_utama || r.basis_kota },
              { key: 'tipe', label: 'Tipe', render: (r) => r.tipe_sederhana },
              { key: 'status', label: 'Verifikasi', render: (r) => <Badge tone={r.status_verifikasi === 'Terverifikasi' ? 'solid' : 'ghost'}>{r.status_verifikasi}</Badge> },
              { key: 'aktif', label: 'Status aktif', render: (r) => r.status_aktif || '-' },
              { key: 'layanan', label: 'Jumlah layanan', align: 'right', render: (r) => r.jumlah_layanan },
              { key: 'kekuatan', label: 'Kekuatan', wrap: true, render: (r) => r.kekuatan },
              { key: 'celah', label: 'Celah', wrap: true, render: (r) => r.celah },
            ]}
            rows={kompetitor}
            rowKey={(r) => r.nama}
          />
        </Panel>
      </div>
    </>
  )
}
