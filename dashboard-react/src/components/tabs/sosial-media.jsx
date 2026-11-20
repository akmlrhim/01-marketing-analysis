import React from 'react'
import platform from '../../data/platform.json'
import ecommerce from '../../data/ecommerce.json'
import biaya from '../../data/biaya-iklan.json'
import channel from '../../data/channel-matrix.json'
import metrics from '../../data/metrics.json'
import { BarList, Heatmap, Kpis, NoteLine, Panel, RangePlot, Table } from '../ui.jsx'
import { fmt1, fmt2, fmtInt } from '../../lib/format.js'

const KANAL = ['instagram', 'tiktok', 'facebook', 'whatsapp', 'google_maps', 'linkedin', 'youtube', 'marketplace', 'google_search', 'ai_search', 'kol']

export default function SosialMedia() {
  const kpis = [
    { label: 'Platform', value: metrics.n_platform, hint: 'jangkauan iklan 18+' },
    { label: 'Platform terbesar', value: metrics.platform_terbesar, hint: `${fmt1(metrics.platform_terbesar_juta)} juta pengguna` },
    { label: 'Marketplace', value: metrics.n_ecommerce, hint: `terbesar: ${metrics.ecommerce_terbesar}` },
    { label: 'Benchmark iklan', value: metrics.n_ad_benchmark, hint: 'CPM / CPC / CPL / retainer' },
  ]

  const ranges = biaya.filter((r) => r.objective !== 'Retainer').map((r) => ({
    label: `${r.kanal} · ${r.metrik}`,
    min: r.batas_bawah_rp,
    max: r.batas_atas_rp,
    mid: r.titik_tengah_rp,
  }))

  const heatRows = channel.map((r) => ({ name: r.industri, values: KANAL.map((k) => r[k] || 0) }))

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel kicker="Panggung iklan" title="Jangkauan platform (juta)" note="Iklan 18+; DataReportal Digital 2027.">
          <BarList
            data={[...platform].sort((a, b) => b.jangkauan_iklan_juta - a.jangkauan_iklan_juta)
              .map((r) => ({ label: r.platform, value: r.jangkauan_iklan_juta }))}
            format={(v) => `${fmt1(v)} jt`}
          />
        </Panel>

        <Panel kicker="Belanja online" title="E-commerce & social commerce" note="MAU aktif dan GMV 2025 (US$ miliar).">
          <BarList
            data={[...ecommerce].sort((a, b) => b.mau_juta - a.mau_juta)
              .map((r) => ({ label: r.platform, value: r.mau_juta }))}
            format={(v) => `${fmtInt(v)} jt`}
          />
          <p className="panel-note" style={{ marginTop: 14 }}>
            {metrics.ecommerce_terbesar} memimpin; kategori utama dan GMV ada di tabel sumber.
          </p>
        </Panel>

        <Panel
          kicker="Biaya"
          title="Benchmark biaya iklan & retainer"
          note="Garis = rentang wajar, belah ketupat = titik tengah. Skala log Rupiah."
          className="span-2"
        >
          <RangePlot data={ranges} height={Math.max(320, ranges.length * 30 + 50)} />
          <div style={{ marginTop: 12 }}>
            <NoteLine>
              CPM = biaya per 1.000 tayangan, CPC = biaya per klik, CPL = biaya per kontak.
              Makin ke bawah, makin mahal tapi makin dekat ke penjualan.
            </NoteLine>
          </div>
        </Panel>

        <Panel
          kicker="Peta kanal"
          title="Prioritas kanal per industri"
          note="Skor 1–5: seberapa efektif kanal untuk menjual ke industri itu di kota Kalimantan."
          className="span-2"
        >
          <Heatmap
            rows={heatRows}
            cols={KANAL}
            valueAt={(row, col) => row.values[KANAL.indexOf(col)]}
            max={5}
            format={(v) => fmtInt(v)}
            nameWidth={190}
          />
        </Panel>

        <Panel kicker="Detail kanal" title="Tabel prioritas kanal" note={`${channel.length} industri × ${KANAL.length} kanal.`} className="span-2">
          <Table
            tall
            columns={[
              { key: 'industri', label: 'Industri' },
              ...KANAL.map((k) => ({ key: k, label: k.replace('_', ' '), align: 'right', render: (r) => r[k] })),
              { key: 'rata', label: 'Rata-rata', align: 'right', render: (r) => fmt2(r.rata_rata) },
            ]}
            rows={channel}
            rowKey={(r) => r.industri}
          />
        </Panel>
      </div>
    </>
  )
}
