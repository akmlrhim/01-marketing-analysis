const int = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 })
const dec1 = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const dec2 = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export const fmtInt = (value) => (value == null ? '-' : int.format(value))
export const fmt1 = (value) => (value == null ? '-' : dec1.format(value))
export const fmt2 = (value) => (value == null ? '-' : dec2.format(value))

export function fmtJuta(value, digits = 1) {
  if (value == null) return '-'
  const formatted = digits === 2 ? dec2.format(value / 1e6) : dec1.format(value / 1e6)
  return `Rp${formatted} jt`
}

export function fmtRp(value) {
  if (value == null) return '-'
  return `Rp${int.format(value)}`
}

export const fmtPct = (value, digits = 1) => (value == null ? '-' : `${digits === 2 ? dec2.format(value) : dec1.format(value)}%`)

export const fmtSigned = (value) => (value > 0 ? `+${value}` : `${value}`)

export function shortLabel(text, max = 24) {
  if (!text) return ''
  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}
