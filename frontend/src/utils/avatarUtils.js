/**
 * ========================================
 * UTILITÁRIOS PARA AVATAR
 * ========================================
 * Funções compartilhadas para gerenciamento de avatares de usuário
 */

/**
 * Gera um avatar SVG com as iniciais do nome do usuário
 * @param {string} name - Nome completo do usuário
 * @returns {string} - Data URL do SVG gerado
 */
export const makeInitialsAvatar = (name) => {
  // Extrai até 2 iniciais do nome
  const initials = (name || '')
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map(s => s.charAt(0).toUpperCase())
    .join('') || '?'
  
  // Gera SVG com gradiente e iniciais
  const svg = `
    <svg xmlns='http://www.w3.org/2000/svg' width='128' height='128' viewBox='0 0 64 64'>
      <defs>
        <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
          <stop offset='0%' stop-color='#667eea'/>
          <stop offset='100%' stop-color='#764ba2'/>
        </linearGradient>
      </defs>
      <circle cx='32' cy='32' r='32' fill='url(#g)'/>
      <text x='50%' y='54%' text-anchor='middle' dominant-baseline='middle' 
            font-family='Segoe UI, Arial' font-size='22' fill='#fff' font-weight='700'>
        ${initials}
      </text>
    </svg>`
  
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
}

/**
 * Adiciona cache-busting parameter em URLs de avatar
 * @param {string} url - URL do avatar
 * @returns {string} - URL com timestamp para evitar cache
 */
export const withCacheBust = (url) => {
  if (!url) return url
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}v=${Date.now()}`
}
