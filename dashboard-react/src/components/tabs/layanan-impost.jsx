import React, { useState } from 'react'
import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import impost from '../../data/impost-layanan.json'
import metrics from '../../data/metrics.json'
import { Badge, BarList, ChartTooltip, Heatmap, Kpis, NoteLine, Panel, RangePlot, Table } from '../ui.jsx'
import { fmt1, fmt2, fmtJuta } from '../../lib/format.js'
import { MONO } from '../ui.jsx'

const WILAYAH = [
  { key: 'demand_kalsel', label: 'Kalsel' },
  { key: 'demand_kalimantan', label: 'Kalimantan' },
  { key: 'demand_nasional', label: 'Nasional' },
]

export default function LayananImpost() {
  const [wilayah, setWilayah] = useState('demand_kalsel')
  const signalKey = wilayah.replace('demand_', 'sinyal_cari_')

  const kpis = [
    { label: 'Layanan IMPOST', value: metrics.n_impost_layanan, hint: 'harga pasar vs harga ideal' },
    { label: 'Demand Kalsel', value: fmt1(metrics.impost_demand_kalsel_skor), hint: metrics.impost_demand_tertinggi_kalsel },
    { label: 'Demand nasional', value: fmt1(metrics.impost_demand_nasional_skor), hint: metrics.impost_demand_tertinggi_nasional },
    { label: 'Paling sepi', value: fmt2(metrics.impost_demand_kalimantan_skor), hint: metrics.impost_demand_terendah_kalimantan },
  ]

  const priceData = impost.map((r) => ({
    label: r.layanan,
    min: r.harga_pasar_min_rp,
    max: r.harga_pasar_max_rp,
    mid: r.tengah_ideal_rp,
  }))
  const signalData = [...impost].sort((a, b) => b[signalKey] - a[signalKey]).slice(0, 10)
    .map((r) => ({ label: r.layanan, value: r[signalKey] }))

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel
          kicker="Permintaan relatif"
          title="Peta demand layanan per wilayah"
          note="Skor 1-5, makin gelap makin ramai dicari. Bandingkan antar layanan dalam satu kolom wilayah."
          className="span-2"
        >
          <Heatmap
            rows={impost.map((r) => ({ name: r.layanan, values: WILAYAH.map((w) => r[w.key]) }))}
            cols={WILAYAH.map((w) => w.label)}
            valueAt={(row, col) => row.values[WILAYAH.findIndex((w) => w.label === col)]}
            max={5}
            format={(v) => fmt2(v)}
            nameWidth={250}
          />
        </Panel>

        <Panel
          kicker="Proxy minat"
          title="Sinyal pencarian"
          note="Jumlah domain unik untuk query “jasa X di wilayah Y” (Tavily)."
          actions={
            <div className="seg" role="group" aria-label="Pilih wilayah">
              {WILAYAH.map((w) => (
                <button key={w.key} aria-pressed={wilayah === w.key} onClick={() => setWilayah(w.key)}>{w.label}</button>
              ))}
            </div>
          }
        >
          <div className="chart" style={{ height: 340 }}>
            <ResponsiveContainer>
              <BarChart data={signalData} layout="vertical" margin={{ left: 4, right: 28, top: 4 }}>
                <CartesianGrid strokeDasharray="2 4" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 10 }} allowDecimals={false} />
                <YAxis type="category" dataKey="label" width={168} tick={{ fontSize: 9.5 }} interval={0} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                <Bar dataKey="value" name="Domain unik" fill={MONO[1]} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Pasokan" title="Pasokan kompetitor" note="Berapa dari 56 agensi yang menjual layanan terkait. Pasokan rendah + demand tinggi = celah.">
          <BarList
            data={[...impost].sort((a, b) => b.pasokan_kompetitor - a.pasokan_kompetitor)
              .map((r) => ({ label: r.layanan, value: r.pasokan_kompetitor }))}
            format={(v) => `${v} agensi`}
          />
        </Panel>

        <Panel
          kicker="Posisi harga"
          title="Harga pasar vs harga ideal"
          note="Garis = rentang harga pasar. Belah ketupat = titik tengah harga ideal usulan kami. Skala log."
          className="span-2"
        >
          <RangePlot data={priceData} height={480} />
          <div style={{ marginTop: 12 }}>
            <NoteLine>
              Garis abu dan titik tengah ideal memakai skala log karena harga melompat dari ratusan ribu sampai puluhan juta.
              Bacalah <strong>posisinya</strong>, bukan angkanya persis.
            </NoteLine>
          </div>
        </Panel>

        <Panel kicker="Detail lengkap" title="Tabel harga & demand" note="Harga ideal adalah hipotesis usulan; harga pasar dirangkai dari sinyal publik." className="span-2">
          <Table
            tall
            columns={[
              { key: 'layanan', label: 'Layanan' },
              { key: 'kategori', label: 'Kategori' },
              { key: 'pasar', label: 'Harga pasar', align: 'right', render: (r) => `${fmtJuta(r.harga_pasar_min_rp, 1)}–${fmtJuta(r.harga_pasar_max_rp, 1)}` },
              { key: 'ideal', label: 'Harga ideal', align: 'right', render: (r) => `${fmtJuta(r.harga_ideal_min_rp, 1)}–${fmtJuta(r.harga_ideal_max_rp, 1)}` },
              { key: 'posisi', label: 'Ideal/pasar', align: 'right', render: (r) => fmt2(r.posisi_vs_pasar) },
              { key: 'kalsel', label: 'Demand Kalsel', align: 'right', render: (r) => fmt2(r.demand_kalsel) },
              { key: 'kalimantan', label: 'Demand Kalimantan', align: 'right', render: (r) => fmt2(r.demand_kalimantan) },
              { key: 'nasional', label: 'Demand nasional', align: 'right', render: (r) => fmt2(r.demand_nasional) },
              { key: 'status', label: 'Status', render: () => <Badge tone="ghost">Hipotesis</Badge> },
            ]}
            rows={impost}
            rowKey={(r) => r.layanan}
          />
        </Panel>
      </div>
    </>
  )
}
