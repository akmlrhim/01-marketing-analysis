import React, { useEffect, useState } from 'react'
import metrics from './data/metrics.json'
import Industri from './components/tabs/industri.jsx'
import PainPoint from './components/tabs/pain-point.jsx'
import Kompetitor from './components/tabs/kompetitor.jsx'
import LayananWinning from './components/tabs/layanan-winning.jsx'
import LayananImpost from './components/tabs/layanan-impost.jsx'
import SosialMedia from './components/tabs/sosial-media.jsx'
import Persepsi from './components/tabs/persepsi.jsx'
import PasarKota from './components/tabs/pasar-kota.jsx'
import Metodologi from './components/tabs/metodologi.jsx'

const PAGES = [
  { id: 'winning', label: 'Industri Winning', eyebrow: '1 / Prioritas', lede: 'Industri mana yang paling menguntungkan untuk digodok duluan? Bandingkan daya tarik, kemudahan masuk, dan sensitivitas peringkat terhadap data kompetitor nyata.', component: <Industri mode="winning" /> },
  { id: 'pain', label: 'Pain Point Owner', eyebrow: '2 / Masalah', lede: 'Kami tidak menjual “sosmed”. Kami menjual obat untuk masalah yang sering dialami calon klien dan sudah mereka bayar.', component: <PainPoint /> },
  { id: 'potensial', label: 'Industri Potensial', eyebrow: '3 / Cadangan', lede: 'Industri di bawah ambang prioritas. Layak dipantau dan dicoba saat tim punya sisa kapasitas.', component: <Industri mode="potensial" /> },
  { id: 'kompetitor', label: 'Kompetitor Agency', eyebrow: '4 / Lanskap', lede: 'Siapa lawan kita dan seberapa kuat? 56 agency terpetakan: sebaran kota, tipe, layanan yang dijual, dan sinyal harga publik.', component: <Kompetitor /> },
  { id: 'layanan', label: 'Layanan Winning', eyebrow: '5 / Produk', lede: 'Produk kita dijual bagaimana? Tangga paket, kustomisasi per industri, add-on, dan benchmark retainer pasar.', component: <LayananWinning /> },
  { id: 'impost', label: 'Layanan IMPOST', eyebrow: '6 / Portofolio', lede: 'Harga ideal layanan kami dibandingkan harga pasar, dan seberapa ramai permintaan di Kalsel, Kalimantan, serta nasional.', component: <LayananImpost /> },
  { id: 'sosial', label: 'Sosial Media', eyebrow: '7 / Kanal', lede: 'Iklan digital itu mahal tidak? Jangkauan platform, belanja e-commerce, benchmark biaya iklan, dan prioritas kanal per industri.', component: <SosialMedia /> },
  { id: 'persepsi', label: 'Persepsi Agency', eyebrow: '8 / Positioning', lede: 'Harapan tinggi dengan kinerja pasar yang rendah adalah peluang. Ukur kesenjangan kepentingan dan kinerja di 14 dimensi.', component: <Persepsi /> },
  { id: 'kota', label: 'Pasar Kota', eyebrow: '9 / Wilayah', lede: 'Di kota mana kita bermain? Peta gelembung, penduduk, UMK, UMKM, dan kondisi makro lima provinsi.', component: <PasarKota /> },
  { id: 'metodologi', label: 'Metodologi', eyebrow: '10 / Audit', lede: 'Dari mana setiap angka berasal dan bagaimana cara menghitungnya? Alur pipeline, kamus rumus, dan 50 sumber data.', component: <Metodologi /> },
]

const SIDEBAR_KEY = 'dashboard-sidebar-collapsed-v2'

function pageFromPath() {
  const segment = window.location.pathname.replace(/\/+$/, '').split('/').pop()
  if (!segment || segment === PAGES[0].id) return PAGES[0].id
  return PAGES.some((page) => page.id === segment) ? segment : PAGES[0].id
}

function CollapseIcon({ collapsed }) {
  return (
    <svg
      className={collapsed ? 'rotated' : ''}
      width="18"
      height="18"
      viewBox="0 0 20 20"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      aria-hidden="true"
    >
      <path d="M12 4L6 10l6 6" />
    </svg>
  )
}

function MenuIcon({ open }) {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
      {open ? <path d="M4 4l12 12M16 4L4 16" /> : <path d="M3 6h14M3 10h14M3 14h14" />}
    </svg>
  )
}

export default function App() {
  const [active, setActive] = useState(pageFromPath)
  const [menuOpen, setMenuOpen] = useState(false)
  const [collapsed, setCollapsed] = useState(() => {
    try {
      const saved = window.localStorage.getItem(SIDEBAR_KEY)
      return saved === null ? true : saved === '1'
    } catch {
      return true
    }
  })
  const expanded = !collapsed
  const page = PAGES.find((p) => p.id === active) || PAGES[0]

  useEffect(() => {
    try {
      window.localStorage.setItem(SIDEBAR_KEY, collapsed ? '1' : '0')
    } catch {}
  }, [collapsed])

  useEffect(() => {
    function onPopState() {
      setActive(pageFromPath())
    }
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  function navigate(id) {
    const path = id === PAGES[0].id ? '/' : `/${id}`
    if (window.location.pathname !== path) window.history.pushState({}, '', path)
    setActive(id)
    setMenuOpen(false)
    window.scrollTo({ top: 0, behavior: 'instant' })
  }

  return (
    <div className={`app ${expanded ? 'expanded' : ''}`}>
      <a className="skip-link" href="#konten">Lewati ke konten</a>

      {menuOpen && <button className="scrim" aria-label="Tutup menu" onClick={() => setMenuOpen(false)} />}

      <aside
        className={`sidebar ${menuOpen ? 'open' : ''} ${expanded ? 'expanded' : ''}`}
        aria-label="Navigasi dashboard"
      >
        <button
          className="collapse-toggle"
          aria-label={expanded ? 'Perkecil sidebar' : 'Perbesar sidebar'}
          aria-expanded={expanded}
          title={expanded ? 'Perkecil sidebar' : 'Perbesar sidebar'}
          onClick={() => setCollapsed((value) => !value)}
        >
          <CollapseIcon collapsed={!expanded} />
        </button>
        <div className="nav-label">Halaman</div>
        <nav className="nav">
          {PAGES.map((item) => (
            <button
              key={item.id}
              className="nav-item"
              aria-label={item.label}
              title={item.label}
              aria-current={active === item.id ? 'page' : undefined}
              onClick={() => navigate(item.id)}
            >
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      <main className="main" id="konten">
        <div className="mobile-bar">
          <button aria-label={menuOpen ? 'Tutup menu' : 'Buka menu'} aria-expanded={menuOpen} onClick={() => setMenuOpen((v) => !v)}>
            <MenuIcon open={menuOpen} />
          </button>
          <span>{page.label}</span>
        </div>

        <header className="page-head">
          <div>
            <p className="eyebrow">{page.eyebrow}</p>
            <h2>{page.label}</h2>
            <p className="lede">{page.lede}</p>
          </div>
          <div className="head-meta">Diperbarui · {metrics.generated_at}</div>
        </header>

        <div className="status-banner" role="status">
          <div>
            <strong>Status data:</strong> {metrics.data_status}. Skor 1-5 adalah penilaian analis, bukan hasil survei.
            Gunakan untuk prioritisasi awal. <a href="/metodologi" onClick={(e) => { e.preventDefault(); navigate('metodologi') }}>Baca metodologi</a>.
          </div>
        </div>

        {page.component}
      </main>
    </div>
  )
}
