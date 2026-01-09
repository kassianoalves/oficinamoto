<template>
  <div class="motos-view">
    <div class="view-header">
      <h2>Motos Cadastradas ({{ motosFiltradas.length }})</h2>
      <div class="header-actions">
        <input 
          v-model="filtro" 
          type="text" 
          placeholder="🔍 Buscar por marca, modelo ou placa..." 
          class="search-input"
        >
        <button @click="showForm = !showForm" class="btn-add">➕ Registrar Moto</button>
      </div>
    </div>

    <!-- Formulário de Adição -->
    <div v-if="showForm" class="form-container">
      <form @submit.prevent="salvarMoto">
        <h3>{{ editingId ? 'Editar Moto' : 'Registrar Nova Moto' }}</h3>
        <div class="form-grid">
          <select v-model="form.cliente" required>
            <option value="">Selecione o Cliente</option>
            <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
              {{ cliente.nome }}
            </option>
          </select>
          <input v-model="form.marca" type="text" placeholder="Marca" required minlength="2">
          <input v-model="form.modelo" type="text" placeholder="Modelo" required minlength="2">
          <input 
            v-model.number="form.ano" 
            type="number" 
            placeholder="Ano" 
            required
            :min="1900"
            :max="new Date().getFullYear() + 1"
          >
          <input v-model="form.cor" type="text" placeholder="Cor">
          <input 
            v-model="form.placa" 
            type="text" 
            placeholder="Placa (ABC-1234)" 
            required
            maxlength="8"
            @input="formatPlaca"
          >
          <input v-model="form.numero_serie" type="text" placeholder="Número de Série" required>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ editingId ? 'Atualizar' : 'Salvar' }}</button>
          <button type="button" @click="resetForm" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </div>

    <!-- Lista de Motos -->
    <div v-if="motosFiltradas.length" class="motos-list">
      <div v-for="moto in motosFiltradas" :key="moto.id" class="moto-card">
        <div class="moto-info">
          <h4>{{ moto.marca }} {{ moto.modelo }} ({{ moto.ano }})</h4>
          <p><strong>Placa:</strong> {{ moto.placa }}</p>
          <p><strong>Cor:</strong> {{ moto.cor }}</p>
          <p><strong>Série:</strong> {{ moto.numero_serie }}</p>
          <p><strong>Cliente:</strong> {{ getClienteName(moto.cliente) }}</p>
        </div>
        <div class="moto-actions">
          <button @click="editarMoto(moto)" class="btn btn-edit">✏️ Editar</button>
          <button @click="deletarMoto(moto.id)" class="btn btn-delete">🗑️ Deletar</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhuma moto cadastrada. Clique em "Registrar Moto" para começar.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'

export default {
  name: 'MotosView',
  setup() {
    const { success, error } = useToast()
    const motos = ref([])
    const clientes = ref([])
    const showForm = ref(false)
    const editingId = ref(null)
    const filtro = ref('')
    const form = ref({
      cliente: '',
      marca: '',
      modelo: '',
      ano: new Date().getFullYear(),
      cor: '',
      placa: '',
      numero_serie: ''
    })

    const motosFiltradas = computed(() => {
      if (!filtro.value) return motos.value
      const termo = filtro.value.toLowerCase()
      return motos.value.filter(m => 
        m.marca.toLowerCase().includes(termo) ||
        m.modelo.toLowerCase().includes(termo) ||
        m.placa.toLowerCase().includes(termo)
      )
    })

    const formatPlaca = (event) => {
      let value = event.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '')
      if (value.length > 7) value = value.slice(0, 7)
      if (value.length > 3) {
        value = value.replace(/(\w{3})(\w{0,4})/, '$1-$2')
      }
      form.value.placa = value
    }

    const carregarMotos = async () => {
      try {
        const res = await api.get('/motos/')
        motos.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar motos:', err)
        error('Erro ao carregar motos')
      }
    }

    const carregarClientes = async () => {
      try {
        const res = await api.get('/clientes/')
        clientes.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar clientes:', err)
        error('Erro ao carregar lista de clientes')
      }
    }

    const getClienteName = (clienteId) => {
      const cliente = clientes.value.find(c => c.id === clienteId)
      return cliente ? cliente.nome : 'Desconhecido'
    }

    const salvarMoto = async () => {
      try {
        if (editingId.value) {
          await api.put(`/motos/${editingId.value}/`, form.value)
          success('Moto atualizada com sucesso!')
        } else {
          await api.post('/motos/', form.value)
          success('Moto registrada com sucesso!')
        }
        resetForm()
        carregarMotos()
      } catch (err) {
        console.error('Erro ao salvar moto:', err)
        const errorMsg = err.response?.data?.placa?.[0] ||
                        err.response?.data?.detail || 
                        'Erro ao salvar moto'
        error(errorMsg)
      }
    }

    const editarMoto = (moto) => {
      editingId.value = moto.id
      form.value = { ...moto }
      showForm.value = true
    }

    const deletarMoto = async (id) => {
      if (confirm('Deseja deletar esta moto?')) {
        try {
          await api.delete(`/motos/${id}/`)
          success('Moto deletada com sucesso!')
          carregarMotos()
        } catch (err) {
          console.error('Erro ao deletar moto:', err)
          error('Erro ao deletar moto. Verifique as permissões.')
        }
      }
    }

    const resetForm = () => {
      form.value = {
        cliente: '',
        marca: '',
        modelo: '',
        ano: new Date().getFullYear(),
        cor: '',
        placa: '',
        numero_serie: ''
      }
      editingId.value = null
      showForm.value = false
    }

    onMounted(() => {
      carregarClientes()
      carregarMotos()
    })

    return {
      motos,
      motosFiltradas,
      clientes,
      showForm,
      editingId,
      form,
      filtro,
      salvarMoto,
      editarMoto,
      deletarMoto,
      resetForm,
      getClienteName,
      formatPlaca
    }
  }
}
</script>

<style scoped>
.motos-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.view-header h2 {
  font-size: 1.8rem;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 0.8rem 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 300px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-add {
  padding: 0.8rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-add:hover {
  transform: scale(1.05);
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-container h3 {
  margin-bottom: 1.5rem;
  color: #333;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-grid input,
.form-grid select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-grid input:focus,
.form-grid select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.motos-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.moto-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.moto-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.moto-info h4 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.moto-info p {
  color: #666;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.moto-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-edit {
  background: #4facfe;
  color: white;
  flex: 1;
}

.btn-delete {
  background: #f5576c;
  color: white;
  flex: 1;
}

.btn-edit:hover,
.btn-delete:hover {
  opacity: 0.9;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .motos-list {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
