import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000/api'

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
