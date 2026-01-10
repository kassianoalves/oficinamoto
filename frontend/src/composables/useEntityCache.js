import { ref } from 'vue'
import api from '@/api'

const motos = ref([])
const clientes = ref([])

const loadMotos = async (force = false) => {
  if (motos.value.length && !force) return motos.value
  const res = await api.get('/motos/')
  motos.value = res.data.results || res.data || []
  return motos.value
}

const loadClientes = async (force = false) => {
  if (clientes.value.length && !force) return clientes.value
  const res = await api.get('/clientes/')
  clientes.value = res.data.results || res.data || []
  return clientes.value
}

export const useEntityCache = () => ({
  motos,
  clientes,
  loadMotos,
  loadClientes,
  refreshMotos: () => loadMotos(true),
  refreshClientes: () => loadClientes(true)
})
