<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="logo">
        <h1>Moto Express</h1>
      </div>
      <ul class="nav-menu">
        <li v-if="isAuthenticated"><router-link to="/">Home</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/clientes">Clientes</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/motos">Motos</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/manutencoes">Agendamento</router-link></li>
        <li v-if="!isAuthenticated"><router-link to="/login">🔐 Login</router-link></li>
        <li v-if="!isAuthenticated"><router-link to="/register">📝 Cadastrar</router-link></li>
        <li v-if="isAuthenticated" class="user-menu">
          <span>👤 {{ username }}</span>
          <button @click="logout" class="btn-logout">Sair</button>
        </li>
      </ul>
    </nav>
    <main class="main-content">
      <router-view @login="checkAuth" />
    </main>
    <ToastNotification />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ToastNotification from '@/components/ToastNotification.vue'

export default {
  name: 'App',
  components: {
    ToastNotification
  },
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)
    const username = ref('')

    const checkAuth = () => {
      const token = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      isAuthenticated.value = !!token
      
      if (user) {
        try {
          const userData = JSON.parse(user)
          username.value = userData.username || userData.email
        } catch (e) {
          username.value = ''
        }
      }
    }

    const logout = () => {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      isAuthenticated.value = false
      username.value = ''
      router.push('/login')
    }

    onMounted(() => {
      checkAuth()
      // Verificar autenticação a cada mudança de rota
      router.afterEach(() => {
        checkAuth()
      })
    })

    return {
      isAuthenticated,
      username,
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
  gap: 2rem;
  align-items: center;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
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

.user-menu span {
  font-weight: 500;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
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
