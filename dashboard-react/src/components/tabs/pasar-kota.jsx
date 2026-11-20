import React from 'react'
import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Scatter, ScatterChart,
  Tooltip, XAxis, YAxis, ZAxis,
} from 'recharts'
import kota from '../../data/kota.json'
import makro from '../../data/makro.json'
import metrics from '../../data/metrics.json'
import { Badge, BarList, ChartTooltip, Kpis, Panel, Table } from '../ui.jsx'
import { fmt1, fmtInt, fmtJuta } from '../../lib/format.js'
import { MONO } from '../ui.jsx'

export default function PasarKota() {
  const kpis = [
    { label: 'Kota dipetakan', value: metrics.n_kota, hint: 'di 5 provinsi Kalimantan' },
    { label: 'Total penduduk kota', value: fmtInt(metrics.total_penduduk_kota), hint: 'akumulasi 9 kota' },
    { label: 'Penduduk terbesar', value: 'Samarinda', hint: `${fmtInt(metrics.total_penduduk_provinsi)} jiwa se-Kalimantan` },
    { label: 'UMK tertinggi', value: fmtJuta(3983882, 2), hint: 'Samarinda, 2026' },
  ]

  const peta = kota.map((row) => ({ ...row, x: row.lon, y: row.lat, z: row.penduduk }))
  const pop = [...kota].sort((a, b) => b.penduduk - a.penduduk).slice(0, 8)
    .map((r) => ({ label: r.kota, value: r.penduduk }))
  const umk = [...kota].sort((a, b) => b.umk_rp - a.umk_rp)
    .map((r) => ({ label: r.kota, value: r.umk_rp / 1e6 }))
  const umkm = kota.filter((r) => r.umkm_unit != null).sort((a, b) => b.umkm_unit - a.umkm_unit)
    .map((r) => ({ label: r.kota, value: r.umkm_unit }))
  const provinsi = [...makro].sort((a, b) => b.pertumbuhan_terbaru - a.pertumbuhan_terbaru)

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel
          kicker="Geografi"
          title="Peta gelembung kota"
          note="Posisi sesuai koordinat kota; luas gelembung = jumlah penduduk."
          className="span-2"
        >
          <div className="chart" style={{ height: 430 }}>
            <ResponsiveContainer>
              <ScatterChart margin={{ top: 12, right: 18, bottom: 22, left: 6 }}>
                <CartesianGrid strokeDasharray="2 4" />
                <XAxis type="number" dataKey="x" name="Bujur" domain={[108.5, 119]} tickCount={6} />
                <YAxis type="number" dataKey="y" name="Lintang" domain={[-4, 2]} tickCount={6} width={46} />
                <ZAxis type="number" dataKey="z" range={[120, 1500]} name="Penduduk" />
                <Tooltip
                  content={<ChartTooltip note="Kota dengan gelembung besar = pasar dengan penduduk lebih banyak." />}
                  formatter={(value, name) => [fmtInt(value), name]}
                />
                <Scatter data={peta} fill={MONO[1]} fillOpacity={0.7} stroke={MONO[0]} strokeWidth={1} />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Penduduk" title="Penduduk kota" note="Pasar = orang; makin banyak jiwa, makin besar kue.">
          <BarList data={pop} format={(v) => fmtInt(v)} />
        </Panel>

        <Panel kicker="Daya beli" title="UMK 2026 (Rp juta)" note="Proksi daya beli dan kemampuan membayar jasa.">
          <BarList data={umk} format={(v) => `Rp${fmt1(v)} jt`} />
        </Panel>

        <Panel kicker="Calon klien" title="UMKM yang terdata" note="Hanya 4 kota yang punya data UMKM terdata.">
          <BarList data={umkm} format={(v) => fmtInt(v)} />
        </Panel>

        <Panel kicker="Makro provinsi" title="Pertumbuhan ekonomi Q3 2026" note="YoY, persen. Dibandingkan dengan nasional 5,47%.">
          <div className="chart" style={{ height: 240 }}>
            <ResponsiveContainer>
              <BarChart data={provinsi} layout="vertical" margin={{ left: 10, right: 24, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="2 4" horizontal={false} />
                <XAxis type="number" domain={[0, 7]} tick={{ fontSize: 10 }} unit="%" />
                <YAxis type="category" dataKey="provinsi" width={116} tick={{ fontSize: 10 }} interval={0} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                <Bar dataKey="pertumbuhan_terbaru" name="Pertumbuhan (%)" fill={MONO[1]} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Konektivitas" title="Penetrasi internet 2026" note="Persen populasi; nasional 81,72%.">
          <div className="chart" style={{ height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={[...makro].sort((a, b) => b.penetrasi_internet_terbaru - a.penetrasi_internet_terbaru)} layout="vertical" margin={{ left: 10, right: 26 }}>
                <CartesianGrid strokeDasharray="2 4" horizontal={false} />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10 }} unit="%" />
                <YAxis type="category" dataKey="provinsi" width={116} tick={{ fontSize: 10 }} interval={0} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                <Bar dataKey="penetrasi_internet_terbaru" name="Penetrasi (%)" fill={MONO[3]} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Detail data" title="Tabel kota" note="Status diambil dari sumber masing-masing baris.">
          <Table
            tall
            columns={[
              { key: 'kota', label: 'Kota' },
              { key: 'provinsi', label: 'Provinsi' },
              { key: 'penduduk', label: 'Penduduk', align: 'right', render: (r) => fmtInt(r.penduduk) },
              { key: 'umk', label: 'UMK 2026', align: 'right', render: (r) => fmtJuta(r.umk_rp, 2) },
              { key: 'umkm', label: 'UMKM', align: 'right', render: (r) => r.umkm_unit == null ? '-' : fmtInt(r.umkm_unit) },
              { key: 'internet', label: 'Internet', align: 'right', render: (r) => `${fmt1(r.internet_provinsi_persen)}%` },
              { key: 'status', label: 'Status', render: (r) => <Badge tone={r.status_data?.includes('Dukcapil') ? 'solid' : 'ghost'}>{r.status_data?.split(';')[0]}</Badge> },
            ]}
            rows={kota}
            rowKey={(r) => r.kota}
          />
        </Panel>
      </div>
    </>
  )
}
