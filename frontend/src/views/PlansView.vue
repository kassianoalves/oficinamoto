<template>
  <div class="plans-view">
    <div class="plans-header">
      <h1>Escolha seu Plano</h1>
      <p>Desbloqueie recursos exclusivos para sua oficina</p>
    </div>

    <div class="plans-container">
      <!-- PLANO BÁSICO -->
      <div v-if="userSubscription?.plan_name === 'basic'" class="plan-card">
        <div class="badge badge-free">BÁSICO</div>
        <h2>BÁSICO</h2>
        <div class="price">
          <span>R$00.00</span>
        </div>

        <ul class="features">
          <li class="active">
            <span>👥 Clientes:</span> 50
          </li>
          <li class="active">
            <span>🏍️ Motos:</span> 50
          </li>
          <li class="active">
            <span>📅 Agendamentos:</span> 50
          </li>
          <li>
            <span>❌ Gerenciador de Fornecedores</span>
          </li>
          <li>
            <span>❌ Lembretes Automáticos</span>
          </li>
          <li>
            <span>❌ Integração WhatsApp/SMS</span>
          </li>
          <li>
            <span>❌ Agendamentos Prioritários</span>
          </li>
          <li>
            <span>❌ Chat Suporte (sem fila)</span>
          </li>
          <li>
            <span>❌ Plano de Fidelidade</span>
          </li>
          <li>
            <span>❌ Backup em Nuvem</span>
          </li>
          <li>
            <span>❌ IA para Diagnóstico</span>
          </li>
          <li>
            <span>❌ App Mobile</span>
          </li>
        </ul>

        <button 
          v-if="userSubscription?.plan_name === 'basic'"
          class="btn-current" 
          disabled
        >
          ✓ Plano Atual
        </button>
        <button v-else class="btn-choose btn-downgrade" disabled>
          Plano Anterior
        </button>
      </div>

      <!-- PLANO PRO -->
      <div class="plan-card">
        <div class="badge badge-pro">⭐ MAIS POPULAR</div>
        
        <h2>PRO</h2>
        <div class="price">
          <span>R$ 99.90<span class="period">/mês</span></span>
        </div>

        <ul class="features">
          <li class="active">
            <span>👥 Clientes:</span> 1000
          </li>
          <li class="active">
            <span>🏍️ Motos:</span> 1000
          </li>
          <li class="active">
            <span>📅 Agendamentos:</span> 250
          </li>
          <li class="active">
            <span>✅ Gerenciador de Fornecedores</span>
          </li>
          <li class="active">
            <span>✅ Lembretes Automáticos</span>
          </li>
          <li class="active">
            <span>✅ Integração WhatsApp/SMS</span>
          </li>
          <li class="active">
            <span>✅ Agendamentos Prioritários</span>
          </li>
          <li class="active">
            <span>✅ Chat Suporte (sem fila)</span>
          </li>
          <li class="active">
            <span>✅ Plano de Fidelidade</span>
          </li>
          <li>
            <span>❌ Backup em Nuvem</span>
          </li>
          <li>
            <span>❌ IA para Diagnóstico</span>
          </li>
          <li>
            <span>❌ App Mobile</span>
          </li>
          
          <li>
            <span>❌ Fornecedores</span>
          </li>
        </ul>

        <button 
          v-if="userSubscription?.plan_name === 'pro'"
          class="btn-current" 
          disabled
        >
          ✓ Plano Atual
        </button>
        <button 
          v-else-if="userSubscription?.plan_name === 'basic'"
          @click="escolherPlano('pro')" 
          class="btn-choose btn-pro"
        >
          FAZER UPGRADE PRO
        </button>
        <button v-else class="btn-choose btn-downgrade" disabled>
          Plano Superior
        </button>
      </div>

      <!-- PLANO ENTERPRISE -->
      <div class="plan-card enterprise-badge">
        <div class="badge badge-enterprise">👑 PREMIUM</div>
        
        <h2>ENTERPRISE</h2>
        <div class="price">
          <span>R$ 499.90<span class="period">/mês</span></span>
        </div>

        <ul class="features">
          <li class="active">
            <span>👥 Clientes:</span> Ilimitado
          </li>
          <li class="active">
            <span>🏍️ Motos:</span> Ilimitado
          </li>
          <li class="active">
            <span>📅 Agendamentos:</span> Ilimitado
          </li>
          <li class="active">
            <span>✅ Gerenciador de Fornecedores</span>
          </li>
          <li class="active">
            <span>✅ Lembretes Automáticos</span>
          </li>
          <li class="active">
            <span>✅ Integração WhatsApp/SMS</span>
          </li>
          <li class="active">
            <span>✅ Agendamentos Prioritários</span>
          </li>
          <li class="active">
            <span>✅ Chat Suporte (sem fila)</span>
          </li>
          <li class="active">
            <span>✅ Plano de Fidelidade</span>
          </li>
          <li class="active">
            <span>✅ Backup em Nuvem</span>
          </li>
          <li class="active">
            <span>✅ IA para Diagnóstico</span>
          </li>
          <li class="active">
            <span>✅ App Mobile</span>
          </li>
          
          <li class="active">
            <span>✅ Loja de Produtos</span>
          </li>
          <li class="active">
            <span>✅ Base de Manuais</span>
          </li>
        </ul>

        <button 
          v-if="userSubscription?.plan_name === 'enterprise'"
          class="btn-current" 
          disabled
        >
          ✓ Plano Atual
        </button>
        <button 
          v-else
          @click="escolherPlano('enterprise')" 
          class="btn-choose btn-enterprise"
        >
          CONTRATAR ENTERPRISE
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'
import { useSubscription } from '@/composables/useSubscription'

export default {
  name: 'PlansView',
  setup() {
    const { success, error } = useToast()
    const { userSubscription, loadSubscription } = useSubscription()

    const escolherPlano = async (planName) => {
      try {
        if (planName === 'free') {
          success('Você está usando o plano Básico')
          return
        }

        if (planName === 'pro') {
          const res = await api.post('/subscription/upgrade-pro/')
          const paymentUrl = res?.data?.payment_url

          // Evita redirecionar para página vazia quando a API não devolve checkout
          if (!paymentUrl) {
            success('Upgrade PRO registrado. Em breve entraremos em contato.')
            return
          }

          window.location.href = paymentUrl
          return
        }

        if (planName === 'enterprise') {
          // Backend ainda não tem endpoint dedicado; reutiliza o upgrade-pro para gerar checkout
          const res = await api.post('/subscription/upgrade-pro/')
          const paymentUrl = res?.data?.payment_url

          if (!paymentUrl) {
            success('Pedido Enterprise registrado. Em breve entraremos em contato.')
            return
          }

          window.location.href = paymentUrl
          return
        }
      } catch (err) {
        error('Erro ao processar plano')
      }
    }

    onMounted(() => {
      loadSubscription()
    })

    return {
      userSubscription,
      escolherPlano
    }
  }
}
</script>

<style scoped>
.plans-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}

.plans-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plans-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.plans-header p {
  font-size: 1.1rem;
  color: #666;
}

.plans-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.plan-card {
  background: rgb(255, 255, 255);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  flex-direction: column;
}
.plan-card:nth-child(1) {
  border-color: #1700e7;
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.15);
}
.plan-card:nth-child(2) {
  border-color: #05b178;
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.15);
}

.plan-card:nth-child(3) {
  border-color: #FF1493;
  box-shadow: 0 6px 25px rgba(255, 20, 147, 0.15);
}

.plan-card:hover {
  box-shadow: 0 8px 35px rgba(0, 0, 0, 0.12);
  transform: translateY(-8px);
  border-color: #667eea;
}

.plan-card:nth-child(3):hover {
  border-color: #FF1493;
}
.badge-free {
  position: absolute;
  top: -20px;
  left: 35%;
  transform: translateX(-50%);
  color: white;
  padding: 0.7rem 1.4rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  z-index: 10;
}
.badge-pro {
  position: absolute;
  top: -20px;
  left: 22%;
  transform: translateX(-50%);
  color: white;
  padding: 0.7rem 1.4rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  z-index: 10;
}
.badge-enterprise {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  padding: 0.7rem 1.4rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  z-index: 10;
}

.badge-free {
  background: linear-gradient(135deg, #0025f8 0%, #00c9fc 100%);
}

.badge-pro {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.badge-enterprise {
  background: linear-gradient(135deg, #da680b 0%, #faaa33 50%, #FFD700 100%);
  animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% { 
    transform: translateX(-50%) scale(1); 
  }
  50% { 
    transform: translateX(-50%) scale(1.05); 
  }
}

.plan-card h2 {
  font-size: 1.9rem;
  color: #2d3748;
  margin: 1.2rem 0 0.8rem 0;
  text-align: center;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.price {
  text-align: center;
  font-size: 2.8rem;
  color: #667eea;
  font-weight: 800;
  margin: 0.5rem 0 1.5rem 0;
  line-height: 1;
}

.plan-card.enterprise-badge .price {
  background: linear-gradient(135deg, #FF1493, #FF69B4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.period {
  font-size: 1rem;
  color: #718096;
  font-weight: 500;
}

.features {
  list-style: none;
  margin: 1.5rem 0;
  padding: 0;
  flex: 1;
}

.features li {
  padding: 0.75rem 0.5rem;
  color: #a0aec0;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: all 0.2s;
}

.features li:last-child {
  border-bottom: none;
}

.features li.active {
  color: #2d3748;
  font-weight: 500;
}

.features li.feature-pro {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-radius: 8px;
  padding: 0.85rem 0.8rem;
  font-weight: 600;
  color: #667eea;
  border-bottom: none;
  margin: 0.3rem 0;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.features li.feature-enterprise {
  background: linear-gradient(135deg, rgba(255, 20, 147, 0.08), rgba(255, 215, 0, 0.08));
  border-radius: 8px;
  padding: 0.85rem 0.8rem;
  font-weight: 600;
  color: #FF1493;
  border-bottom: none;
  margin: 0.3rem 0;
  box-shadow: 0 2px 8px rgba(255, 20, 147, 0.1);
}

.features li.feature-free {
  background: linear-gradient(135deg, rgba(72, 187, 120, 0.08), rgba(56, 161, 105, 0.08));
  border-radius: 8px;
  padding: 0.85rem 0.8rem;
  font-weight: 600;
  color: #48bb78;
  border-bottom: none;
  margin: 0.3rem 0;
  box-shadow: 0 2px 8px rgba(72, 187, 120, 0.1);
}

.features span {
  margin-right: 0.5rem;
}

.btn-choose,
.btn-current {
  width: 100%;
  padding: 1.1rem 1.5rem;
  margin-top: auto;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #1f6ed4;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-choose:hover {
  background: #5782f8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 0, 255, 0.15);
}

.btn-pro {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-pro:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  transform: translateY(-3px);
}

.btn-enterprise {
  background: linear-gradient(135deg, #FF1493 0%, #c948f0 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 0, 234, 0.3);
}

.btn-enterprise:hover {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
  transform: translateY(-3px);
}



.btn-current {
  background: linear-gradient(135deg, #0b1fd3, #1f89e0);
  color: white;
  cursor: not-allowed;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .plans-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .plans-header h1 {
    font-size: 2rem;
  }

  .plans-header p {
    font-size: 1rem;
  }

  .price {
    font-size: 2.3rem;
  }

  .plan-card h2 {
    font-size: 1.6rem;
  }
}
</style>
