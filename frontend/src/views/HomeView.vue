<template>
  <div class="home-view">
    <div class="hero">
      <h1>Bem-vindo ao Gerenciador de Moto Express</h1>
      <p>Sistema completo para gerenciar clientes, motos e manutenções</p>
    </div>

    <!-- Badge do Plano
    <div class="plan-badge" :class="{ 'plan-pro': userPlan === 'pro' }">
      <span v-if="userPlan === 'pro'">⭐ Plano PRO Ativo</span>
      <span v-else>📦 Plano Básico - <router-link to="/planos" class="upgrade-link">Fazer Upgrade</router-link></span>
    </div> -->

    <div class="stats-grid">
      <div class="stat-card">
        <h3>{{ totalClientes }}</h3>
        <p>Clientes Cadastrados</p>
      </div>
      <div class="stat-card">
        <h3>{{ totalMotos }}</h3>
        <p>Motos Registradas</p>
      </div>
      <div class="stat-card">
        <h3>{{ agendamentosProximos }}</h3>
        <p>Agendamentos Concluídos</p>
      </div>
    </div>

    <div class="quick-actions">
      <router-link to="/clientes" class="action-btn btn-primary">
        ➕ Novo Cliente
      </router-link>
      <button @click="abrirFila" class="action-btn btn-secondary btn-fila">
        <span class="fila-badge" v-if="filaAtendimento.length > 0">{{ filaAtendimento.length }}</span>
        📋 Fila de Atendimento
      </button>
      <router-link to="/manutencoes" class="action-btn btn-tertiary">
        🔧 Agendar Manutenção
      </router-link>
    </div>

    <!-- Modal Fila de Atendimento -->
    <div v-if="showFila" class="modal-overlay" @click="fecharFila">
      <div class="modal-fila" @click.stop>
        <div class="modal-header">
          <h2>📋 Fila de Atendimento</h2>
          <button class="close-btn" @click="fecharFila">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="filaAtendimento.length" class="fila-list">
            <div v-for="(item, index) in filaAtendimento" :key="index" class="fila-item">
              <div class="fila-numero">{{ index + 1 }}</div>
              <div class="fila-info">
                <h4>{{ item.cliente_nome }}</h4>
                <p><strong>Moto:</strong> {{ item.moto_info }}</p>
                <p><strong>Serviço:</strong> {{ item.tipo_servico }}</p>
                <p><strong>Data/Hora:</strong> {{ item.data_hora }}</p>
                <p v-if="item.observacoes" class="observacoes"><strong>Obs:</strong> {{ item.observacoes }}</p>
              </div>
              <div class="fila-status" :class="item.status">{{ item.status_label }}</div>
            </div>
          </div>
          <div v-else class="empty-fila">
            <p>Nenhum agendamento para hoje</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="fecharFila" class="btn btn-secondary">Fechar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from '@/api.js'
import { useSubscription } from '@/composables/useSubscription'

export default {
  name: 'HomeView',
  setup() {
    const totalClientes = ref(0)
    const totalMotos = ref(0)
    const agendamentosProximos = ref(0)
    const showFila = ref(false)
    const filaAtendimento = ref([])

    // Estado de assinatura centralizado
    const { userSubscription, loadSubscription } = useSubscription()
    const userPlan = computed(() => userSubscription.value?.plan_name || 'free')

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

    const getStatusLabel = (status) => {
      const labels = {
        'pendente': 'Pendente',
        'em_andamento': 'Em Andamento',
        'concluido': 'Concluído',
        'cancelado': 'Cancelado'
      }
      return labels[status] || status
    }

    const formatDateTime = (dateString) => {
      const date = new Date(dateString)
      const dia = date.toLocaleDateString('pt-BR')
      const hora = date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      return `${dia} às ${hora}`
    }

    const carregarFila = async () => {
      try {
        const [agendamentosRes, motosRes, clientesRes] = await Promise.all([
          api.get('/agendamentos/'),
          api.get('/motos/'),
          api.get('/clientes/')
        ])

        const agendamentos = agendamentosRes.data.results || agendamentosRes.data || []
        const motos = motosRes.data.results || motosRes.data || []
        const clientes = clientesRes.data.results || clientesRes.data || []

        // Filtrar agendamentos pendentes e em andamento, ordenados por data e hora
        const filaProcessada = agendamentos
          .filter(a => a.status !== 'concluido' && a.status !== 'cancelado')
          .map(agendamento => {
            const moto = motos.find(m => m.id === agendamento.moto)
            const cliente = clientes.find(c => c.id === moto?.cliente)
            return {
              cliente_nome: cliente?.nome || 'Cliente desconhecido',
              moto_info: moto ? `${moto.marca} ${moto.modelo} (${moto.placa})` : 'Moto desconhecida',
              tipo_servico: getTipoServico(agendamento.tipo_servico),
              data_hora: formatDateTime(agendamento.data_agendada),
              data_agendada: agendamento.data_agendada,
              observacoes: agendamento.observacoes,
              status: agendamento.status,
              status_label: getStatusLabel(agendamento.status)
            }
          })
          .sort((a, b) => new Date(a.data_agendada) - new Date(b.data_agendada))

        filaAtendimento.value = filaProcessada
      } catch (error) {
        console.error('Erro ao carregar fila:', error)
      }
    }

    const abrirFila = () => {
      carregarFila()
      showFila.value = true
    }

    const fecharFila = () => {
      showFila.value = false
    }

    onMounted(async () => {
      try {
        const [clientesRes, motosRes, agendamentosRes] = await Promise.all([
          api.get('/clientes/'),
          api.get('/motos/'),
          api.get('/agendamentos/?status=concluido')
        ])

        totalClientes.value = clientesRes.data.count ?? clientesRes.data.length ?? 0
        totalMotos.value = motosRes.data.count ?? motosRes.data.length ?? 0
        agendamentosProximos.value = agendamentosRes.data.count ?? agendamentosRes.data.length ?? 0

        // Carregar fila ao inicializar
        carregarFila()
        // Carregar plano do usuário (state centralizado)
        await loadSubscription()
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      }
    })

    return {
      totalClientes,
      totalMotos,
      agendamentosProximos,
      showFila,
      filaAtendimento,
      userPlan,
      abrirFila,
      fecharFila
    }
  }
}
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(1rem, env(safe-area-inset-bottom)) max(1rem, env(safe-area-inset-left));
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.plan-badge {
  background: #f0f0f0;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  font-size: 1.1rem;
  color: #666;
  border: 2px solid #ddd;
}

.plan-badge.plan-pro {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  border-color: #FFD700;
  animation: pulse-border 2s infinite;
}

@keyframes pulse-border {
  0%, 100% { border-color: #FFD700; }
  50% { border-color: #FFA500; }
}

.upgrade-link {
  color: #667eea;
  text-decoration: underline;
  font-weight: bold;
}

.upgrade-link:hover {
  color: #764ba2;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 2.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(102, 126, 234, 0.1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
}

.stat-card h3 {
  font-size: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.stat-card p {
  color: #555;
  font-size: 1.05rem;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.action-btn {
  padding: 0.85rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.btn-primary > * {
  position: relative;
  z-index: 2;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
  transition: left 0.6s ease;
  z-index: 1;
  pointer-events: none;
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn-secondary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.btn-secondary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
  transition: left 0.6s ease;
  z-index: 1;
  pointer-events: none;
}

.btn-secondary:hover::before {
  left: 100%;
}

.btn-secondary:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn-fila {
  position: relative;
  overflow: visible;
}

.btn-fila > * {
  position: relative;
  z-index: 2;
}

.fila-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(255, 68, 68, 0.4);
  border: 2px solid white;
  z-index: 10;
  pointer-events: none;
}

.btn-tertiary {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.btn-tertiary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
  transition: left 0.5s ease;
}

.btn-tertiary:hover::before {
  left: 100%;
}

.btn-tertiary:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(79, 172, 254, 0.5);
}

/* Modal Fila */
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

.modal-fila {
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

.modal-header h2 {
  margin: 0;
  color: #667eea;
  font-size: 1.5rem;
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

.fila-list {
  display: grid;
  gap: 1rem;
}

.fila-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  align-items: flex-start;
}

.fila-numero {
  min-width: 40px;
  height: 40px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.fila-info {
  flex: 1;
}

.fila-info h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
}

.fila-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.fila-info .observacoes {
  color: #999;
  font-style: italic;
  margin-top: 0.5rem;
}

.fila-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.fila-status.pendente {
  background: #fff3cd;
  color: #856404;
}

.fila-status.em_andamento {
  background: #cfe2ff;
  color: #084298;
}

.fila-status.concluido {
  background: #d1e7dd;
  color: #0f5132;
}

.fila-status.cancelado {
  background: #f8d7da;
  color: #842029;
}

.empty-fila {
  text-align: center;
  padding: 2rem;
  color: #999;
  font-style: italic;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 2px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-secondary {
  background: #2eaa4d;
  color: #ffffff;
}

.btn-secondary:hover {
  background: #2a8842;
}

@media (max-width: 768px) {
  .home-view {
    gap: 1.5rem;
    padding: 1rem;
    padding-top: calc(1rem + env(safe-area-inset-top, 0px));
  }

  .hero {
    padding: 2rem 1.25rem;
    margin: 0;
  }

  .hero h1 {
    font-size: 1.5rem;
    line-height: 1.3;
  }

  .hero p {
    font-size: 0.95rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    margin: 0;
  }

  .stat-card {
    padding: 1.25rem 1rem;
  }

  .stat-card h3 {
    font-size: 2rem;
  }

  .quick-actions {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .action-btn {
    min-height: 48px;
    padding: 1rem;
    font-size: 1rem;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
  }

  .modal-fila {
    width: 95vw;
    max-width: none;
    margin: 1rem;
    max-height: 85vh;
  }

  .fila-item {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .home-view {
    gap: 1rem;
    padding: 0.75rem;
    padding-top: calc(0.75rem + env(safe-area-inset-top, 0px));
  }

  .hero {
    padding: 1.5rem 1rem;
    border-radius: 8px;
  }

  .hero h1 {
    font-size: 1.3rem;
  }

  .hero p {
    font-size: 0.9rem;
  }

  .stat-card {
    padding: 1rem 0.75rem;
  }

  .stat-card h3 {
    font-size: 1.75rem;
  }

  .stat-card p {
    font-size: 0.85rem;
  }

  .action-btn {
    padding: 0.875rem;
    font-size: 0.95rem;
  }
}
</style>
