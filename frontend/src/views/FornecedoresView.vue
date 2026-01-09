<template>
  <div class="fornecedores-view">
    <div class="header">
      <h1>🏭 Gerenciamento de Fornecedores</h1>
      <p class="subtitle">Gerencie seus fornecedores e parceiros comerciais</p>
      <span class="badge-pro">⭐ Recurso Especial</span>
    </div>

    <div class="actions">
      <button @click="mostrarFormulario = true" class="btn-add">
        ➕ Novo Fornecedor
      </button>
    </div>

    <!-- Lista de Fornecedores -->
    <div class="fornecedores-grid" v-if="fornecedores.length">
      <div v-for="fornecedor in fornecedores" :key="fornecedor.id" class="fornecedor-card">
        <div class="card-header">
          <h3>{{ fornecedor.nome }}</h3>
          <div class="card-actions">
            <button @click="editarFornecedor(fornecedor)" class="btn-edit">✏️</button>
            <button @click="deletarFornecedor(fornecedor.id)" class="btn-delete">🗑️</button>
          </div>
        </div>
        <div class="card-body">
          <p><strong>📧 Email:</strong> {{ fornecedor.email }}</p>
          <p><strong>📱 Telefone:</strong> {{ fornecedor.telefone }}</p>
          <p v-if="fornecedor.cnpj"><strong>📄 CNPJ:</strong> {{ fornecedor.cnpj }}</p>
          <p><strong>📍 Cidade:</strong> {{ fornecedor.cidade }}</p>
          <p><strong>🏷️ Especialidade:</strong> <span class="badge-especialidade">{{ fornecedor.especialidade }}</span></p>
          <p><strong>📅 Cadastrado:</strong> {{ formatarData(fornecedor.data_criacao) }}</p>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhum fornecedor cadastrado</p>
    </div>

    <!-- Modal Formulário -->
    <div v-if="mostrarFormulario" class="modal-overlay" @click="fecharFormulario">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ fornecedorEditando ? 'Editar Fornecedor' : 'Novo Fornecedor' }}</h2>
          <button @click="fecharFormulario" class="btn-close">✕</button>
        </div>
        <form @submit.prevent="salvarFornecedor" class="form">
          <div class="form-group">
            <label>Nome *</label>
            <input v-model="form.nome" type="text" required placeholder="Nome do fornecedor">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Email *</label>
              <input v-model="form.email" type="email" required placeholder="email@exemplo.com">
            </div>
            <div class="form-group">
              <label>Telefone *</label>
              <input v-model="form.telefone" type="text" required placeholder="(00) 00000-0000">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>CNPJ</label>
              <input v-model="form.cnpj" type="text" placeholder="00.000.000/0000-00">
            </div>
            <div class="form-group">
              <label>Cidade *</label>
              <input v-model="form.cidade" type="text" required placeholder="Nome da cidade">
            </div>
          </div>
          <div class="form-group">
            <label>Especialidade *</label>
            <input v-model="form.especialidade" type="text" required placeholder="Ex: Óleo, Pneus, Peças">
          </div>
          <div class="form-group">
            <label>Endereço *</label>
            <textarea v-model="form.endereco" required placeholder="Endereço completo" rows="3"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" @click="fecharFormulario" class="btn-cancel">Cancelar</button>
            <button type="submit" class="btn-save">{{ fornecedorEditando ? 'Atualizar' : 'Salvar' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'

export default {
  name: 'FornecedoresView',
  setup() {
    const { success, error } = useToast()
    const fornecedores = ref([])
    const mostrarFormulario = ref(false)
    const fornecedorEditando = ref(null)
    const form = ref({
      nome: '',
      email: '',
      telefone: '',
      cnpj: '',
      endereco: '',
      cidade: '',
      especialidade: ''
    })

    const carregarFornecedores = async () => {
      try {
        const res = await api.get('/subscription/fornecedores/')
        fornecedores.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar fornecedores:', err)
        error('Erro ao carregar fornecedores')
      }
    }

    const salvarFornecedor = async () => {
      try {
        if (fornecedorEditando.value) {
          await api.put(`/subscription/fornecedores/${fornecedorEditando.value.id}/`, form.value)
          success('Fornecedor atualizado com sucesso!')
        } else {
          await api.post('/subscription/fornecedores/', form.value)
          success('Fornecedor cadastrado com sucesso!')
        }
        fecharFormulario()
        carregarFornecedores()
      } catch (err) {
        console.error('Erro ao salvar fornecedor:', err)
        error('Erro ao salvar fornecedor')
      }
    }

    const editarFornecedor = (fornecedor) => {
      fornecedorEditando.value = fornecedor
      form.value = { ...fornecedor }
      mostrarFormulario.value = true
    }

    const deletarFornecedor = async (id) => {
      if (!confirm('Tem certeza que deseja deletar este fornecedor?')) return
      
      try {
        await api.delete(`/subscription/fornecedores/${id}/`)
        success('Fornecedor deletado com sucesso!')
        carregarFornecedores()
      } catch (err) {
        console.error('Erro ao deletar fornecedor:', err)
        error('Erro ao deletar fornecedor')
      }
    }

    const fecharFormulario = () => {
      mostrarFormulario.value = false
      fornecedorEditando.value = null
      form.value = {
        nome: '',
        email: '',
        telefone: '',
        cnpj: '',
        endereco: '',
        cidade: '',
        especialidade: ''
      }
    }

    const formatarData = (data) => {
      return new Date(data).toLocaleDateString('pt-BR')
    }

    onMounted(() => {
      carregarFornecedores()
    })

    return {
      fornecedores,
      mostrarFormulario,
      fornecedorEditando,
      form,
      salvarFornecedor,
      editarFornecedor,
      deletarFornecedor,
      fecharFormulario,
      formatarData
    }
  }
}
</script>

<style scoped>
.fornecedores-view {
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.badge-pro {
  display: inline-block;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 2rem;
}

.btn-add {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-add:hover {
  transform: translateY(-2px);
}

.fornecedores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.fornecedor-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.fornecedor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.card-header h3 {
  color: #333;
  font-size: 1.3rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.3rem;
  transition: transform 0.2s;
}

.btn-edit:hover, .btn-delete:hover {
  transform: scale(1.2);
}

.card-body p {
  margin: 0.6rem 0;
  color: #555;
  font-size: 0.95rem;
}

.badge-especialidade {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  color: #333;
  font-size: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-save:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .fornecedores-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
