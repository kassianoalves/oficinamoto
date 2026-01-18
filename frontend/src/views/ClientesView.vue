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
            type="cpf" 
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

        <div v-if="!editingId" class="moto-extra">
          <div class="moto-extra-header">
            <h4>🏍️ Cadastro Moto</h4>
            <span class="hint">Preencha para cadastrar a moto junto com o cliente.</span>
          </div>
          <div class="form-grid moto-grid">
            <input v-model="motoForm.marca" type="text" placeholder="Marca">
            <input v-model="motoForm.modelo" type="text" placeholder="Modelo">
            <input v-model.number="motoForm.ano" type="number" placeholder="Ano" min="1900" max="2099">
            <input v-model="motoForm.cor" type="text" placeholder="Cor">
            <input v-model="motoForm.placa" type="text" placeholder="Placa (ABC1D23)" maxlength="8">
            <input v-model="motoForm.numero_serie" type="text" placeholder="Número de série">
          </div>
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
          <div class="info-group">
            <p><strong>CPF:</strong> {{ cliente.cpf }}</p>
            <p><strong>Telefone:</strong> {{ cliente.telefone }}</p>
            <p><strong>Email:</strong> {{ cliente.email }}</p>
            <p><strong>Endereço:</strong> {{ cliente.endereco }}, {{ cliente.cidade }}</p>
          </div>
        </div>
        <div class="cliente-actions">
          <button @click="verHistorico(cliente)" class="btn btn-history" title="Ver histórico">📋Histórico</button>
          <button @click="editarCliente(cliente)" class="btn btn-edit" title="Editar">✏️Editar</button>
          <button @click="deletarCliente(cliente.id)" class="btn btn-delete" title="Deletar">🗑️Deletar</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhum cliente cadastrado. Clique em "Novo Cliente" para começar.</p>
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

          <div class="historico-section">
            <h4>📦 Peças Usadas ({{ pecasUsadas.length }})</h4>
            <div v-if="pecasUsadas.length" class="pecas-list">
              <div v-for="item in pecasUsadas" :key="item.id" class="peca-item">
                <div class="peca-header">
                  <strong>{{ item.peca_nome }}</strong>
                  <span class="data-badge">{{ formatDate(item.data_adicao) }}</span>
                </div>
                <p><strong>Quantidade:</strong> {{ item.quantidade_usada }} un.</p>
                <p><strong>Preço Unitário:</strong> R$ {{ formatarMoeda(item.preco_unitario) }}</p>
                <p><strong>Subtotal:</strong> R$ {{ formatarMoeda(item.subtotal) }}</p>
              </div>
            </div>
            <p v-else class="empty-msg">Nenhuma peça registrada</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeHistorico" class="btn btn-secondary">Fechar</button>
        </div>
      </div>
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
    const pecasUsadas = ref([])
    const form = ref({
      nome: '',
      cpf: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: ''
    })
    const motoForm = ref({
      marca: '',
      modelo: '',
      ano: '',
      cor: '',
      placa: '',
      numero_serie: ''
    })

    const motoPreenchida = computed(() =>
      Object.values(motoForm.value).some(v => `${v ?? ''}`.trim() !== '')
    )

    const motoCompleta = computed(() =>
      ['marca', 'modelo', 'ano', 'cor', 'placa', 'numero_serie']
        .every(campo => `${motoForm.value[campo] ?? ''}`.trim() !== '')
    )

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
          if (motoPreenchida.value && !motoCompleta.value) {
            error('Preencha todos os campos da moto ou deixe-os em branco.')
            return
          }

          const clienteRes = await api.post('/clientes/', form.value)
          success('Cliente cadastrado com sucesso!')

          if (motoPreenchida.value) {
            const payloadMoto = {
              ...motoForm.value,
              cliente: clienteRes.data.id,
              ano: Number(motoForm.value.ano)
            }
            await api.post('/motos/', payloadMoto)
            success('Moto cadastrada junto com o cliente!')
          }
        }
        resetForm()
        carregarClientes()
      } catch (err) {
        console.error('Erro ao salvar cliente:', err)
        const errorMsg = err.response?.data?.placa?.[0] ||
                        err.response?.data?.numero_serie?.[0] ||
                        err.response?.data?.cpf?.[0] ||
                        err.response?.data?.detail ||
                        'Erro ao salvar cliente'
        error(errorMsg)
      }
    }

    const editarCliente = (cliente) => {
      editingId.value = cliente.id
      form.value = { ...cliente }
      showForm.value = true
      motoForm.value = {
        marca: '',
        modelo: '',
        ano: '',
        cor: '',
        placa: '',
        numero_serie: ''
      }
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
      motoForm.value = {
        marca: '',
        modelo: '',
        ano: '',
        cor: '',
        placa: '',
        numero_serie: ''
      }
      editingId.value = null
      showForm.value = false
    }

    const carregarHistoricoCliente = async (clienteId) => {
      try {
        const resMotos = await api.get('/motos/')
        const todasMotos = resMotos.data.results || resMotos.data || []
        motosCliente.value = todasMotos.filter(m => m.cliente === clienteId)

        const resAgendamentos = await api.get('/agendamentos/')
        const todosAgendamentos = resAgendamentos.data.results || resAgendamentos.data || []
        const motosIds = motosCliente.value.map(m => m.id)
        const agendamentosCliente = todosAgendamentos.filter(a =>
          a.status === 'concluido' && motosIds.includes(a.moto)
        )
        manutencoesCliente.value = agendamentosCliente

        const resPecas = await api.get('/itens-agendamento/')
        const todasPecas = resPecas.data.results || resPecas.data || []
        const agendamentosIds = agendamentosCliente.map(a => a.id)
        pecasUsadas.value = todasPecas.filter(p => agendamentosIds.includes(p.agendamento))
      } catch (err) {
        console.error('Erro ao carregar histórico:', err)
        error('Erro ao carregar histórico do cliente')
      }
    }

    const verHistorico = async (cliente) => {
      clienteSelecionado.value = cliente
      showHistorico.value = true
      await carregarHistoricoCliente(cliente.id)
    }

    const closeHistorico = () => {
      showHistorico.value = false
      clienteSelecionado.value = null
      motosCliente.value = []
      manutencoesCliente.value = []
      pecasUsadas.value = []
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

    const formatarMoeda = (valor) => {
      return valor.toFixed(2).replace('.', ',')
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
      pecasUsadas,
      motoForm,
      salvarCliente,
      editarCliente,
      deletarCliente,
      resetForm,
      verHistorico,
      closeHistorico,
      getMotoDados,
      getTipoServico,
      formatDate,
      formatarMoeda,
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
  font-size: 1.3rem;
}

.moto-extra {
  margin-top: 1rem;
  background: #f9fafb;
  border: 1px dashed #e0e7ff;
  padding: 1rem;
  border-radius: 10px;
}

.moto-extra-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.moto-extra-header h4 {
  margin: 0;
  color: #4b5563;
  font-size: 1.1rem;
}

.hint {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.3;
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
  padding: 0.5rem 0.5rem;
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
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
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
  padding: 3rem 1rem;
  color: #999;
  font-size: 1.1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin: 0 12px;
}

.pecas-list {
  display: grid;
  gap: 0.75rem;
}

.peca-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #f59e0b;
}

.peca-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.peca-nome {
  font-weight: 600;
  color: #333;
}

.peca-preco {
  color: #667eea;
  font-weight: 600;
}

.peca-details {
  display: grid;
  grid-template-columns: auto auto auto;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: #666;
}

.peca-detail-item {
  display: flex;
  gap: 0.5rem;
}

.peca-detail-label {
  font-weight: 600;
  color: #333;
}

.moto-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

@media (max-width: 768px) {
  .clientes-view {
    gap: 1.5rem;
    padding: 0.5rem;
  }

  .view-header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.8rem;
    padding: 0 8px;
  }

  .view-header h2 {
    font-size: 1.5rem;
  }

  .header-actions {
    flex-direction: column;
    gap: 0.6rem;
  }

  .search-input {
    min-width: 100%;
    padding: 0.7rem 1rem;
    font-size: 0.95rem;
  }

  .btn-add {
    width: 100%;
    padding: 0.7rem 1rem;
    font-size: 0.95rem;
  }

  .clientes-list {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    padding: 0 8px;
  }

  .cliente-card {
    padding: 1.2rem;
  }

  .cliente-info h4 {
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
  }

  .cliente-info p {
    font-size: 0.85rem;
    margin: 0.4rem 0;
  }

  .cliente-actions {
    margin-top: 0.8rem;
    gap: 0.4rem;
  }

  .btn-history,
  .btn-edit,
  .btn-delete {
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }

  .form-grid input {
    padding: 0.8rem;
    font-size: 0.95rem;
  }

  .moto-grid {
    grid-template-columns: 1fr;
  }

  .form-container {
    padding: 1.2rem 8px;
  }

  .form-container h3 {
    font-size: 1.2rem;
  }

  .form-actions {
    gap: 0.8rem;
    flex-direction: row;
  }

  .form-actions button {
    flex: 1;
    padding: 0.7rem;
  }
}

/* Mobile pequeno - 480px e abaixo */
@media (max-width: 480px) {
  .clientes-view {
    gap: 1rem;
    padding: 0;
  }

  .view-header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.6rem;
    padding: 0 8px;
    margin-bottom: 0.5rem;
  }

  .view-header h2 {
    font-size: 1.3rem;
  }

  .header-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-input {
    min-width: 100%;
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .btn-add {
    width: 100%;
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .clientes-list {
    grid-template-columns: 1fr;
    gap: 0.8rem;
    padding: 0 8px;
  }

  .cliente-card {
    padding: 1rem;
    border-radius: 10px;
  }

  .cliente-info h4 {
    font-size: 1rem;
    margin-bottom: 0.6rem;
  }

  .cliente-info p {
    font-size: 0.8rem;
    margin: 0.3rem 0;
    line-height: 1.3;
  }

  .cliente-actions {
    margin-top: 0.6rem;
    gap: 0.3rem;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }

  .btn-history,
  .btn-edit,
  .btn-delete {
    padding: 0.5rem 0.6rem;
    font-size: 0.75rem;
    white-space: nowrap;
    min-width: auto;
  }

  .form-container {
    padding: 1rem 8px;
    border-radius: 8px;
  }

  .form-container h3 {
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }

  .form-grid input {
    padding: 0.6rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .moto-extra {
    margin-top: 0.8rem;
    padding: 0.8rem;
  }

  .moto-extra-header {
    margin-bottom: 0.6rem;
  }

  .moto-extra-header h4 {
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
  }

  .hint {
    font-size: 0.75rem;
  }

  .moto-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    gap: 0.6rem;
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
    padding: 0.6rem;
    font-size: 0.9rem;
  }

  /* Modal responsivo */
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-historico {
    max-height: calc(100vh - 1rem);
    border-radius: 12px 12px 0 0;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-header h3 {
    font-size: 1.1rem;
  }

  .close-btn {
    font-size: 1.2rem;
  }

  .modal-body {
    padding: 0.8rem;
    overflow-y: auto;
  }

  .historico-section {
    margin-bottom: 0.8rem;
  }

  .historico-section h4 {
    font-size: 0.95rem;
    margin-bottom: 0.6rem;
  }

  .motos-list,
  .manutencoes-list,
  .pecas-list {
    gap: 0.6rem;
  }

  .moto-item,
  .manutencao-item,
  .peca-item {
    padding: 0.8rem;
  }

  .moto-item p,
  .manutencao-item p,
  .peca-item p {
    font-size: 0.8rem;
  }

  .peca-details {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }
}

/* Tablet intermediário - 1024px */
@media (max-width: 1024px) {
  .clientes-list {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }

  .view-header {
    padding: 0 10px;
  }

  .search-input {
    min-width: calc(100% - 20px);
  }

  .cliente-actions {
    display: flex;
    gap: 0.4rem;
  }

  .btn-history,
  .btn-edit,
  .btn-delete {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }
}

/* Tela grande - 1440px+ */
@media (min-width: 1440px) {
  .clientes-list {
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  }

  .view-header {
    gap: 1.5rem;
  }

  .search-input {
    min-width: 400px;
  }

  .cliente-card {
    padding: 1.8rem;
  }

  .cliente-info h4 {
    font-size: 1.3rem;
  }
}
</style>
