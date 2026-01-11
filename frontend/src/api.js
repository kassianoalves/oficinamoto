import axios from 'axios'
import { authStorage } from './utils/authStorage.js'

// Função para detectar a URL da API dinamicamente
function getApiBaseUrl() {
  // Primeiro tenta variável de ambiente (Vite)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Se não estiver em desenvolvimento local (localhost), tenta descobrir dinamicamente
  const protocol = window.location.protocol
  const hostname = window.location.hostname
  const port = window.location.port ? `:${window.location.port}` : ''
  
  // Se estiver em localhost:5174 (Vite dev), aponta para localhost:8000 (Django)
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    if (window.location.port === '5174') {
      return `${protocol}//localhost:8000/api`
    }
  }
  
  // Se estiver em outro IP (ex: 192.168.1.99), aponta para o mesmo IP com porta 8000
  return `${protocol}//${hostname}:8000/api`
}

// Base da API (configurável via env ou auto-detectada)
let API_BASE = getApiBaseUrl()

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Função para obter configuração da API dinamicamente
export async function updateApiConfig() {
  try {
    // Tenta pegar configuração do servidor
    const response = await axios.get(`${API_BASE}/config/`, {
      timeout: 3000
    })
    
    if (response.data.api_url) {
      API_BASE = response.data.api_url
      api.defaults.baseURL = API_BASE
      console.log('✓ Configuração da API detectada:', API_BASE)
      return response.data
    }
  } catch (error) {
    // Se falhar, mantém a URL já detectada
    console.warn('⚠ Não foi possível obter config da API, usando:', API_BASE)
  }
  
  return {
    api_url: API_BASE,
    detected: true
  }
}

// Chamar ao inicializar a aplicação
updateApiConfig()

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use((config) => {
  const token = authStorage.getToken()
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api

