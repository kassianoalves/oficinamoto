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
        
        <!-- Dados do Cliente -->
        <div class="form-section">
          <h4>Dados Pessoais</h4>
          <div class="form-grid">
            <input v-model="form.nome" type="text" placeholder="Nome completo" required minlength="3">
            <input 
              v-model="form.cpf" 
              type="CPF" 
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
        </div>

        <!-- Dados das Motos -->
        <div class="form-section">
          <div class="section-header">
            <h4>Motos do Cliente</h4>
            <button type="button" @click="adicionarMoto" class="btn-add-moto">+ Adicionar Moto</button>
          </div>

          <div v-if="form.motos.length" class="motos-form-list">
            <div v-for="(moto, index) in form.motos" :key="index" class="moto-form-item">
              <div class="moto-form-grid">
                <input v-model="moto.marca" type="text" placeholder="Marca (ex: Honda)" required>
                <input v-model="moto.modelo" type="text" placeholder="Modelo (ex: CB 500)" required>
                <input v-model="moto.placa" type="text" placeholder="Placa (ex: ABC-1234)" required>                <input v-model="moto.numero_serie" type="text" placeholder="Número de Série" required>                <input v-model="moto.ano" type="number" placeholder="Ano" min="1950" :max="new Date().getFullYear()" required>
                <input v-model="moto.cor" type="text" placeholder="Cor" required>
                <input v-model="moto.cilindrada" type="number" placeholder="Cilindrada (cc)" min="0">
                <textarea v-model="moto.observacoes" placeholder="Observações" rows="2"></textarea>
              </div>
              <button type="button" @click="removerMoto(index)" class="btn-remove-moto">Remover</button>
            </div>
          </div>
          <p v-else class="no-motos">Nenhuma moto adicionada ainda</p>
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
          <button @click="verHistorico(cliente)" class="btn btn-history">📋 Histórico</button>
          <button @click="editarCliente(cliente)" class="btn btn-edit">✏️ Editar</button>
          <button @click="deletarCliente(cliente.id)" class="btn btn-delete">🗑️ Deletar</button>
        </div>
      </div>
    </div>

    <!-- Modal de Histórico -->
    <div v-if="showHistorico" class="modal-overlay" @click="closeHistorico">
      <div class="modal-historico" @click.stop>
        <div class="modal-header">
          <h3>📋 Histórico de {{ clienteSelecionado?.nome }}</h3>
          <button class="close-btn" @click="closeHistorico">✕</button>
        </div>
        <div class="modal-body">
          <div class="historico-section">
            <h4>🏍️ Motos Cadastradas ({{ motosCliente.length }})</h4>
            <div v-if="motosCliente.length" class="motos-list">
              <div v-for="moto in motosCliente" :key="moto.id" class="moto-item">
                <p><strong>{{ moto.marca }} {{ moto.modelo }}</strong></p>
                <p class="moto-details">{{ moto.placa }} - {{ moto.ano }}</p>
              </div>
            </div>
            <p v-else class="empty-msg">Nenhuma moto cadastrada</p>
          </div>

          <div class="historico-section">
            <h4>🔧 Manutenções Concluídas ({{ manutencoesCliente.length }})</h4>
            <div v-if="manutencoesCliente.length" class="manutencoes-list">
              <div v-for="manutencao in manutencoesCliente" :key="manutencao.id" class="manutencao-item">
                <div class="manutencao-header">
                  <strong>{{ getMotoDados(manutencao.moto) }}</strong>
                  <span class="data-badge">{{ formatDate(manutencao.data_agendada) }}</span>
                </div>
                <p><strong>Serviço:</strong> {{ getTipoServico(manutencao.tipo_servico) }}</p>
                <p v-if="manutencao.observacoes" class="observacoes">{{ manutencao.observacoes }}</p>
              </div>
            </div>
            <p v-else class="empty-msg">Nenhuma manutenção concluída</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeHistorico" class="btn btn-secondary">Fechar</button>
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
    const showHistorico = ref(false)
    const clienteSelecionado = ref(null)
    const motosCliente = ref([])
    const manutencoesCliente = ref([])
    const form = ref({
      nome: '',
      cpf: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: '',
      motos: []
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

    const validarPlaca = (placa) => {
      // Formato antigo: ABC1234
      // Formato Mercosul: ABC1D23
      const placaLimpa = placa.toUpperCase().replace('-', '').replace(' ', '')
      const regexAntiga = /^[A-Z]{3}\d{4}$/
      const regexMercosul = /^[A-Z]{3}\d[A-Z0-9]\d{2}$/
      return regexAntiga.test(placaLimpa) || regexMercosul.test(placaLimpa)
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
        // Validar motos antes de salvar
        if (form.value.motos.length > 0) {
          for (const moto of form.value.motos) {
            if (!moto.marca || !moto.modelo || !moto.placa || !moto.numero_serie || !moto.ano || !moto.cor) {
              error('Todos os campos das motos são obrigatórios!')
              return
            }
            if (!validarPlaca(moto.placa)) {
              error(`Placa inválida: "${moto.placa}". Use formato ABC-1234 ou ABC1D23`)
              return
            }
          }
        }

        const clienteData = {
          nome: form.value.nome,
          cpf: form.value.cpf,
          email: form.value.email,
          telefone: form.value.telefone,
          endereco: form.value.endereco,
          cidade: form.value.cidade
        }

        let clienteId = editingId.value
        
        if (editingId.value) {
          await api.put(`/clientes/${editingId.value}/`, clienteData)
          success('Cliente atualizado com sucesso!')
        } else {
          const res = await api.post('/clientes/', clienteData)
          clienteId = res.data.id
          success('Cliente cadastrado com sucesso!')
        }

        // Salvar motos do cliente
        if (form.value.motos.length > 0) {
          for (const moto of form.value.motos) {
            try {
              // Se a moto não tem ID, é uma nova moto
              if (!moto.id) {
                console.log('Salvando nova moto:', moto)
                await api.post('/motos/', {
                  ...moto,
                  cliente: clienteId
                })
              } else {
                // Se tem ID, atualizar moto existente
                console.log('Atualizando moto:', moto)
                await api.put(`/motos/${moto.id}/`, {
                  ...moto,
                  cliente: clienteId
                })
              }
            } catch (motoErr) {
              console.error('Erro ao salvar moto:', motoErr)
              console.error('Dados da moto:', moto)
              console.error('Cliente ID:', clienteId)
              throw motoErr
            }
          }
          success('Motos do cliente salvas com sucesso!')
        }

        resetForm()
        carregarClientes()
      } catch (err) {
        console.error('Erro completo ao salvar cliente:', err)
        console.error('Resposta do erro:', err.response?.data)
        
        // Tentar extrair mensagens de erro específicas
        let errorMsg = 'Erro ao salvar cliente ou moto'
        const errorData = err.response?.data
        
        if (errorData) {
          // Se tem array de erros
          if (errorData.placa && Array.isArray(errorData.placa)) {
            console.error('Erro de placa:', errorData.placa[0])
            errorMsg = `Erro na placa: ${errorData.placa[0]}`
          } else if (errorData.numero_serie && Array.isArray(errorData.numero_serie)) {
            console.error('Erro de número de série:', errorData.numero_serie[0])
            errorMsg = `Erro no número de série: ${errorData.numero_serie[0]}`
          } else if (errorData.cpf && Array.isArray(errorData.cpf)) {
            console.error('Erro de CPF:', errorData.cpf[0])
            errorMsg = `Erro no CPF: ${errorData.cpf[0]}`
          } else if (typeof errorData === 'string') {
            errorMsg = errorData
          } else if (errorData.detail) {
            errorMsg = errorData.detail
          }
        }
        
        error(errorMsg)
      }
    }

    const editarCliente = (cliente) => {
      editingId.value = cliente.id
      form.value = { 
        nome: cliente.nome,
        cpf: cliente.cpf,
        email: cliente.email,
        telefone: cliente.telefone,
        endereco: cliente.endereco,
        cidade: cliente.cidade,
        motos: []
      }
      
      // Carregar motos do cliente
      carregarMotosDoCliente(cliente.id)
      showForm.value = true
    }

    const carregarMotosDoCliente = async (clienteId) => {
      try {
        const res = await api.get('/motos/')
        const todasMotos = res.data.results || res.data || []
        form.value.motos = todasMotos
          .filter(m => m.cliente === clienteId)
          .map(m => ({
            id: m.id,
            marca: m.marca,
            modelo: m.modelo,
            placa: m.placa,
            numero_serie: m.numero_serie,
            ano: m.ano,
            cor: m.cor,
            cilindrada: m.cilindrada,
            observacoes: m.observacoes
          }))
      } catch (err) {
        console.error('Erro ao carregar motos do cliente:', err)
      }
    }

    const adicionarMoto = () => {
      form.value.motos.push({
        id: null,
        marca: '',
        modelo: '',
        placa: '',
        numero_serie: '',
        ano: new Date().getFullYear(),
        cor: '',
        cilindrada: '',
        observacoes: ''
      })
    }

    const removerMoto = (index) => {
      form.value.motos.splice(index, 1)
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
        cidade: '',
        motos: []
      }
      editingId.value = null
      showForm.value = false
    }

    const verHistorico = async (cliente) => {
      clienteSelecionado.value = cliente
      showHistorico.value = true
      
      try {
        // Carregar motos do cliente
        const resMotos = await api.get('/motos/')
        const todasMotos = resMotos.data.results || resMotos.data || []
        motosCliente.value = todasMotos.filter(m => m.cliente === cliente.id)

        // Carregar manutenções concluídas das motos do cliente
        const resAgendamentos = await api.get('/agendamentos/')
        const todosAgendamentos = resAgendamentos.data.results || resAgendamentos.data || []
        const motosIds = motosCliente.value.map(m => m.id)
        manutencoesCliente.value = todosAgendamentos.filter(a => 
          a.status === 'concluido' && motosIds.includes(a.moto)
        )
      } catch (err) {
        console.error('Erro ao carregar histórico:', err)
        error('Erro ao carregar histórico do cliente')
      }
    }

    const closeHistorico = () => {
      showHistorico.value = false
      clienteSelecionado.value = null
      motosCliente.value = []
      manutencoesCliente.value = []
    }

    const getMotoDados = (motoId) => {
      const moto = motosCliente.value.find(m => m.id === motoId)
      return moto ? `${moto.marca} ${moto.modelo} (${moto.placa})` : 'Moto desconhecida'
    }

    const getTipoServico = (tipo) => {
      const tipos = {
        'troca': 'Troca de Óleo',
        'reparo': 'Reparo',
        'assistencia': 'Assistência',
        'vistoria': 'Vistoria',
        'manutencao': 'Manutenção Periódica'
      }
      return tipos[tipo] || tipo
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }

    onMounted(carregarClientes)

    return {
      clientes,
      clientesFiltrados,
      showForm,
      editingId,
      form,
      filtro,
      showHistorico,
      clienteSelecionado,
      motosCliente,
      manutencoesCliente,
      manutencoesCliente,
      salvarCliente,
      editarCliente,
      deletarCliente,
      resetForm,
      verHistorico,
      closeHistorico,
      getMotoDados,
      getTipoServico,
      formatDate,
      formatCPF,
      formatTelefone,
      validarPlaca,
      adicionarMoto,
      removerMoto,
      carregarMotosDoCliente
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

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.form-section h4 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  margin: 0;
}

.btn-add-moto {
  padding: 0.6rem 1rem;
  background: #4facfe;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-add-moto:hover {
  background: #0080ff;
}

.motos-form-list {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.moto-form-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #4facfe;
}

.moto-form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.moto-form-grid input,
.moto-form-grid textarea {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.moto-form-grid input:focus,
.moto-form-grid textarea:focus {
  outline: none;
  border-color: #4facfe;
  box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
}

.btn-remove-moto {
  padding: 0.6rem 1rem;
  background: #f5576c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-remove-moto:hover {
  background: #e63946;
}

.no-motos {
  color: #999;
  text-align: center;
  padding: 1rem;
  font-style: italic;
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

.btn-history {
  background: #00d084;
  color: white;
  flex: 1;
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

.btn-history:hover,
.btn-edit:hover,
.btn-delete:hover {
  opacity: 0.9;
}

/* Modal Histórico */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-historico {
  background: white;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #667eea;
  font-size: 1.4rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.historico-section {
  margin-bottom: 2rem;
}

.historico-section h4 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.motos-list {
  display: grid;
  gap: 0.75rem;
}

.moto-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.moto-item p {
  margin: 0.25rem 0;
  color: #333;
}

.moto-details {
  color: #666;
  font-size: 0.9rem;
}

.manutencoes-list {
  display: grid;
  gap: 1rem;
}

.manutencao-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #00d084;
}

.manutencao-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.data-badge {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.manutencao-item p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.observacoes {
  font-style: italic;
  color: #999;
}

.empty-msg {
  text-align: center;
  color: #999;
  padding: 2rem;
  font-style: italic;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 2px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
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
