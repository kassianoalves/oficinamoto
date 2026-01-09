<template>
  <div class="home-view">
    <div class="hero">
      <h1>Bem-vindo ao Gerenciador de Moto Express</h1>
      <p>Sistema completo para gerenciar clientes, motos e manutenções</p>
    </div>

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
        <p>Agendamentos Próximos</p>
      </div>
    </div>

    <div class="quick-actions">
      <router-link to="/clientes" class="action-btn btn-primary">
        ➕ Novo Cliente
      </router-link>
      <router-link to="/motos" class="action-btn btn-secondary">
        🏍️ Registrar Moto
      </router-link>
      <router-link to="/manutencoes" class="action-btn btn-tertiary">
        🔧 Agendar Manutenção
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/api.js'

export default {
  name: 'HomeView',
  setup() {
    const totalClientes = ref(0)
    const totalMotos = ref(0)
    const agendamentosProximos = ref(0)

    onMounted(async () => {
      try {
        const clientesRes = await api.get('/clientes/')
        totalClientes.value = clientesRes.data.length || clientesRes.data.count || 0

        const motosRes = await api.get('/motos/')
        totalMotos.value = motosRes.data.length || motosRes.data.count || 0

        const agendamentosRes = await api.get('/agendamentos/?status=pendente')
        agendamentosProximos.value = agendamentosRes.data.length || agendamentosRes.data.count || 0
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      }
    })

    return {
      totalClientes,
      totalMotos,
      agendamentosProximos
    }
  }
}
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-card p {
  color: #666;
  font-size: 1rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  padding: 1rem;
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
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-secondary:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
}

.btn-tertiary {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.btn-tertiary:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .stat-card h3 {
    font-size: 2rem;
  }
}
</style>
