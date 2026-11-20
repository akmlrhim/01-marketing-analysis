import React, { useMemo, useState } from 'react'
import {
  CartesianGrid, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis, ZAxis,
} from 'recharts'
import pain from '../../data/pain.json'
import metrics from '../../data/metrics.json'
import { Badge, BarList, ChartTooltip, Kpis, Panel, Table } from '../ui.jsx'
import { fmt1 } from '../../lib/format.js'
import { MONO, SURFACE_STROKE } from '../ui.jsx'

const SEGMENTS = ['Semua', ...Array.from(new Set(pain.map((p) => p.segmen))).sort()]
const KUADRAN = ['Kritis', 'Sering tapi ringan', 'Jarang tapi berat', 'Monitor']

export default function PainPoint() {
  const [segmen, setSegmen] = useState('Semua')
  const [kuadran, setKuadran] = useState('Semua')

  const filtered = useMemo(() => pain.filter((row) =>
    (segmen === 'Semua' || row.segmen === segmen) &&
    (kuadran === 'Semua' || row.kuadran === kuadran),
  ), [segmen, kuadran])

  const top = [...filtered].sort((a, b) => b.skor_prioritas - a.skor_prioritas).slice(0, 12)
    .map((r) => ({ label: r.pain_point, value: r.skor_prioritas }))
  const bubble = filtered.map((r) => ({ ...r, x: r.frekuensi, y: r.dampak, z: r.kesiapan_bayar }))

  const kpis = [
    { label: 'Pain point', value: metrics.n_pain_point, hint: 'lintas segmen' },
    { label: 'Kuadran kritis', value: metrics.n_pain_kritis, hint: 'frekuensi & dampak ≥ 4' },
    { label: 'Prioritas #1', value: fmt1(metrics.skor_pain_prioritas), hint: metrics.pain_point_prioritas },
    { label: 'Segmen tercakup', value: SEGMENTS.length - 1, hint: 'UMKM, SME, B2B, klinik, dll.' },
  ]

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel
          kicker="Prioritas"
          title="12 pain point tertinggi"
          note="Skor = 0,4 × frekuensi + 0,4 × dampak + 0,2 × kesiapan bayar."
          actions={
            <>
              <div className="seg" role="group" aria-label="Filter segmen">
                {SEGMENTS.slice(0, 5).map((s) => (
                  <button key={s} aria-pressed={segmen === s} onClick={() => setSegmen(s)}>{s}</button>
                ))}
              </div>
              <div className="seg" role="group" aria-label="Filter kuadran">
                {['Semua', ...KUADRAN].map((k) => (
                  <button key={k} aria-pressed={kuadran === k} onClick={() => setKuadran(k)}>{k === 'Sering tapi ringan' ? 'Sering·ringan' : k === 'Jarang tapi berat' ? 'Jarang·berat' : k}</button>
                ))}
              </div>
            </>
          }
        >
          <BarList data={top} format={(v) => fmt1(v)} max={5} />
        </Panel>

        <Panel
          kicker="Peta masalah"
          title="Peta pain point"
          note="X = frekuensi, Y = dampak, ukuran = kesiapan bayar. Titik kanan-atas = masalah yang rela dibayar."
        >
          <div className="chart" style={{ height: 430 }}>
            <ResponsiveContainer>
              <ScatterChart margin={{ top: 10, right: 16, bottom: 22, left: -6 }}>
                <CartesianGrid strokeDasharray="2 4" />
                <XAxis type="number" dataKey="x" domain={[0.5, 5.5]} name="Frekuensi" tickCount={5} />
                <YAxis type="number" dataKey="y" domain={[0.5, 5.5]} name="Dampak" tickCount={5} width={44} />
                <ZAxis type="number" dataKey="z" range={[40, 420]} name="Kesiapan bayar" />
                <Tooltip content={<ChartTooltip note="Skor 5 = penilaian analis atas bukti desk, bukan hasil survei." />} />
                {KUADRAN.map((k, i) => (
                  <Scatter
                    key={k}
                    name={k}
                    data={bubble.filter((r) => r.kuadran === k)}
                    fill={MONO[i]}
                    fillOpacity={0.75}
                    stroke={SURFACE_STROKE}
                    strokeWidth={1}
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', fontSize: 11, color: 'var(--muted)', marginTop: 8 }}>
            {KUADRAN.map((k, i) => (
              <span key={k}><i style={{ display: 'inline-block', width: 9, height: 9, background: MONO[i], borderRadius: '50%', marginRight: 5 }} />{k}</span>
            ))}
          </div>
        </Panel>

        <Panel kicker="Tabel prioritas" title="Daftar pain point" note={`${filtered.length} baris sesuai filter.`} className="span-2">
          <Table
            tall
            columns={[
              { key: 'peringkat', label: '#', align: 'right', render: (r) => <span className="row-rank">{r.peringkat}</span> },
              { key: 'pain', label: 'Pain point', render: (r) => r.pain_point },
              { key: 'segmen', label: 'Segmen' },
              { key: 'frekuensi', label: 'Frek.', align: 'right' },
              { key: 'dampak', label: 'Dampak', align: 'right' },
              { key: 'bayar', label: 'Bayar', align: 'right', render: (r) => r.kesiapan_bayar },
              { key: 'skor', label: 'Skor', align: 'right', render: (r) => fmt1(r.skor_prioritas) },
              { key: 'kuadran', label: 'Kuadran', render: (r) => <Badge tone={r.kuadran === 'Kritis' ? 'solid' : 'ghost'}>{r.kuadran}</Badge> },
            ]}
            rows={[...filtered].sort((a, b) => a.peringkat - b.peringkat)}
            rowKey={(r, i) => `${r.pain_point}-${i}`}
          />
        </Panel>
      </div>
    </>
  )
}
