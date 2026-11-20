import React from 'react'
import {
  Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import trust from '../../data/trust.json'
import metrics from '../../data/metrics.json'
import { Badge, ChartTooltip, Kpis, NoteLine, Panel, Table } from '../ui.jsx'
import { fmt1 } from '../../lib/format.js'
import { MONO } from '../ui.jsx'

export default function Persepsi() {
  const kpis = [
    { label: 'Dimensi dinilai', value: metrics.n_persepsi_dimensi, hint: 'kepentingan vs kinerja agensi' },
    { label: 'Gap terbesar', value: fmt1(trust[0]?.gap), hint: trust[0]?.dimensi },
    { label: 'Prioritas #2', value: fmt1(trust[1]?.gap), hint: trust[1]?.dimensi },
    { label: 'Kesenjangan terendah', value: fmt1(trust[trust.length - 1]?.gap), hint: trust[trust.length - 1]?.dimensi },
  ]

  const data = [...trust].reverse().map((r) => ({
    label: r.dimensi.length > 34 ? `${r.dimensi.slice(0, 33)}…` : r.dimensi,
    nama: r.dimensi,
    kepentingan: r.kepentingan,
    kinerja: r.kinerja_agency,
    gap: r.gap,
  }))

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel
          kicker="Importance–performance"
          title="Kesenjangan kepercayaan"
          note="Gap = kepentingan − kinerja agensi. Gap besar = harapan tinggi tapi pasar kecewa = peluang positioning."
          className="span-2"
        >
          <div className="chart" style={{ height: 560 }}>
            <ResponsiveContainer>
              <BarChart data={data} layout="vertical" margin={{ left: 6, right: 34, top: 4, bottom: 4 }} barGap={2}>
                <CartesianGrid strokeDasharray="2 4" horizontal={false} />
                <XAxis type="number" domain={[0, 5.5]} tick={{ fontSize: 10 }} />
                <YAxis type="category" dataKey="label" width={200} tick={{ fontSize: 10 }} interval={0} />
                <Tooltip content={<ChartTooltip note="Penilaian analis berdasarkan pola keluhan dan audit agensi, bukan survei." />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                <Legend iconType="square" wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="kepentingan" name="Kepentingan" fill={MONO[0]} radius={[0, 3, 3, 0]} />
                <Bar dataKey="kinerja" name="Kinerja agensi" fill={MONO[4]} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Daftar dimensi" title="Tabel kesenjangan" note="Diurutkan dari gap terbesar." className="span-2">
          <Table
            tall
            columns={[
              { key: 'prioritas', label: '#', align: 'right', render: (r) => <span className="row-rank">{r.prioritas_perbaikan}</span> },
              { key: 'dimensi', label: 'Dimensi' },
              { key: 'kepentingan', label: 'Kepentingan', align: 'right', render: (r) => fmt1(r.kepentingan) },
              { key: 'kinerja', label: 'Kinerja agensi', align: 'right', render: (r) => fmt1(r.kinerja_agency) },
              { key: 'gap', label: 'Gap', align: 'right', render: (r) => <strong>{fmt1(r.gap)}</strong> },
              { key: 'status', label: 'Status', render: (r) => <Badge tone="ghost">{r.status}</Badge> },
            ]}
            rows={trust}
            rowKey={(r) => r.dimensi}
          />
          <div style={{ marginTop: 16 }}>
            <NoteLine>
              Dua gap terbesar, <strong>{trust[0]?.dimensi}</strong> dan <strong>{trust[1]?.dimensi}</strong>,
              menjadi dasar janji positioning: laporan revenue yang bisa diverifikasi.
            </NoteLine>
          </div>
        </Panel>
      </div>
    </>
  )
}
