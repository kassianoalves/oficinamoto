<template>
  <div class="clientes-view">
    <div class="view-header">
      <h2>Clientes ({{ clientesFiltrados.length }})</h2>
      <div class="header-actions">
        <input 
          v-model="filtro" 
          type="text" 
          placeholder="🔍 Buscar por nome, CPF ou telefone..." 
          class="search-input"
        >
        <button @click="showForm = !showForm" class="btn-add">➕ Novo Cliente</button>
      </div>
    </div>

    <!-- Formulário de Adição -->
    <div v-if="showForm" class="form-container">
      <form @submit.prevent="salvarCliente">
        <h3>{{ editingId ? 'Editar Cliente' : 'Novo Cliente' }}</h3>
        <div class="form-grid">
          <input v-model="form.nome" type="text" placeholder="Nome completo" required minlength="3">
          <input 
            v-model="form.cpf" 
            type="text" 
            placeholder="CPF (000.000.000-00)" 
            required 
            maxlength="14"
            @input="formatCPF"
          >
          <input v-model="form.email" type="email" placeholder="Email" pattern="[^@]+@[^@]+\.[a-zA-Z]{2,}">
          <input 
            v-model="form.telefone" 
            type="tel" 
            placeholder="Telefone (00) 00000-0000" 
            required
            maxlength="15"
            @input="formatTelefone"
          >
          <input v-model="form.endereco" type="text" placeholder="Endereço" required>
          <input v-model="form.cidade" type="text" placeholder="Cidade" required>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ editingId ? 'Atualizar' : 'Salvar' }}</button>
          <button type="button" @click="resetForm" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </div>

    <!-- Lista de Clientes -->
    <div v-if="clientesFiltrados.length" class="clientes-list">
      <div v-for="cliente in clientesFiltrados" :key="cliente.id" class="cliente-card">
        <div class="cliente-info">
          <h4>{{ cliente.nome }}</h4>
          <p><strong>CPF:</strong> {{ cliente.cpf }}</p>
          <p><strong>Telefone:</strong> {{ cliente.telefone }}</p>
          <p><strong>Email:</strong> {{ cliente.email }}</p>
          <p><strong>Endereço:</strong> {{ cliente.endereco }}, {{ cliente.cidade }}</p>
        </div>
        <div class="cliente-actions">
          <button @click="editarCliente(cliente)" class="btn btn-edit">✏️ Editar</button>
          <button @click="deletarCliente(cliente.id)" class="btn btn-delete">🗑️ Deletar</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhum cliente cadastrado. Clique em "Novo Cliente" para começar.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'

export default {
  name: 'ClientesView',
  setup() {
    const { success, error } = useToast()
    const clientes = ref([])
    const showForm = ref(false)
    const editingId = ref(null)
    const filtro = ref('')
    const form = ref({
      nome: '',
      cpf: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: ''
    })

    const clientesFiltrados = computed(() => {
      if (!filtro.value) return clientes.value
      const termo = filtro.value.toLowerCase()
      return clientes.value.filter(c => 
        c.nome.toLowerCase().includes(termo) ||
        c.cpf.replace(/\D/g, '').includes(termo.replace(/\D/g, '')) ||
        c.telefone.replace(/\D/g, '').includes(termo.replace(/\D/g, ''))
      )
    })

    const formatCPF = (event) => {
      let value = event.target.value.replace(/\D/g, '')
      if (value.length > 11) value = value.slice(0, 11)
      if (value.length > 9) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
      } else if (value.length > 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3')
      } else if (value.length > 3) {
        value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2')
      }
      form.value.cpf = value
    }

    const formatTelefone = (event) => {
      let value = event.target.value.replace(/\D/g, '')
      if (value.length > 11) value = value.slice(0, 11)
      if (value.length > 10) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
      } else if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3')
      } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2')
      }
      form.value.telefone = value
    }

    const carregarClientes = async () => {
      try {
        const res = await api.get('/clientes/')
        clientes.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar clientes:', err)
        error('Erro ao carregar clientes. Verifique sua conexão.')
      }
    }

    const salvarCliente = async () => {
      try {
        if (editingId.value) {
          await api.put(`/clientes/${editingId.value}/`, form.value)
          success('Cliente atualizado com sucesso!')
        } else {
          await api.post('/clientes/', form.value)
          success('Cliente cadastrado com sucesso!')
        }
        resetForm()
        carregarClientes()
      } catch (err) {
        console.error('Erro ao salvar cliente:', err)
        const errorMsg = err.response?.data?.cpf?.[0] || 
                        err.response?.data?.detail || 
                        'Erro ao salvar cliente'
        error(errorMsg)
      }
    }

    const editarCliente = (cliente) => {
      editingId.value = cliente.id
      form.value = { ...cliente }
      showForm.value = true
    }

    const deletarCliente = async (id) => {
      if (confirm('Deseja deletar este cliente?')) {
        try {
          await api.delete(`/clientes/${id}/`)
          success('Cliente deletado com sucesso!')
          carregarClientes()
        } catch (err) {
          console.error('Erro ao deletar cliente:', err)
          error('Erro ao deletar cliente. Verifique as permissões.')
        }
      }
    }

    const resetForm = () => {
      form.value = {
        nome: '',
        cpf: '',
        email: '',
        telefone: '',
        endereco: '',
        cidade: ''
      }
      editingId.value = null
      showForm.value = false
    }

    onMounted(carregarClientes)

    return {
      clientes,
      clientesFiltrados,
      showForm,
      editingId,
      form,
      filtro,
      salvarCliente,
      editarCliente,
      deletarCliente,
      resetForm,
      formatCPF,
      formatTelefone
    }
  }
}
</script>

<style scoped>
.clientes-view {
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

.form-grid input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-grid input:focus {
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

.clientes-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.cliente-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.cliente-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.cliente-info h4 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.cliente-info p {
  color: #666;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.cliente-actions {
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
  .clientes-list {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
