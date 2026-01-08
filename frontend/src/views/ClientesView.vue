<template>
  <div class="clientes-view">
    <div class="view-header">
      <h2>Clientes</h2>
      <button @click="showForm = !showForm" class="btn-add">➕ Novo Cliente</button>
    </div>

    <!-- Formulário de Adição -->
    <div v-if="showForm" class="form-container">
      <form @submit.prevent="salvarCliente">
        <h3>{{ editingId ? 'Editar Cliente' : 'Novo Cliente' }}</h3>
        <div class="form-grid">
          <input v-model="form.nome" type="text" placeholder="Nome completo" required>
          <input v-model="form.cpf" type="text" placeholder="CPF" required>
          <input v-model="form.email" type="email" placeholder="Email">
          <input v-model="form.telefone" type="tel" placeholder="Telefone" required>
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
    <div v-if="clientes.length" class="clientes-list">
      <div v-for="cliente in clientes" :key="cliente.id" class="cliente-card">
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
import { ref, onMounted } from 'vue'
import api from '@/api.js'

export default {
  name: 'ClientesView',
  setup() {
    const clientes = ref([])
    const showForm = ref(false)
    const editingId = ref(null)
    const form = ref({
      nome: '',
      cpf: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: ''
    })

    const carregarClientes = async () => {
      try {
        console.log('Carregando clientes...')
        const res = await api.get('/clientes/')
        console.log('Resposta recebida:', res.data)
        clientes.value = res.data.results || res.data || []
        console.log('Clientes carregados:', clientes.value)
      } catch (error) {
        console.error('Erro ao carregar clientes:', error.message)
        console.error('Erro completo:', error)
        alert('Erro ao carregar clientes: ' + error.message)
      }
    }

    const salvarCliente = async () => {
      try {
        console.log('Salvando cliente:', form.value)
        if (editingId.value) {
          const res = await api.put(`/clientes/${editingId.value}/`, form.value)
          console.log('Cliente atualizado:', res.data)
          alert('Cliente atualizado com sucesso!')
        } else {
          const res = await api.post('/clientes/', form.value)
          console.log('Cliente criado:', res.data)
          alert('Cliente salvo com sucesso!')
        }
        resetForm()
        carregarClientes()
      } catch (error) {
        console.error('Erro ao salvar cliente:', error.message)
        console.error('Status:', error.response?.status)
        console.error('Dados:', error.response?.data)
        const errorMsg = error.response?.data?.detail || error.response?.data?.non_field_errors?.[0] || error.message || 'Erro ao salvar cliente'
        alert('Erro: ' + errorMsg)
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
          carregarClientes()
        } catch (error) {
          console.error('Erro ao deletar cliente:', error)
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
      showForm,
      editingId,
      form,
      salvarCliente,
      editarCliente,
      deletarCliente,
      resetForm
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
}

.view-header h2 {
  font-size: 1.8rem;
  color: #333;
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
