import React, { useMemo, useState } from 'react'
import {
  Bar, BarChart, CartesianGrid, Cell, PolarAngleAxis, PolarGrid, Radar, RadarChart,
  ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis, ZAxis,
} from 'recharts'
import industri from '../../data/industri.json'
import metrics from '../../data/metrics.json'
import { Badge, ChartTooltip, Kpis, NoteLine, Panel, Table } from '../ui.jsx'
import { fmt2 } from '../../lib/format.js'
import { MONO, SURFACE_STROKE } from '../ui.jsx'

const KRITERIA = [
  ['ukuran_pasar', 'Ukuran pasar'],
  ['pertumbuhan', 'Pertumbuhan'],
  ['belanja_digital', 'Belanja digital'],
  ['kompetisi_rendah', 'Kompetisi rendah'],
  ['akses_dan_sales_cycle', 'Akses & siklus jual'],
  ['margin_retainer', 'Margin retainer'],
]

const PRIORITAS = ['Prioritas inti', 'Prioritas', 'Potensial']
const shades = { 'Prioritas inti': MONO[0], Prioritas: MONO[2], Potensial: MONO[4] }

function priorityBadge(value) {
  const tone = value === 'Prioritas inti' ? 'solid' : value === 'Prioritas' ? 'dark' : 'ghost'
  return <Badge tone={tone}>{value}</Badge>
}

export default function Industri({ mode = 'winning' }) {
  const [basis, setBasis] = useState('hipotesis')
  const [pilih, setPilih] = useState(industri[0]?.industri)

  const data = useMemo(() => {
    const measured = basis === 'terukur'
    return industri.map((row) => ({
      ...row,
      skor: measured ? row.skor_tertimbang_terukur : row.skor_tertimbang,
      peringkatAktif: measured ? row.peringkat_terukur : row.peringkat,
      kategoriAktif: measured ? row.prioritas_terukur : row.prioritas,
    }))
  }, [basis])

  const rows = mode === 'potensial'
    ? data.filter((row) => row.kategoriAktif === 'Potensial')
    : data.filter((row) => row.kategoriAktif !== 'Potensial')

  const selected = data.find((row) => row.industri === pilih) || data[0]
  const rataRata = KRITERIA.map(([key]) =>
    data.reduce((sum, row) => sum + row[key], 0) / data.length,
  )
  const radarData = KRITERIA.map(([key, label], i) => ({
    kriteria: label,
    industri: selected[key],
    rataRata: Number(rataRata[i].toFixed(2)),
  }))
  const deltaData = useMemo(
    () => [...data]
      .filter((row) => row.delta_peringkat != null)
      .sort((a, b) => Math.abs(b.delta_peringkat) - Math.abs(a.delta_peringkat))
      .slice(0, 12)
      .map((row) => ({
        label: row.industri.length > 26 ? `${row.industri.slice(0, 25)}…` : row.industri,
        nama: row.industri,
        delta: row.delta_peringkat,
      })),
    [data],
  )

  const kpis = mode === 'potensial'
    ? [
        { label: 'Industri potensial', value: rows.length, hint: 'di bawah ambang prioritas' },
        { label: 'Skor tertinggi', value: fmt2(Math.max(...rows.map((r) => r.skor))), hint: rows[0]?.industri },
        { label: 'Rata-rata skor', value: fmt2(rows.reduce((s, r) => s + r.skor, 0) / rows.length), hint: 'seluruh industri potensial' },
      ]
    : [
        { label: 'Industri juara', value: rows.length, hint: 'prioritas inti + prioritas' },
        { label: 'Skor tertinggi', value: fmt2(metrics.skor_industri_prioritas), hint: metrics.industri_prioritas },
        { label: 'Prioritas inti', value: basis === 'terukur' ? metrics.n_prioritas_inti_terukur : 5, hint: basis === 'terukur' ? 'dengan kompetisi terukur' : 'dasar penilaian analis' },
        { label: 'Naik peringkat', value: metrics.n_industri_naik, hint: 'setelah kompetisi dihitung dari data' },
      ]

  return (
    <>
      <Kpis items={kpis} />

      <div className="panel-grid">
        <Panel
          kicker="Peta peluang"
          title="Peta industri: akses × daya tarik"
          note="Sumbu X = kemudahan masuk & closing. Sumbu Y = skor daya tarik. Ukuran gelembung = ukuran pasar."
          className="span-2"
          actions={
            <div className="seg" role="group" aria-label="Dasar skor industri">
              <button aria-pressed={basis === 'hipotesis'} onClick={() => setBasis('hipotesis')}>Hipotesis</button>
              <button aria-pressed={basis === 'terukur'} onClick={() => setBasis('terukur')}>Terukur</button>
            </div>
          }
        >
          <div className="chart" style={{ height: 460 }}>
            <ResponsiveContainer>
              <ScatterChart margin={{ top: 12, right: 20, bottom: 24, left: 4 }}>
                <CartesianGrid strokeDasharray="2 4" />
                <XAxis type="number" dataKey="akses_dan_sales_cycle" domain={[0, 5.5]} name="Akses" tickCount={6} label={{ value: 'Akses & siklus jual →', position: 'insideBottom', offset: -14, fill: '#6b747d', fontSize: 10 }} />
                <YAxis type="number" dataKey="skor" domain={[2.5, 4.6]} name="Skor" tickCount={6} width={44} />
                <ZAxis type="number" dataKey="ukuran_pasar" range={[70, 700]} name="Ukuran pasar" />
                <Tooltip content={<ChartTooltip note="Klik baris di tabel untuk melihat profil industri." />} />
                {PRIORITAS.map((kategori) => (
                  <Scatter
                    key={kategori}
                    name={kategori}
                    data={rows.filter((row) => row.kategoriAktif === kategori)}
                    fill={shades[kategori]}
                    fillOpacity={0.78}
                    stroke={SURFACE_STROKE}
                    strokeWidth={1}
                    onClick={(point) => setPilih(point?.industri || point?.payload?.industri)}
                    cursor="pointer"
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel kicker="Daftar lengkap" title="Peringkat industri" note="Urutan berdasarkan dasar skor yang dipilih.">
          <Table
            tall
            columns={[
              { key: 'peringkat', label: '#', align: 'right', render: (r) => <span className="row-rank">{r.peringkatAktif}</span> },
              { key: 'industri', label: 'Industri', render: (r) => <button className="link-button" onClick={() => setPilih(r.industri)}>{r.industri}</button> },
              { key: 'skor', label: 'Skor', align: 'right', render: (r) => fmt2(r.skor) },
              { key: 'kategori', label: 'Status', render: (r) => priorityBadge(r.kategoriAktif) },
            ]}
            rows={[...rows].sort((a, b) => a.peringkatAktif - b.peringkatAktif)}
            rowKey={(r) => r.industri}
          />
        </Panel>

        <Panel
          kicker="Profil industri"
          title={selected?.industri || '-'}
          note={selected?.catatan}
          actions={<Badge tone="ghost">{selected?.status_data}</Badge>}
        >
          <div className="chart" style={{ height: 280 }}>
            <ResponsiveContainer>
              <RadarChart data={radarData} outerRadius="72%">
                <PolarGrid />
                <PolarAngleAxis dataKey="kriteria" tick={{ fontSize: 10 }} />
                <Radar name="Rata-rata" dataKey="rataRata" stroke={MONO[4]} fill={MONO[5]} fillOpacity={0.25} strokeDasharray="3 3" />
                <Radar name={selected?.industri || 'Industri'} dataKey="industri" stroke={MONO[0]} fill={MONO[1]} fillOpacity={0.25} />
                <Tooltip content={<ChartTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', fontSize: 11.5, color: 'var(--muted)' }}>
            <span><i style={{ display: 'inline-block', width: 12, height: 3, background: MONO[0], verticalAlign: 'middle', marginRight: 6 }} />Industri terpilih</span>
            <span><i style={{ display: 'inline-block', width: 12, height: 3, background: MONO[4], verticalAlign: 'middle', marginRight: 6 }} />Rata-rata 30 industri</span>
          </div>
        </Panel>

        {mode === 'winning' && (
          <Panel
            kicker="Uji sensitivitas"
            title="Dampak data kompetitor pada peringkat"
            note="Selisih peringkat saat kompetisi dihitung dari 56 agency nyata. Positif = naik, negatif = turun."
            className="span-2"
          >
            <div className="chart" style={{ height: 380 }}>
              <ResponsiveContainer>
                <BarChart data={deltaData} margin={{ top: 8, right: 8, bottom: 64, left: -18 }}>
                  <CartesianGrid strokeDasharray="2 4" vertical={false} />
                  <XAxis dataKey="label" angle={-38} textAnchor="end" interval={0} height={72} tick={{ fontSize: 9 }} />
                  <YAxis tick={{ fontSize: 10 }} width={40} />
                  <Tooltip content={<ChartTooltip note="Perubahan peringkat (peringkat lama − peringkat terukur)." />} cursor={{ fill: 'rgba(247,248,249,.04)' }} />
                  <Bar dataKey="delta" name="Δ peringkat" radius={[2, 2, 0, 0]}>
                    {deltaData.map((entry) => (
                      <Cell key={entry.nama} fill={entry.delta >= 0 ? MONO[0] : MONO[4]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ marginTop: 14 }}>
              <NoteLine>
                <strong>{metrics.industri_naik_terbanyak}</strong> naik {metrics.delta_peringkat_maks} peringkat;{' '}
                <strong>{metrics.industri_turun_terbanyak}</strong> turun {Math.abs(metrics.delta_peringkat_min)} peringkat.{' '}
                Prioritas inti menyusut dari 5 menjadi {metrics.n_prioritas_inti_terukur} industri.
              </NoteLine>
            </div>
          </Panel>
        )}
      </div>
    </>
  )
}
