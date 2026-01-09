<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="logo">
        <h1>Moto Express</h1>
      </div>
      <div class="nav-sections">
        <ul class="nav-menu">
          <li v-if="isAuthenticated"><router-link to="/">Home</router-link></li>
          <li v-if="isAuthenticated"><router-link to="/clientes">Clientes</router-link></li>
          <li v-if="isAuthenticated"><router-link to="/manutencoes">Agendamento</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/fornecedores">Fornecedores</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/loja">Loja</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/imagens-3d">3D</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/manuais">Manuais</router-link></li>
          <li v-if="isAuthenticated"><router-link to="/planos">Planos</router-link></li>
        </ul>
        <div class="nav-actions">
          <template v-if="!isAuthenticated">
            <router-link class="nav-btn" to="/login">Login</router-link>
            <router-link class="nav-btn nav-btn-primary" to="/register">Cadastrar</router-link>
          </template>
          <template v-else>
            <button @click="openProfileModal" class="btn-user-profile">
              {{ displayName }} <span v-if="isPro" class="badge-pro">PRO</span><span v-if="isEnterprise" class="badge-enterprise">ENTERPRISE</span>
            </button>
            <button @click="logout" class="btn-logout">Sair</button>
          </template>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view @login="checkAuth" />
    </main>
    <ProfileModal 
      :show="showProfile" 
      :userData="userData"
      @close="showProfile = false"
      @update="handleProfileUpdate"
    />
    <ToastNotification />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api.js'
import ToastNotification from '@/components/ToastNotification.vue'
import ProfileModal from '@/components/ProfileModal.vue'

export default {
  name: 'App',
  components: {
    ToastNotification,
    ProfileModal
  },
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)
    const username = ref('')
    const showProfile = ref(false)
    const userData = ref({})
    const userSubscription = ref(null)
    const isPro = ref(false)
    const isEnterprise = ref(false)

    const displayName = computed(() => {
      if (userData.value.first_name && userData.value.last_name) {
        return `${userData.value.first_name} ${userData.value.last_name}`
      }
      return username.value
    })

    const checkAuth = async () => {
      const token = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      isAuthenticated.value = !!token
      
      if (user) {
        try {
          userData.value = JSON.parse(user)
          username.value = userData.value.username || userData.value.email
          
          // Carregar subscrição do usuário
          if (token) {
            await carregarSubscricao()
          }
        } catch (e) {
          username.value = ''
        }
      }
    }

    const carregarSubscricao = async () => {
      try {
        const res = await api.get('/subscription/subscription/')
        console.log('📦 Resposta da API:', res.data)
        // A API retorna paginação: {results: [{...}]}
        const subscription = res.data.results ? res.data.results[0] : (Array.isArray(res.data) ? res.data[0] : res.data)
        console.log('📋 Subscrição processada:', subscription)
        console.log('💎 Nome do plano:', subscription?.plan_name)
        userSubscription.value = subscription
        isPro.value = subscription?.plan_name === 'pro'
        isEnterprise.value = subscription?.plan_name === 'enterprise'
        console.log('✅ isPro definido como:', isPro.value)
        console.log('👑 isEnterprise definido como:', isEnterprise.value)
      } catch (err) {
        console.error('❌ Erro ao carregar subscrição:', err)
        isPro.value = false
        isEnterprise.value = false
      }
    }

    const openProfileModal = () => {
      showProfile.value = true
    }

    const handleProfileUpdate = (updatedUser) => {
      userData.value = updatedUser
      username.value = updatedUser.username || updatedUser.email
    }

    const logout = () => {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      isAuthenticated.value = false
      username.value = ''
      userData.value = {}
      router.push('/login')
    }

    onMounted(() => {
      checkAuth()
      router.afterEach(() => {
        checkAuth()
      })
    })

    return {
      isAuthenticated,
      username,
      displayName,
      userData,
      userSubscription,
      isPro,
      isEnterprise,
      showProfile,
      checkAuth,
      openProfileModal,
      handleProfileUpdate,
      logout
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #ffffff;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 700;
}

.nav-sections {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex: 1;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 0.75rem;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-menu li {
  list-style: none;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.98rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background 0.3s, transform 0.2s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background-color: #903dc7;
  transform: translateY(-2px);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-btn {
  color: white;
  text-decoration: none;
  font-weight: 600;
  padding: 0.5rem 0.9rem;
  font-size: 0.95rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.12);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-btn-primary {
  background: #ffb347;
  color: #2d3748;
  border-color: #ffb347;
}

.nav-btn-primary:hover {
  background: #ff9f1c;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-user-profile {
  background: rgba(195, 123, 236, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge-pro {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  animation: pulse 2s infinite;
}

.badge-enterprise {
  background: linear-gradient(135deg, #FF1493, #FF69B4);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  animation: pulse-enterprise 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes pulse-enterprise {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.btn-user-profile:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(183, 0, 255, 0.5);
  transform: translateY(-2px);
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1.05rem;
  transition: background 0.3s;
}
.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .nav-sections {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .nav-menu {
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .logo h1 {
    font-size: 1.4rem;
  }

  .nav-actions {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
