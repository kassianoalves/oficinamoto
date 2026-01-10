<template>
  <div id="app" class="app-container">
    <nav v-if="!isAuthPage" class="navbar">
      <div class="logo">
        <!-- <img :src="logoImage" alt="Logo" class="logo-img" /> -->
        <img v-if="siteLogo" :src="siteLogo" alt="Logo" class="logo-img" />
        <div class="logo-text">
          <button v-if="isAdmin" @click="openLogoModal" class="btn-edit-logo" title="Editar logo e nome do site">
            ✏️
          </button>
          <h1>{{ siteName }}</h1>
        </div>
      </div>
      <div class="nav-sections">
        <ul class="nav-menu">
          <!-- Menu Base (todos os usuários autenticados) -->
          <li v-if="isAuthenticated"><router-link to="/">🏠 Home</router-link></li>
          <li v-if="isAuthenticated"><router-link to="/clientes">👥 Clientes</router-link></li>
          <li v-if="isAuthenticated"><router-link to="/manutencoes">📅 Agendamento</router-link></li>
          
          <!-- Menu PRO (PRO e Enterprise) -->
          <li v-if="isAuthenticated && (isPro || isEnterprise)" class="menu-separator">|</li>
          
          <!-- Dropdown Loja (APENAS ENTERPRISE) -->
          <li
            v-if="isAuthenticated && isEnterprise"
            class="dropdown-container"
            @mouseenter="openDropdown"
            @mouseleave="closeDropdown"
          >
            <button class="dropdown-toggle menu-pro" @click="toggleDropdown">🛒 Loja ▼</button>
            <ul class="dropdown-menu" :class="{ show: showDropdown }">
              <li><router-link to="/loja" class="dropdown-item">Loja Principal</router-link></li>
              
              <!-- Submenu Enterprise -->
              <li v-if="isEnterprise" class="dropdown-separator"></li>
              <li v-if="isEnterprise"><router-link to="/fornecedores" class="dropdown-item enterprise">🤝 Fornecedores</router-link></li>
            </ul>
          </li>
        </ul>
        <div class="nav-right">
          <router-link v-if="isAuthenticated" to="/planos" class="menu-plans">💎 Planos</router-link>
          <div class="nav-actions">
          <template v-if="!isAuthenticated">
            <router-link class="nav-btn" to="/login">Login</router-link>
            <router-link class="nav-btn nav-btn-primary" to="/register">Cadastrar</router-link>
          </template>
          <template v-else>
            <button @click="openProfileModal" class="btn-user-profile" :title="`Plano: ${getPlanName()}`">
              <img :src="userData.avatar_thumb || userData.avatar || avatarInitials" alt="Avatar" :class="['user-avatar', avatarBorderClass]" />
              {{ displayName }}
              <span v-if="isPro" class="badge badge-pro">PRO</span>
              <span v-if="isEnterprise" class="badge badge-enterprise">ENTERPRISE</span>
              <span v-if="isFree" class="badge badge-free">GRÁTIS</span>
            </button>
            <button @click="logout" class="btn-logout">Sair</button>
          </template>
          </div>
        </div>
      </div>
    </nav>
    <main :class="['main-content', { 'main-auth': isAuthPage }]">
      <router-view @login="checkAuth" />
    </main>
    <ProfileModal 
      :show="showProfile" 
      :userData="userData"
      @close="showProfile = false"
      @update="handleProfileUpdate"
    />
    <LogoUploadModal
      :show="showLogoModal"
      :currentLogo="siteLogo"
      :siteName="siteName"
      @close="showLogoModal = false"
      @update="handleLogoUpdate"
    />
    <ToastNotification />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/api.js'
import ToastNotification from '@/components/ToastNotification.vue'
import ProfileModal from '@/components/ProfileModal.vue'
import LogoUploadModal from '@/components/LogoUploadModal.vue'
import avatarPlaceholder from '@/assets/avatar-placeholder.svg'
// import logoImage from '@/assets/logo.png'  // Descomente após adicionar logo.png em src/assets/

export default {
  name: 'App',
  components: {
    ToastNotification,
    ProfileModal,
    LogoUploadModal
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isAuthenticated = ref(false)
    const username = ref('')
    const showProfile = ref(false)
    const userData = ref({})
    const userSubscription = ref(null)
    const isPro = ref(false)
    const isEnterprise = ref(false)
    const isFree = ref(false)
    const showDropdown = ref(false)
    const showLogoModal = ref(false)
    const siteLogo = ref('')
    const siteName = ref('Moto Express')
    const isAdmin = computed(() => userData.value.is_admin || false)

    const displayName = computed(() => {
      if (userData.value.first_name && userData.value.last_name) {
        return `${userData.value.first_name} ${userData.value.last_name}`
      }
      return username.value
    })

    const isAuthPage = computed(() => {
      const authPages = ['Login', 'Register', 'ForgotPassword']
      return authPages.includes(route.name)
    })

    const withBust = (url) => {
      if (!url) return url
      const sep = url.includes('?') ? '&' : '?'
      return `${url}${sep}v=${Date.now()}`
    }

    const makeInitialsAvatar = (name) => {
      const initials = (name || '')
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(s => s.charAt(0).toUpperCase())
        .join('') || '?'
      const svg = `
        <svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'>
          <defs>
            <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
              <stop offset='0%' stop-color='#667eea'/>
              <stop offset='100%' stop-color='#764ba2'/>
            </linearGradient>
          </defs>
          <circle cx='32' cy='32' r='32' fill='url(#g)'/>
          <text x='50%' y='54%' text-anchor='middle' dominant-baseline='middle' font-family='Segoe UI, Arial' font-size='26' fill='#fff' font-weight='700'>${initials}</text>
        </svg>`
      return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
    }

    const avatarInitials = computed(() => makeInitialsAvatar(displayName.value || username.value))

    const getPlanName = () => {
      const planName = userSubscription.value?.plan_name
      const names = {
        'free': 'Plano Gratuito',
        'pro': 'Plano PRO',
        'enterprise': 'Plano Enterprise'
      }
      return names[planName] || 'Sem Plano'
    }

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

    const openDropdown = () => {
      showDropdown.value = true
    }

    const closeDropdown = () => {
      showDropdown.value = false
    }

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value
    }

    const carregarSubscricao = async () => {
      try {
        const res = await api.get('/subscription/subscription/')
        const subscription = res.data.results ? res.data.results[0] : (Array.isArray(res.data) ? res.data[0] : res.data)
        
        userSubscription.value = subscription
        const planName = subscription?.plan_name
        
        isPro.value = planName === 'pro'
        isEnterprise.value = planName === 'enterprise'
        isFree.value = planName === 'free'
      } catch (err) {
        console.error('Erro ao carregar subscrição:', err)
        isPro.value = false
        isEnterprise.value = false
        isFree.value = true
      }
    }

    const currentPlan = computed(() => userSubscription.value?.plan_name || 'free')

    const avatarBorderClass = computed(() => {
      if (isEnterprise.value) return 'border-enterprise'
      if (isPro.value) return 'border-pro'
      return 'border-free'
    })

    const openProfileModal = () => {
      showProfile.value = true
    }

    const handleProfileUpdate = (updatedUser) => {
      if (updatedUser.avatar) updatedUser.avatar = withBust(updatedUser.avatar)
      if (updatedUser.avatar_thumb) updatedUser.avatar_thumb = withBust(updatedUser.avatar_thumb)
      userData.value = updatedUser
      username.value = updatedUser.username || updatedUser.email
    }

    const openLogoModal = () => {
      showLogoModal.value = true
    }

    const handleLogoUpdate = (settings) => {
      if (settings.logo_url) {
        siteLogo.value = withBust(settings.logo_url)
      }
      if (settings.site_name) {
        siteName.value = settings.site_name
      }
    }

    const loadSiteSettings = async () => {
      try {
        const res = await api.get('/subscription/site-settings/')
        if (res.data.logo_url) {
          siteLogo.value = res.data.logo_url
        }
        if (res.data.site_name) {
          siteName.value = res.data.site_name
        }
      } catch (err) {
        console.log('Usando configurações padrão')
      }
    }

    const logout = () => {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      isAuthenticated.value = false
      username.value = ''
      userData.value = {}
      userSubscription.value = null
      router.push('/login')
    }

    onMounted(() => {
      checkAuth()
      loadSiteSettings()
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
      isFree,
      showProfile,
      checkAuth,
      openProfileModal,
      handleProfileUpdate,
      logout,
      getPlanName,
      showDropdown,
      openDropdown,
      closeDropdown,
      toggleDropdown
      ,avatarPlaceholder
      ,avatarInitials
      ,avatarBorderClass
      ,currentPlan
      ,isAuthPage      ,showLogoModal
      ,siteLogo
      ,siteName
      ,isAdmin
      ,openLogoModal
      ,handleLogoUpdate      // ,logoImage  // Descomente após adicionar logo.png
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
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-text {
  position: relative;
  display: flex;
  flex-direction: column;
}

.logo-img {
  height: 45px;
  width: auto;
  object-fit: contain;
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 700;
  white-space: nowrap;
}

.btn-edit-logo {
  position: absolute;
  top: -8px;
  right: -8px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  padding: 0;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.2s;
  opacity: 0.9;
  z-index: 10;
}

.btn-edit-logo:hover {
  color: rgba(255, 255, 255, 0.9);
  opacity: 1;
  transform: scale(1.5);
}

.nav-sections {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  position: relative;
  z-index: 1;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 0.5rem;
  align-items: center;
  margin: 0 auto 0 0;
  padding: 0;
  flex-wrap: wrap;
  z-index: 1;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: auto;
}

.nav-menu li {
  list-style: none;
}

.menu-separator {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.8rem;
  padding: 0 0.25rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.55rem 0.9rem;
  border-radius: 6px;
  transition: all 0.3s;
  display: block;
  white-space: nowrap;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.menu-pro {
  background: rgba(255, 215, 0, 0.15);
  border-left: 3px solid #FFD700;
}

.menu-pro:hover {
  background: rgba(255, 215, 0, 0.25);
}

.menu-plans {
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.2), rgba(255, 192, 203, 0.2));
  border-left: 3px solid #FF69B4;
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.55rem 0.9rem;
  border-radius: 6px;
  transition: all 0.3s;
  display: block;
  white-space: nowrap;
}

.menu-plans:hover {
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.3), rgba(255, 192, 203, 0.3));
}

/* Dropdown Menu */
.dropdown-container {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.55rem 0.9rem;
  border-radius: 6px;
  transition: all 0.3s;
  display: block;
  white-space: nowrap;
  background: rgba(255, 215, 0, 0.15);
  border: none;
  border-left: 3px solid #FFD700;
  cursor: pointer;
}

.dropdown-toggle:hover {
  background: rgba(255, 215, 0, 0.25);
  transform: translateY(-2px);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  list-style: none;
  margin: 0.5rem 0 0 0;
  padding: 0.5rem 0;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  min-width: 200px;
  z-index: 1000;
  display: none;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-menu li {
  list-style: none;
}

.dropdown-item {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.6rem 1.2rem;
  display: block;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.15);
  padding-left: 1.4rem;
}

.dropdown-item.enterprise {
  border-left: 3px solid #FF69B4;
  padding-left: 1rem;
}

.dropdown-separator {
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  margin: 0.25rem 0;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: flex-end;
  position: relative;
  z-index: 5;
}

.nav-btn {
  color: white;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.12);
  cursor: pointer;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-btn-primary {
  background: #FFB347;
  color: #2d3748;
  border-color: #FFB347;
  font-weight: 700;
}

.nav-btn-primary:hover {
  background: #FF9F1C;
  border-color: #FF9F1C;
  transform: translateY(-3px);
}

.btn-user-profile {
  background: rgba(195, 123, 236, 0.2);
  border: 2px solid rgba(100, 0, 158, 0);
  color: white;
  padding: 0.65rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.98rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  white-space: nowrap;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255,255,255,0.6);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.15);
}

.user-avatar.placeholder {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.2);
}

.user-avatar.border-free {
  border: 3px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  box-shadow: 0 0 8px rgba(79, 172, 254, 0.5);
}

.user-avatar.border-pro {
  border: 3px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  box-shadow: 0 0 8px rgba(168, 85, 247, 0.5);
}

.user-avatar.border-enterprise {
  border: 3px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
}

.btn-user-profile:hover {
  background: rgba(18, 1, 27, 0.3);
  transform: translateY(-3px);
}

.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.72rem;
  font-weight: bold;
  white-space: nowrap;
  animation: subtle-pulse 2s infinite;
}

.badge-pro {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
}

.badge-enterprise {
  background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
  color: rgb(255, 255, 255);
}

.badge-free {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
}

@keyframes subtle-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

.btn-logout {
  background: rgba(255, 76, 76, 0.2);
  border: 1px solid rgba(255, 76, 76, 0.4);
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.btn-logout:hover {
  background: rgba(255, 76, 76, 0.3);
  border-color: rgba(255, 76, 76, 0.6);
  transform: translateY(-2px);
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.main-auth {
  padding: 0;
  max-width: none;
  margin: 0;
}

@media (max-width: 1024px) {
  .navbar {
    padding: 1rem;
    gap: 1rem;
  }

  .nav-menu {
    gap: 0.4rem;
  }

  .nav-menu a {
    padding: 0.5rem 0.7rem;
    font-size: 0.9rem;
  }

  .logo h1 {
    font-size: 1.4rem;
  }
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem;
  }

  .nav-sections {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .nav-menu {
    gap: 0.3rem;
    flex-wrap: wrap;
    width: 100%;
  }

  .nav-menu a {
    padding: 0.4rem 0.6rem;
    font-size: 0.85rem;
  }

  .logo h1 {
    font-size: 1.2rem;
  }

  .nav-actions {
    width: 100%;
    justify-content: flex-start;
    gap: 0.5rem;
  }

  .btn-user-profile {
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
  }

  .nav-btn {
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
  }

  .main-content {
    padding: 1rem;
  }

  .menu-separator {
    display: none;
  }
}
</style>
