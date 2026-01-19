<template>
  <div class="manutencao-view">
    <div class="view-header">
      <h2>Agendamentos ({{ agendamentosFiltrados.length }})</h2>
      <div class="header-actions">
        <button v-if="viewMode === 'historico'" @click="viewMode = 'cards'" :class="['btn-toggle', { active: viewMode === 'cards' }]">📋 Cards</button>
        <select v-model="filtroStatus" class="filter-select" v-show="viewMode === 'cards'">
          <option value="">Todos os Status</option>
          <option value="pendente">Pendente</option>
          <option value="concluido">Concluído</option>
          <option value="cancelado">Cancelado</option>
        </select>
        <button @click="showForm = !showForm" class="btn-add" v-show="viewMode === 'cards'">➕ Novo Agendamento</button>
        <button v-if="viewMode === 'cards'" @click="viewMode = 'historico'" :class="['btn-toggle', { active: viewMode === 'historico' }]">📊 Histórico</button>
      </div>
    </div>


    <!-- Loading State -->
    <SkeletonLoader v-if="loading" :count="4" variant="card" />

    <!-- View de Cards -->
    <div v-else-if="viewMode === 'cards'" class="content-container">
      <!-- Formulário de Adição/Edição -->
      <div v-if="showForm" class="form-container form-modal">
        <form @submit.prevent="salvarAgendamento">
          <h3>{{ editingId ? 'Editar Agendamento' : 'Novo Agendamento' }}</h3>
          <div class="form-grid">
            <select v-model="clienteSelecionado" @change="carregarMotosCliente" required>
              <option value="">Selecione o Cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }} ({{ cliente.telefone }})
              </option>
            </select>
            <select v-model="form.moto" :disabled="!clienteSelecionado" required>
              <option value="">{{ clienteSelecionado ? 'Selecione a Moto' : 'Selecione um cliente primeiro' }}</option>
              <option v-for="moto in motosCliente" :key="moto.id" :value="moto.id">
                {{ moto.marca }} {{ moto.modelo }} ({{ moto.placa }}) - {{ moto.ano }}
              </option>
            </select>
            <select v-model="form.tipo_servico" required>
              <option value="troca">Troca de Óleo</option>
              <option value="reparo">Reparo</option>
              <option value="assistencia">Assistência</option>
              <option value="vistoria">Vistoria</option>
              <option value="manutencao">Manutenção Periódica</option>
            </select>
            <input v-model="form.data_agendada" type="datetime-local" required>
            <select v-model="form.status">
              <option value="pendente">Pendente</option>
              <option value="concluido">Concluído</option>
              <option value="cancelado">Cancelado</option>
              </select>
          </div>
          <div class="form-full">
            <textarea v-model="form.observacoes" placeholder="Observações"></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">{{ editingId ? 'Atualizar' : 'Salvar' }}</button>
            <button type="button" @click="resetForm" class="btn btn-secondary">Cancelar</button>
          </div>
        </form>
      </div>

      <!-- Lista de Agendamentos -->
      <div v-if="agendamentosFiltrados.length" class="agendamentos-list">
        <div v-for="agendamento in agendamentosFiltrados" :key="agendamento.id" class="agendamento-card" :class="getStatusClass(agendamento.status)">
          <div class="agendamento-info">
            <h4>{{ getClienteNome(agendamento.moto) }}</h4>
            <p><strong>Moto:</strong> {{ getMotoDados(agendamento.moto) }}</p>
            <p><strong>Tipo:</strong> {{ getTipoServico(agendamento.tipo_servico) }}</p>
            <p><strong>Data/Hora:</strong> {{ formatDate(agendamento.data_agendada) }}</p>
            <p><strong>Status:</strong> <span class="status-badge">{{ agendamento.status }}</span></p>
            <p><strong>Observações:</strong> {{ agendamento.observacoes || '-' }}</p>
          </div>
          <div class="agendamento-actions">
            <button @click="editarAgendamento(agendamento)" class="btn btn-edit">✏️Editar</button>
            <button v-if="agendamento.status !== 'concluido'" @click="finalizarAgendamento(agendamento)" class="btn btn-finish">✓Finalizar</button>
            <button @click="deletarAgendamento(agendamento.id)" class="btn btn-delete">🗑️Deletar</button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>Nenhum agendamento registrado. Clique em "Novo Agendamento" para começar.</p>
      </div>
    </div>

    <!-- View de Histórico (Tabela) -->
    <div v-else-if="viewMode === 'historico'" class="historico-container">
      <div v-if="agendamentosConcluidos.length" class="tabela-wrapper">
        <div class="historico-search-bar">
          <input v-model="historicoSearch" type="text" placeholder="Pesquisar histórico..." class="historico-search-input" />
        </div>
        <table class="historico-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Moto</th>
              <th>Tipo de Serviço</th>
              <th>Data/Hora</th>
              <th>Observações</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="agendamento in historicoFiltrado" :key="agendamento.id">
              <td>{{ getClienteNome(agendamento.moto) }}</td>
              <td>{{ getMotoDados(agendamento.moto) }}</td>
              <td>{{ getTipoServico(agendamento.tipo_servico) }}</td>
              <td>{{ formatDate(agendamento.data_agendada) }}</td>
              <td>{{ agendamento.observacoes || '-' }}</td>
              <td>
                <button @click="restaurarAgendamento(agendamento)" class="btn btn-edit">⏪ Restaurar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state">
        <p>Nenhum agendamento concluído ainda.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'
import { useEntityCache } from '@/composables/useEntityCache'
import SkeletonLoader from '@/components/SkeletonLoader.vue'

export default {
  name: 'ManutencaoView',
  components: {
    SkeletonLoader
  },
  setup() {
    const { success, error } = useToast()
    const agendamentos = ref([])
    const { motos, clientes, loadMotos, loadClientes } = useEntityCache()
    const clienteSelecionado = ref('')
    const motosCliente = ref([])
    const showForm = ref(false)
    const editingId = ref(null)
    const filtroStatus = ref('')
    const loading = ref(true)
    const viewMode = ref('cards') // 'cards' ou 'historico'
    const form = ref({
      moto: '',
      tipo_servico: 'manutencao',
      data_agendada: '',
      observacoes: '',
      status: 'pendente'
    })
    const historicoSearch = ref("");

    const agendamentosFiltrados = computed(() => {
      let lista = agendamentos.value.filter(a => a.status !== 'concluido')
      // Se houver filtro específico, filtra por esse status (exceto concluido)
      if (filtroStatus.value) {
        lista = lista.filter(a => a.status === filtroStatus.value)
      }
      return lista
    })

    const agendamentosConcluidos = computed(() => {
      return agendamentos.value.filter(a => a.status === 'concluido')
    })

    const historicoFiltrado = computed(() => {
      if (!historicoSearch.value) return agendamentosConcluidos.value;
      const termo = historicoSearch.value.toLowerCase();
      return agendamentosConcluidos.value.filter(a => {
        return (
          getClienteNome(a.moto).toLowerCase().includes(termo) ||
          getMotoDados(a.moto).toLowerCase().includes(termo) ||
          getTipoServico(a.tipo_servico).toLowerCase().includes(termo) ||
          formatDate(a.data_agendada).toLowerCase().includes(termo) ||
          (a.observacoes || '').toLowerCase().includes(termo)
        );
      });
    });

    const carregarAgendamentos = async () => {
      try {
        const res = await api.get('/agendamentos/')
        agendamentos.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar agendamentos:', err)
        error('Erro ao carregar agendamentos')
      }
    }

    const carregarDadosBase = async () => {
      loading.value = true
      try {
        const [agRes] = await Promise.all([
          api.get('/agendamentos/'),
          loadMotos(),
          loadClientes()
        ])
        agendamentos.value = agRes.data.results || agRes.data || []
      } catch (err) {
        console.error('Erro ao carregar dados iniciais:', err)
        error('Erro ao carregar dados iniciais')
      } finally {
        loading.value = false
      }
    }

    const carregarMotosCliente = () => {
      if (!clienteSelecionado.value) {
        motosCliente.value = []
        form.value.moto = ''
        return
      }
      const todasMotos = motos.value || []
      motosCliente.value = todasMotos.filter(m => m.cliente === parseInt(clienteSelecionado.value))
      form.value.moto = '' // Limpa a seleção de moto ao trocar de cliente
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

    const getMotoDados = (motoId) => {
      const moto = motos.value.find(m => m.id === motoId)
      return moto ? `${moto.marca} ${moto.modelo} (${moto.placa})` : 'Moto desconhecida'
    }

    const getClienteNome = (motoId) => {
      const moto = motos.value.find(m => m.id === motoId)
      if (!moto) return 'Cliente desconhecido'
      const cliente = clientes.value.find(c => c.id === moto.cliente)
      return cliente ? cliente.nome : 'Cliente desconhecido'
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }

    const formatDateTimeLocal = (dateString) => {
      // Converte data ISO para formato que datetime-local espera: YYYY-MM-DDTHH:mm
      if (!dateString) return ''
      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}`
    }

    const getStatusClass = (status) => {
      return `status-${status}`
    }

    const salvarAgendamento = async () => {
      try {
        if (editingId.value) {
          await api.put(`/agendamentos/${editingId.value}/`, form.value)
          success('Agendamento atualizado com sucesso!')
        } else {
          await api.post('/agendamentos/', form.value)
          success('Agendamento criado com sucesso!')
        }
        resetForm()
        carregarAgendamentos()
      } catch (err) {
        console.error('Erro ao salvar agendamento:', err)
        const errorMsg = err.response?.data?.detail || 
                        err.response?.data?.non_field_errors?.[0] || 
                        'Erro ao salvar agendamento'
        error(errorMsg)
      }
    }

    const editarAgendamento = (agendamento) => {
      editingId.value = agendamento.id
      form.value = {
        ...agendamento,
        data_agendada: formatDateTimeLocal(agendamento.data_agendada)
      }
      
      // Obter o cliente da moto
      const moto = motos.value.find(m => m.id === agendamento.moto)
      if (moto) {
        clienteSelecionado.value = moto.cliente.toString()
        // Carregar as motos do cliente
        const todasMotos = motos.value || []
        motosCliente.value = todasMotos.filter(m => m.cliente === moto.cliente)
      }
      
      showForm.value = true
    }

    const deletarAgendamento = async (id) => {
      if (confirm('Deseja deletar este agendamento?')) {
        try {
          await api.delete(`/agendamentos/${id}/`)
          success('Agendamento deletado com sucesso!')
          carregarAgendamentos()
        } catch (err) {
          console.error('Erro ao deletar agendamento:', err)
          error('Erro ao deletar agendamento. Verifique as permissões.')
        }
      }
    }

    const finalizarAgendamento = async (agendamento) => {
      try {
        const payload = {
          ...agendamento,
          status: 'concluido'
        }
        await api.put(`/agendamentos/${agendamento.id}/`, payload)
        success('Agendamento finalizado com sucesso!')
        await carregarAgendamentos()
      } catch (err) {
        console.error('Erro ao finalizar agendamento:', err)
        const errorMsg = err.response?.data?.detail ||
                        err.response?.data?.non_field_errors?.[0] ||
                        Object.values(err.response?.data || {}).flat()[0] ||
                        'Erro ao finalizar agendamento'
        error(errorMsg)
      }
    }

    const restaurarAgendamento = async (agendamento) => {
      try {
        const payload = {
          ...agendamento,
          status: 'pendente'
        }
        await api.put(`/agendamentos/${agendamento.id}/`, payload)
        success('Agendamento restaurado!')
        await carregarAgendamentos()
      } catch (err) {
        console.error('Erro ao restaurar agendamento:', err)
        const errorMsg = err.response?.data?.detail ||
                        err.response?.data?.non_field_errors?.[0] ||
                        Object.values(err.response?.data || {}).flat()[0] ||
                        'Erro ao restaurar agendamento'
        error(errorMsg)
      }
    }

    const resetForm = () => {
      form.value = {
        moto: '',
        tipo_servico: 'manutencao',
        data_agendada: '',
        observacoes: '',
        status: 'pendente'
      }
      clienteSelecionado.value = ''
      motosCliente.value = []
      editingId.value = null
      showForm.value = false
    }

    onMounted(() => {
      carregarDadosBase()
    })

    return {
      agendamentos,
      agendamentosFiltrados,
      agendamentosConcluidos,
      motos,
      clientes,
      clienteSelecionado,
      motosCliente,
      showForm,
      editingId,
      form,
      filtroStatus,
      loading,
      viewMode,
      carregarMotosCliente,
      salvarAgendamento,
      editarAgendamento,
      deletarAgendamento,
      finalizarAgendamento,
      restaurarAgendamento,
      resetForm,
      carregarDadosBase,
      getTipoServico,
      getMotoDados,
      getClienteNome,
      formatDate,
      formatDateTimeLocal,
      getStatusClass,
      historicoSearch,
      historicoFiltrado
    }
  }
}
</script>

<style scoped>
.manutencao-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1.2rem 0.5rem 0.5rem 0.5rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.content-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-modal {
  position: sticky;
  top: 100px;
  z-index: 10;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  flex-wrap: wrap;
}

.btn-toggle {
  padding: 0.8rem 0.8rem;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-toggle:hover {
  background: #f0f0ff;
}

.btn-toggle.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.filter-select {
  padding: 0.8rem 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 200px;
  transition: all 0.3s;
  background: white;
  cursor: pointer;
}

.filter-select:focus {
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
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
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

.form-full {
  margin-bottom: 1.5rem;
}

.form-full textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  min-height: 100px;
  resize: vertical;
}

.form-full textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 0.85rem;
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

.agendamentos-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  justify-items: center;
}

@media (max-width: 900px) {
  .agendamentos-list {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 600px) {
  .agendamentos-list {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}

@media (max-width: 1200px) {
  .agendamentos-list {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 900px) {
  .agendamentos-list {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 600px) {
  .agendamentos-list {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}

.agendamento-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  padding: 0.8rem 0.7rem 0.7rem 0.7rem;
  margin-bottom: 0.5rem;
  border: 1px solid #f0f0f0;
  min-width: 0;
  width: 100%;
  max-width: 320px;
  margin-left: auto;
  margin-right: auto;
  transition: box-shadow 0.18s, border 0.18s;
}

.agendamento-card.status-pendente {
  border-left-color: #ffa500;
}

.agendamento-card.status-concluido {
  border-left-color: #00d084;
}

.agendamento-card.status-cancelado {
  border-left-color: #f5576c;
}

.agendamento-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.agendamento-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.agendamento-info h4 {
  color: #667eea;
  margin: 0;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

.agendamento-info p {
  color: #666;
  margin: 0;
  font-size: 0.8rem;
  min-height: 1.2rem;
  display: flex;
  align-items: center;
}

.status-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #f0f0f0;
  color: #333;
}

.agendamento-actions {
  display: flex;
  gap: 0.2rem;
  margin-top: 0.3rem;
  justify-content: flex-start;
}

.agendamento-actions button {
  width: 110px;
  min-width: 10px;
  max-width: 95px;
  height: 30px;
  font-size: 0.93rem;
  padding: 0.18rem 0.5rem;
  border-radius: 5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3em;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  letter-spacing: 0.01em;
  transition: box-shadow 0.18s, filter 0.18s;
}

.btn-edit {
  background: #4facfe;
  color: white;
  flex: 1;
}

.btn-finish {
  background: #00d084;
  color: white;
  flex: 1;
}

.btn-delete {
  background: #f5576c;
  color: white;
  flex: 1;
  
}

.btn-edit:hover,
.btn-finish:hover,
.btn-delete:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn:disabled:hover {
  opacity: 0.5;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.1rem;
}

/* Histórico - Tabela */
.historico-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabela-wrapper {
  overflow-x: auto;
}

.historico-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.97rem;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(80, 80, 120, 0.08);
}

.historico-table thead {
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
}

.historico-table th {
  padding: 0.8rem 0.5rem;
  text-align: left;
  font-weight: 700;
  letter-spacing: 0.02em;
  border: none;
}

.historico-table tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.18s;
}

.historico-table tbody tr:hover {
  background: #f6fbff;
}

.historico-table td {
  padding: 0.85rem 0.7rem;
  color: #444;
  border: none;
  vertical-align: middle;
}

.historico-table td:last-child {
  text-align: right;
}

.historico-table tbody tr:last-child {
  border-bottom: none;
}

/* Botão restaurar e outros na tabela */
.historico-table .btn {
  padding: 0.38rem 0.9rem;
  font-size: 0.93rem;
  border-radius: 7px;
  font-weight: 600;
  border: none;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  transition: background 0.18s, color 0.18s, box-shadow 0.18s;
  margin-left: 0.2rem;
  margin-right: 0.2rem;
  display: flex;
  align-items: right;
  gap: 0.4em;
}

.historico-table .btn-edit {
  background: linear-gradient(90deg, #4facfe 60%, #00f2fe 100%);
  color: #fff;
}

.historico-table .btn-edit:hover {
  background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(79, 172, 254, 0.13);
}

.historico-search-bar {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}
.historico-search-input {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1.5px solid #d1d5db;
  font-size: 1rem;
  width: 100%;
  max-width: 320px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  transition: border 0.18s;
}
.historico-search-input:focus {
  border-color: #4facfe;
  outline: none;
}
</style>
