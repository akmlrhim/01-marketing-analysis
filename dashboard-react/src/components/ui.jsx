import React from 'react'

/** Tangga monokrom untuk chart, dari terang ke gelap. */
export const MONO = ['#17181a', '#4b5259', '#767d85', '#a2a8af', '#c8ccd0', '#e1e4e6']
export const SURFACE_STROKE = '#ffffff'

export function Panel({ kicker, title, note, actions, children, className = '' }) {
  return (
    <section className={`panel ${className}`}>
      {(title || actions) && (
        <div className="panel-head">
          <div>
            {kicker && <div className="panel-kicker">{kicker}</div>}
            {title && <h3>{title}</h3>}
          </div>
          {actions && <div className="panel-actions">{actions}</div>}
        </div>
      )}
      {note && <p className="panel-note">{note}</p>}
      {children}
    </section>
  )
}

export function Kpis({ items }) {
  return (
    <div className="kpi-grid">
      {items.map((item, index) => (
        <div className="kpi" key={`${item.label}-${index}`}>
          <div className="kpi-label">{item.label}</div>
          <div className="kpi-value">{item.value}</div>
          {item.hint && <div className="kpi-hint" title={item.hint}>{item.hint}</div>}
        </div>
      ))}
    </div>
  )
}

export function Badge({ children, tone = '' }) {
  return <span className={`badge ${tone}`}>{children}</span>
}

export function Table({ columns, rows, rowKey = (row, i) => i, tall = false, empty = 'Tidak ada baris yang cocok. Ubah filter untuk melihat data lain.' }) {
  if (!rows?.length) return <p className="panel-note">{empty}</p>
  return (
    <div className={`table-wrap ${tall ? 'tall' : ''}`}>
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} className={col.align === 'right' ? 'num' : ''}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={rowKey(row, index)}>
              {columns.map((col) => {
                const content = col.render ? col.render(row, index) : row[col.key]
                return (
                  <td
                    key={col.key}
                    className={col.align === 'right' ? 'num' : col.wrap ? 'wrap-cell' : ''}
                  >
                    {content ?? '-'}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function BarList({ data, labelKey = 'label', valueKey = 'value', format = (v) => v, max }) {
  const peak = max ?? Math.max(...data.map((d) => d[valueKey] || 0), 1)
  return (
    <div className="bar-list">
      {data.map((row, index) => (
        <div className="bar-row" key={`${row[labelKey]}-${index}`}>
          <div className="bar-label" title={row[labelKey]}>{row[labelKey]}</div>
          <div className="bar-track">
            <div
              className="bar-fill"
              style={{ width: `${Math.max(2, ((row[valueKey] || 0) / peak) * 100)}%` }}
            />
          </div>
          <div className="bar-value">{format(row[valueKey])}</div>
        </div>
      ))}
    </div>
  )
}

export function Heatmap({ rows, cols, valueAt, max, format = (v) => v, nameWidth = 170 }) {
  return (
    <div className="heat-scroll">
      <div
        className="heat"
        style={{ gridTemplateColumns: `${nameWidth}px repeat(${cols.length}, 26px)` }}
      >
        <div />
        {cols.map((col) => (
          <div className="heat-head" title={col} key={col}>{col}</div>
        ))}
        {rows.map((row) => (
          <React.Fragment key={row.name}>
            <div className="heat-name" title={row.name}>{row.name}</div>
            {cols.map((col) => {
              const value = valueAt(row, col) || 0
              const ratio = max ? Math.min(1, value / max) : value
              return (
                <div
                  className="heat-cell"
                  key={col}
                  title={`${row.name} · ${col}: ${format(value)}`}
                  style={{
                    background: `rgb(var(--ink) / ${0.04 + ratio * 0.66})`,
                    borderColor: `rgb(var(--ink) / ${0.08 + ratio * 0.16})`,
                  }}
                />
              )
            })}
          </React.Fragment>
        ))}
      </div>
      <div className="heat-legend">
        <span>Rendah</span>
        {[0.08, 0.25, 0.45, 0.65, 0.8].map((alpha) => (
          <i key={alpha} style={{ background: `rgb(var(--ink) / ${alpha})` }} />
        ))}
        <span>Tinggi</span>
      </div>
    </div>
  )
}

/** Grafik rentang harga dengan skala log, dibuat dengan SVG (tanpa dependensi ekstra). */
export function RangePlot({ data, height = 320, ticks = [1e5, 1e6, 1e7, 1e8], unit = 'Rp' }) {
  const width = 820
  const margin = { top: 16, right: 26, bottom: 30, left: 196 }
  const innerW = width - margin.left - margin.right
  const rowH = (height - margin.top - margin.bottom) / data.length
  const all = data.flatMap((d) => [d.min, d.max]).filter((v) => v > 0)
  const lo = Math.log10(Math.min(...all) * 0.8)
  const hi = Math.log10(Math.max(...all) * 1.2)
  const x = (value) => margin.left + ((Math.log10(value) - lo) / (hi - lo)) * innerW
  const label = (value) => (value >= 1e6 ? `${value / 1e6}jt` : `${value / 1e3}rb`)

  return (
    <div className="range-plot">
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Rentang harga dengan skala logaritmik">
        {ticks
          .filter((t) => t >= 10 ** lo && t <= 10 ** hi)
          .map((tick) => (
            <g key={tick}>
              <line className="grid-line" x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} />
              <text className="axis-text" x={x(tick)} y={height - 10} textAnchor="middle">
                {label(tick)}
              </text>
            </g>
          ))}
        {data.map((d, i) => {
          const cy = margin.top + i * rowH + rowH / 2
          return (
            <g className="row-group" key={`${d.label}-${i}`}>
              <title>{`${d.label}: ${unit}${d.min.toLocaleString('id-ID')} – ${unit}${d.max.toLocaleString('id-ID')}`}</title>
              <text className="row-label" x={margin.left - 12} y={cy + 4} textAnchor="end">
                {d.label.length > 32 ? `${d.label.slice(0, 31)}…` : d.label}
              </text>
              <line className="row-line" x1={x(d.min)} x2={x(d.max)} y1={cy} y2={cy} />
              <rect x={x(d.min) - 2} y={cy - 6} width="4" height="12" rx="1" fill="#9aa2aa" />
              <rect x={x(d.max) - 2} y={cy - 6} width="4" height="12" rx="1" fill="#9aa2aa" />
              {d.mid != null && (
                <path className="mid-tick" d={`M ${x(d.mid)} ${cy - 7} L ${x(d.mid) + 6} ${cy} L ${x(d.mid)} ${cy + 7} L ${x(d.mid) - 6} ${cy} Z`} />
              )}
            </g>
          )
        })}
      </svg>
    </div>
  )
}

export function ChartTooltip({ active, payload, label, note }) {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <div className="tt-title">{label}</div>
      {payload.map((entry, index) => (
        <div className="tt-row" key={`${entry.dataKey}-${index}`}>
          <span>{entry.name}</span>
          <b>{entry.value}</b>
        </div>
      ))}
      {note && <div className="tt-note">{note}</div>}
    </div>
  )
}

export function NoteLine({ children }) {
  return <div className="note-line">{children}</div>
}
