<template>
  <div class="manutencao-view">
    <div class="view-header">
      <h2>Agendamentos ({{ agendamentosFiltrados.length }})</h2>
      <div class="header-actions">
        <select v-model="filtroStatus" class="filter-select">
          <option value="">Todos os Status</option>
          <option value="pendente">Pendente</option>
          <option value="confirmado">Confirmado</option>
          <option value="concluido">Concluído</option>
          <option value="cancelado">Cancelado</option>
        </select>
        <button @click="showForm = !showForm" class="btn-add">➕ Novo Agendamento</button>
      </div>
    </div>

    <!-- Formulário de Adição -->
    <div v-if="showForm" class="form-container">
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
            <option value="confirmado">Confirmado</option>
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
          <p v-if="agendamento.observacoes"><strong>Observações:</strong> {{ agendamento.observacoes }}</p>
        </div>
        <div class="agendamento-actions">
          <button @click="editarAgendamento(agendamento)" class="btn btn-edit">✏️ Editar</button>
          <button v-if="agendamento.status !== 'concluido'" @click="finalizarAgendamento(agendamento)" class="btn btn-finish">✓ Finalizar</button>
          <button @click="deletarAgendamento(agendamento.id)" class="btn btn-delete">🗑️ Deletar</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhum agendamento registrado. Clique em "Novo Agendamento" para começar.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'

export default {
  name: 'ManutencaoView',
  setup() {
    const { success, error } = useToast()
    const agendamentos = ref([])
    const motos = ref([])
    const clientes = ref([])
    const clienteSelecionado = ref('')
    const motosCliente = ref([])
    const showForm = ref(false)
    const editingId = ref(null)
    const filtroStatus = ref('')
    const form = ref({
      moto: '',
      tipo_servico: 'manutencao',
      data_agendada: '',
      observacoes: '',
      status: 'pendente'
    })

    const agendamentosFiltrados = computed(() => {
      let lista = agendamentos.value
      
      // Se não houver filtro específico, oculta os concluídos
      if (!filtroStatus.value) {
        lista = lista.filter(a => a.status !== 'concluido')
      } else {
        lista = lista.filter(a => a.status === filtroStatus.value)
      }
      
      return lista
    })

    const carregarAgendamentos = async () => {
      try {
        const res = await api.get('/agendamentos/')
        agendamentos.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar agendamentos:', err)
        error('Erro ao carregar agendamentos')
      }
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
        error('Erro ao carregar clientes')
      }
    }

    const carregarMotosCliente = async () => {
      if (!clienteSelecionado.value) {
        motosCliente.value = []
        form.value.moto = ''
        return
      }
      try {
        const res = await api.get('/motos/')
        const todasMotos = res.data.results || res.data || []
        motosCliente.value = todasMotos.filter(m => m.cliente === parseInt(clienteSelecionado.value))
        form.value.moto = '' // Limpa a seleção de moto ao trocar de cliente
      } catch (err) {
        console.error('Erro ao carregar motos do cliente:', err)
        error('Erro ao carregar motos do cliente')
      }
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
      form.value = { ...agendamento }
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
          moto: agendamento.moto,
          tipo_servico: agendamento.tipo_servico,
          data_agendada: agendamento.data_agendada,
          observacoes: agendamento.observacoes,
          status: 'concluido'
        }
        await api.put(`/agendamentos/${agendamento.id}/`, payload)
        success('Agendamento finalizado com sucesso!')
        carregarAgendamentos()
      } catch (err) {
        console.error('Erro ao finalizar agendamento:', err)
        const errorMsg = err.response?.data?.detail ||
                        err.response?.data?.non_field_errors?.[0] ||
                        Object.values(err.response?.data || {}).flat()[0] ||
                        'Erro ao finalizar agendamento'
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
      carregarMotos()
      carregarClientes()
      carregarAgendamentos()
    })

    return {
      agendamentos,
      agendamentosFiltrados,
      motos,
      clientes,
      clienteSelecionado,
      motosCliente,
      showForm,
      editingId,
      form,
      filtroStatus,
      carregarMotosCliente,
      salvarAgendamento,
      editarAgendamento,
      deletarAgendamento,
      finalizarAgendamento,
      resetForm,
      getTipoServico,
      getMotoDados,
      getClienteNome,
      formatDate,
      getStatusClass
    }
  }
}
</script>

<style scoped>
.manutencao-view {
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

.agendamentos-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.agendamento-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 5px solid #ccc;
  transition: transform 0.3s, box-shadow 0.3s;
}

.agendamento-card.status-pendente {
  border-left-color: #ffa500;
}

.agendamento-card.status-confirmado {
  border-left-color: #4facfe;
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

.agendamento-info h4 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.agendamento-info p {
  color: #666;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  background: #f0f0f0;
  color: #333;
}

.agendamento-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
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

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .agendamentos-list {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
