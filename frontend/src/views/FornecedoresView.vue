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
          <p><strong>🏷️ Especialidade:</strong> <span class="badge-especialidade">{{ fornecedor.especialidade }}</span>
          </p>
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
          <div class="form-section">
            <h3 class="form-section-title">Dados da Empresa</h3>
            <div class="form-group">
              <label>Nome Social *</label>
              <input v-model="form.nome" type="text" required placeholder="Fornecedor">
            </div>
            <div class="form-group">
              <label>Email *</label>
              <input v-model="form.email" type="email" required placeholder="email@exemplo.com">
            </div>
            <div class="form-group">
              <label>Especialidade *</label>
              <input v-model="form.especialidade" type="text" required placeholder="Ex: Peças, Pneus, Serviços">
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>CNPJ</label>
                <input v-model="form.cnpj" type="cnpj" placeholder="00.000.000/0000-00"
              </div>
              <div class="form-group">
                <label>Telefone *</label>
                <input v-model="form.telefone" type="tel" placeholder="(00) 00000-0000" required maxlength="15"
                  @input="formatTelefone">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group" style="flex:2; min-width:120px;">
                <label>CEP *</label>
                <input v-model="form.cep" type="CEP" placeholder="CEP" maxlength="9"
                  @blur="buscarEnderecoPorCep">
                <div v-if="cepErro" class="cep-erro">{{ cepErro }}</div>
              </div>
              <div class="form-group" style="flex:1; min-width:80px;">
                <label>Estado</label>
                <input v-model="form.estado" type="text" placeholder="Estado" :disabled="true">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Rua</label>
                <input v-model="form.rua" type="text" placeholder="Rua" :disabled="true">
              </div>
              <div class="form-group">
                <label>Número *</label>
                <input v-model="form.numero" type="text" placeholder="Número" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Bairro</label>
                <input v-model="form.bairro" type="text" placeholder="Bairro" :disabled="true">
              </div>
              <div class="form-group">
                <label>Cidade</label>
                <input v-model="form.cidade" type="text" placeholder="Cidade" :disabled="true">
              </div>
            </div>
          </div>
          <div class="form-section">
            <h3 class="form-section-title">Dados do Representante</h3>
            <div class="form-row">
              <div class="form-group">
                <label>Nome</label>
                <input v-model="form.representante_nome" type="text" placeholder="Representante">
              </div>
              <div class="form-group">
                <label>Telefone</label>
                <input v-model="form.representante_telefone" type="tel" placeholder="(00) 00000-0000" maxlength="15"
                  @input="formatTelefoneRepresentante">
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-save">Salvar</button>
              <button type="button" class="btn-cancel" @click="fecharFormulario">Cancelar</button>
            </div>
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
        // Monta o endereço completo
        const enderecoCompleto = (form.value.rua || '') + (form.value.numero ? ', ' + form.value.numero : '')
        const payload = {
          ...form.value,
          endereco: enderecoCompleto,
        }
        if (fornecedorEditando.value) {
          await api.put(`/subscription/fornecedores/${fornecedorEditando.value.id}/`, payload)
          success('Fornecedor atualizado com sucesso!')
        } else {
          await api.post('/subscription/fornecedores/', payload)
          success('Fornecedor cadastrado com sucesso!')
        }
        fecharFormulario()
        carregarFornecedores()
      } catch (err) {
        // Tenta mostrar erro detalhado do backend
        if (err.response && err.response.data) {
          error('Erro: ' + JSON.stringify(err.response.data))
        } else {
          error('Erro ao salvar fornecedor')
        }
        console.error('Erro ao salvar fornecedor:', err)
      }
    }

    const editarFornecedor = (fornecedor) => {
      fornecedorEditando.value = fornecedor
      // Separar rua e número do campo endereco
      let rua = '', numero = ''
      if (fornecedor.endereco) {
        const partes = fornecedor.endereco.split(',')
        rua = partes[0] ? partes[0].trim() : ''
        numero = partes[1] ? partes[1].trim() : ''
      }
      form.value = {
        ...fornecedor,
        rua,
        numero,
        representante_nome: fornecedor.representante_nome || '',
        representante_telefone: fornecedor.representante_telefone || ''
      }
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

    const formatTelefoneRepresentante = (event) => {
      let value = event.target.value.replace(/\D/g, '')
      if (value.length > 11) value = value.slice(0, 11)
      if (value.length > 10) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
      } else if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3')
      } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2')
      }
      form.value.representante_telefone = value
    }

    const cepErro = ref('')
    const buscarEnderecoPorCep = async () => {
      cepErro.value = ''
      const cep = form.value.cep.replace(/\D/g, '')
      if (cep.length !== 8) return
      try {
        const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
        const data = await res.json()
        if (!data.erro) {
          form.value.rua = data.logradouro || ''
          form.value.bairro = data.bairro || ''
          form.value.cidade = data.localidade || ''
          form.value.estado = data.uf || ''
        } else {
          form.value.rua = ''
          form.value.bairro = ''
          form.value.cidade = ''
          form.value.estado = ''
          cepErro.value = 'CEP não encontrado. Verifique e tente novamente.'
        }
      } catch (e) {
        form.value.rua = ''
        form.value.bairro = ''
        form.value.cidade = ''
        form.value.estado = ''
        cepErro.value = 'Erro ao buscar o CEP. Tente novamente.'
      }
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
      formatarData,
      formatTelefone,
      formatTelefoneRepresentante,
      buscarEnderecoPorCep,
      cepErro
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.2rem;
}

.fornecedor-card {
  background: rgb(250, 250, 250);
  border: 2px solid #0088f7;
  border-radius: 12px;
  padding: 0.5rem;
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

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.3rem;
  transition: transform 0.2s;
}

.btn-edit:hover,
.btn-delete:hover {
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
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(80, 120, 180, 0.18);
  padding: 2.2rem 2.2rem 1.5rem 2.2rem;
  max-width: 480px;
  width: 96vw;
  margin: 2.5rem auto;
  position: relative;
  animation: modalFadeIn 0.25s;
}

@keyframes modalFadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.2rem;
}

.modal-header h2 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #2a4365;
  display: flex;
  align-items: center;
  gap: 0.05rem;
}

.modal-header h2::before {
  content: '🏭';
  font-size: 1.5rem;
  margin-right: 0.3rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
  cursor: pointer;
  transition: color 0.18s;
}
.btn-close:hover {
  color: #f5576c;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-row {
  display: flex;
  gap: 1.2rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.0rem;
}

.form-group label {
  font-size: 0.97rem;
  color: #4facfe;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 1rem;
  transition: border 0.18s;
  background: #f9fbfd;
}
.form-group input:focus,
.form-group textarea:focus {
  border-color: #4facfe;
  outline: none;
}

.form-section {
  margin-bottom: 0rem;
  padding-bottom: 0.01rem;
  border-bottom: 1.5px solid #e3e8ee;
}
.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0.5rem;
}
.form-section-title {
  font-size: 1.08rem;
  color: #4facfe;
  font-weight: 700;
  margin-bottom: 0.5rem;
  margin-top: 0.2rem;
  letter-spacing: 0.01em;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-save {
  background: linear-gradient(90deg, #4facfe 60%, #00f2fe 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 0.7rem 1.5rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(79, 172, 254, 0.10);
  transition: background 0.18s, box-shadow 0.18s;
}
.btn-save:hover {
  background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
  box-shadow: 0 4px 16px rgba(79, 172, 254, 0.13);
}

.btn-cancel {
  background: #f5576c;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 0.7rem 1.5rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(245, 87, 108, 0.10);
  transition: background 0.18s, box-shadow 0.18s;
}
.btn-cancel:hover {
  background: #d90429;
  box-shadow: 0 4px 16px rgba(245, 87, 108, 0.13);
}

.form-section:last-child .form-row {
  display: flex;
  gap: 0.7rem;
  flex-wrap: nowrap;
}
.form-section:last-child .form-row .form-group {
  flex: 1 1 0;
  min-width: 120px;
  max-width: 100%;
}
@media (max-width: 600px) {
  .modal-content {
    padding: 1.1rem 0.5rem 1rem 0.5rem;
    max-width: 99vw;
  }
  .form-row {
    flex-direction: column;
    gap: 0.7rem;
  }
  .form-section:last-child .form-row {
    flex-direction: column;
    gap: 0.5rem;
  }
  .form-section:last-child .form-group {
    max-width: 100%;
  }
}
</style>

.cep-erro {
  color: #d32f2f;
  font-size: 0.95em;
  margin-top: 2px;
  margin-bottom: 2px;
}
