import axios from 'axios'

// Detectar a URL da API dinamicamente baseada na URL do navegador
const getAPIBase = () => {
  // Em desenvolvimento, sempre usar o proxy configurado no Vite
  if (import.meta.env.DEV) {
    return '/api'
  }
  
  // Em produção, usar o mesmo host do frontend
  const protocol = window.location.protocol
  const host = window.location.hostname
  const port = 8000
  
  return `${protocol}//${host}:${port}/api`
}

const API_BASE = getAPIBase()

console.log('API Base URL:', API_BASE)

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api
