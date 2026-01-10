/**
 * ========================================
 * FORMATADORES DE DADOS
 * ========================================
 * Funções para formatação de CPF, telefone, datas, etc.
 */

/**
 * Formata número de telefone brasileiro
 * Aceita 10 dígitos (fixo) ou 11 dígitos (celular)
 * @param {string} value - Número do telefone (apenas dígitos ou com formatação)
 * @returns {string} - Telefone formatado: (11) 99999-9999 ou (11) 9999-9999
 */
export const formatTelefone = (value) => {
  // Remove todos os caracteres não numéricos
  let cleaned = (value || '').replace(/\D/g, '')
  
  // Limita a 11 dígitos
  if (cleaned.length > 11) {
    cleaned = cleaned.slice(0, 11)
  }
  
  // Formata conforme quantidade de dígitos
  if (cleaned.length > 10) {
    // Celular: (11) 99999-9999
    return cleaned.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
  } else if (cleaned.length > 6) {
    // Fixo: (11) 9999-9999
    return cleaned.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3')
  } else if (cleaned.length > 2) {
    // Parcial: (11) 9999
    return cleaned.replace(/(\d{2})(\d{0,5})/, '($1) $2')
  }
  
  return cleaned
}

/**
 * Formata CPF brasileiro
 * @param {string} value - CPF (apenas dígitos ou com formatação)
 * @returns {string} - CPF formatado: 123.456.789-10
 */
export const formatCPF = (value) => {
  // Remove todos os caracteres não numéricos
  let cleaned = (value || '').replace(/\D/g, '')
  
  // Limita a 11 dígitos
  if (cleaned.length > 11) {
    cleaned = cleaned.slice(0, 11)
  }
  
  // Formata conforme quantidade de dígitos
  if (cleaned.length > 9) {
    // CPF completo: 123.456.789-10
    return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
  } else if (cleaned.length > 6) {
    // Parcial: 123.456.789
    return cleaned.replace(/(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3')
  } else if (cleaned.length > 3) {
    // Parcial: 123.456
    return cleaned.replace(/(\d{3})(\d{0,3})/, '$1.$2')
  }
  
  return cleaned
}

/**
 * Formata data ISO para formato brasileiro
 * @param {string} dateString - Data no formato ISO (YYYY-MM-DD)
 * @returns {string} - Data formatada: DD/MM/YYYY
 */
export const formatDate = (dateString) => {
  if (!dateString) return '-'
  
  try {
    const date = new Date(dateString)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    
    return `${day}/${month}/${year}`
  } catch (e) {
    return dateString
  }
}

/**
 * Formata data e hora ISO para formato brasileiro
 * @param {string} dateTimeString - Data/hora no formato ISO
 * @returns {string} - Data/hora formatada: DD/MM/YYYY HH:MM
 */
export const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return '-'
  
  try {
    const date = new Date(dateTimeString)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${day}/${month}/${year} ${hours}:${minutes}`
  } catch (e) {
    return dateTimeString
  }
}

/**
 * Formata valor monetário para formato brasileiro
 * @param {number} value - Valor numérico
 * @returns {string} - Valor formatado: R$ 1.234,56
 */
export const formatMoney = (value) => {
  if (value === null || value === undefined) return 'R$ 0,00'
  
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}
