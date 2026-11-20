import React from 'react'
import metrics from '../../data/metrics.json'
import layanan from '../../data/layanan-winning.json'
import paket from '../../data/layanan-industri.json'
import addon from '../../data/layanan-addon.json'
import biaya from '../../data/biaya-iklan.json'
import layananCount from '../../data/layanan-count.json'
import { BarList, Kpis, NoteLine, Panel, RangePlot, Table } from '../ui.jsx'
import { fmtJuta } from '../../lib/format.js'

export default function LayananWinning() {
  const kpis = [
    { label: 'Tangga paket', value: metrics.n_paket, hint: 'dari audit hingga enterprise' },
    { label: 'Harga masuk', value: fmtJuta(metrics.harga_entry_rp), hint: metrics.paket_entry },
    { label: 'Paket inti', value: fmtJuta(metrics.harga_growth_rp), hint: 'Growth per bulan' },
    { label: 'Paket per industri', value: metrics.n_paket_industri, hint: 'penawaran yang dikustom' },
    { label: 'Add-on', value: metrics.n_addon, hint: 'layanan di luar langganan' },
  ]

  const retainer = biaya.filter((r) => r.objective === 'Retainer').map((r) => ({
    label: r.kanal,
    min: r.batas_bawah_rp,
    max: r.batas_atas_rp,
    mid: r.titik_tengah_rp,
  }))

  return (
    <>
      <Kpis items={kpis} />
      <div className="panel-grid">
        <Panel kicker="Arsitektur harga" title="Tangga paket" note="Usulan internal; harga harus diuji dengan survei willingness-to-pay." className="span-2">
          <Table
            columns={[
              { key: 'tier', label: 'Tier' },
              { key: 'target', label: 'Target' },
              { key: 'harga', label: 'Rentang harga', align: 'right', render: (r) => `${fmtJuta(r.harga_min_rp, r.harga_min_rp % 1e6 ? 2 : 0)} – ${fmtJuta(r.harga_max_rp, r.harga_max_rp % 1e6 ? 2 : 0)}` },
              { key: 'satuan', label: 'Satuan' },
              { key: 'isi', label: 'Isi paket', wrap: true, render: (r) => r.isi },
              { key: 'tujuan', label: 'Tujuan', wrap: true, render: (r) => r.tujuan },
            ]}
            rows={layanan}
            rowKey={(r) => r.tier}
          />
        </Panel>

        <Panel kicker="Kustomisasi" title="Paket per industri" note="Versi paket inti yang disesuaikan dengan masalah industri.">
          <Table
            columns={[
              { key: 'paket', label: 'Paket', render: (r) => <strong>{r.paket}</strong> },
              { key: 'industri', label: 'Industri' },
              { key: 'harga', label: 'Harga', align: 'right', render: (r) => `${fmtJuta(r.harga_min_rp, 0)}–${fmtJuta(r.harga_max_rp, 0)}` },
              { key: 'kpi', label: 'KPI', wrap: true, render: (r) => r.kpi },
            ]}
            rows={paket}
            rowKey={(r) => r.paket}
          />
        </Panel>

        <Panel kicker="Tambahan" title="Add-on" note="Dijual di luar langganan bulanan.">
          <Table
            columns={[
              { key: 'layanan', label: 'Add-on' },
              { key: 'harga', label: 'Rentang', align: 'right', render: (r) => `${fmtJuta(r.harga_min_rp, 0)}–${fmtJuta(r.harga_max_rp, 0)}` },
              { key: 'satuan', label: 'Satuan' },
            ]}
            rows={addon}
            rowKey={(r) => r.layanan}
          />
          <div style={{ marginTop: 16 }}>
            <NoteLine>Harga di atas adalah <strong>usulan analis</strong>, bukan hasil survei harga pasar.</NoteLine>
          </div>
        </Panel>

        <Panel kicker="Konteks pasar" title="Layanan yang paling sering dijual kompetitor" note="Dari 56 agency yang diaudit.">
          <BarList
            data={[...layananCount].sort((a, b) => b.jumlah - a.jumlah).slice(0, 10)
              .map((r) => ({ label: r.layanan, value: r.jumlah }))}
            format={(v) => `${v} agency`}
          />
          <div style={{ marginTop: 16 }}>
            <NoteLine>Banyak yang menjual konten dan website. Kami membedakan diri lewat laporan dan KPI yang terukur, bukan harga termurah.</NoteLine>
          </div>
        </Panel>

        <Panel kicker="Pembanding" title="Benchmark retainer" note="Rentang langganan pasar; garis = rentang, belah ketupat = titik tengah.">
          <RangePlot data={retainer} height={Math.max(180, retainer.length * 42 + 40)} />
          <p className="panel-note" style={{ marginTop: 10 }}>
            {retainer.length} benchmark. Semua angka dalam Rupiah, skala logaritmik.
          </p>
        </Panel>
      </div>
    </>
  )
}
