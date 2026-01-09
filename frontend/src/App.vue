<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="logo">
        <h1>Moto Express</h1>
      </div>
      <ul class="nav-menu">
        <li v-if="isAuthenticated"><router-link to="/">🏠 Home</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/clientes">👥 Clientes</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/manutencoes">🔧 Agendamento</router-link></li>
        <li v-if="!isAuthenticated"><router-link to="/login">🔐 Login</router-link></li>
        <li v-if="!isAuthenticated"><router-link to="/register">📝 Cadastrar</router-link></li>
        <li v-if="isAuthenticated" class="user-menu">
          <button @click="openProfileModal" class="btn-user-profile">
            👤 {{ displayName }}
          </button>
          <button @click="logout" class="btn-logout">🚪 Sair</button>
        </li>
      </ul>
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

    const displayName = computed(() => {
      if (userData.value.first_name && userData.value.last_name) {
        return `${userData.value.first_name} ${userData.value.last_name}`
      }
      return username.value
    })

    const checkAuth = () => {
      const token = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      isAuthenticated.value = !!token
      
      if (user) {
        try {
          userData.value = JSON.parse(user)
          username.value = userData.value.username || userData.value.email
        } catch (e) {
          username.value = ''
        }
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
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 700;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 1rem;
  align-items: center;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.05rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-user-profile {
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 1.05rem;
}

.btn-user-profile:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
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
    gap: 1rem;
  }

  .nav-menu {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .logo h1 {
    font-size: 1.4rem;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
