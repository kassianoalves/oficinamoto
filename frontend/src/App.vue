<template>
  <div id="app" class="app-container">
    <nav v-if="!isAuthPage" class="navbar">
      <!-- Botão Hambúrguer Mobile -->
      <button class="hamburger-btn" @click="toggleMobileMenu" :class="{ active: showMobileMenu }">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div class="logo">
        <img v-if="siteLogo" :src="siteLogo" alt="Logo" class="logo-img" />
        <div class="logo-text">
          <button v-if="isAdmin" @click="openLogoModal" class="btn-edit-logo" title="Editar logo e nome do site">
            ✏️
          </button>
          <h1>{{ siteName }}</h1>
        </div>
      </div>
      <div class="nav-sections desktop-menu">
        <ul class="nav-menu">
          <!-- Menu Base (todos os usuários autenticados) -->
          <li v-if="isAuthenticated"><router-link to="/">🏠 Home</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)" class="menu-separator">|</li>
          <li v-if="isAuthenticated"><router-link to="/clientes">👥 Clientes</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)" class="menu-separator">|</li>
          <li v-if="isAuthenticated"><router-link to="/manutencoes">📅 Agendamento</router-link></li>
      
          <!-- Menu PRO (PRO e Enterprise) -->
          <li v-if="isAuthenticated && (isPro || isEnterprise)" class="menu-separator">|</li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/pecas">📦 Estoque</router-link></li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)" class="menu-separator">|</li>
          <li v-if="isAuthenticated && (isPro || isEnterprise)"><router-link to="/loja">🛒 Loja</router-link></li>
          
          <!-- Menu ENTERPRISE -->
          <li v-if="isAuthenticated && isEnterprise" class="menu-separator">|</li>
          <li v-if="isAuthenticated && isEnterprise"><router-link to="/fornecedores">🤝 Fornecedores</router-link></li>
        </ul>
        <div class="nav-right">
          <router-link v-if="isAuthenticated && !isEnterprise" to="/planos" class="menu-plans">💎 Upgrade</router-link>
          
          <!-- Ícone do Carrinho -->
          <button v-if="isAuthenticated && (isPro || isEnterprise)" @click="toggleCarrinho" class="btn-carrinho" title="Meu Carrinho">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1"/>
              <circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            <span v-if="totalItensCarrinho > 0" class="carrinho-badge">{{ totalItensCarrinho }}</span>
          </button>
          
          <div class="nav-actions">
          <template v-if="!isAuthenticated">
            <router-link class="nav-btn" to="/login">Login</router-link>
            <router-link class="nav-btn nav-btn-primary" to="/register">Cadastrar</router-link>
          </template>
          <template v-else>
            <button @click="openProfileModal" :class="['btn-user-profile', profilePlanClass]" :title="`Plano: ${getPlanName()}`">
              <img :src="userData.avatar_thumb || userData.avatar || avatarInitials" alt="Avatar" :class="['user-avatar', avatarBorderClass]" />
              <div class="user-info">
                <span class="user-name">{{ displayName }}</span>
                <span class="user-plan">
                  <span v-if="isPro" class="plan-label plan-pro">PRO</span>
                  <span v-if="isEnterprise" class="plan-label plan-enterprise">ENTERPRISE</span>
                  <span v-if="isFree" class="plan-label plan-basico">BÁSICO</span>
                </span>
              </div>
            </button>
          </template>
          </div>
        </div>
      </div>
      <!-- Sidebar Mobile Menu -->
      <div class="mobile-sidebar-overlay" :class="{ active: showMobileMenu }" @click="closeMobileMenu"></div>
      <div class="mobile-sidebar" :class="{ active: showMobileMenu }">
        <div class="sidebar-header">
          <div class="sidebar-user">
            <template v-if="isAuthenticated">
              <img :src="userData.avatar_thumb || userData.avatar || avatarInitials" alt="Avatar" class="sidebar-avatar" />
              <div class="sidebar-user-info">
                <span class="sidebar-username">{{ displayName }}</span>
                <span v-if="isPro" class="sidebar-badge badge-pro">PRO</span>
                <span v-if="isEnterprise" class="sidebar-badge badge-enterprise">ENTERPRISE</span>
                <span v-if="isFree" class="sidebar-badge badge-free">GRÁTIS</span>
              </div>
            </template>
            <template v-else>
              <span class="sidebar-guest">Bem-vindo!</span>
            </template>
          </div>
          <button class="sidebar-close" @click="closeMobileMenu">✕</button>
        </div>
        
        <nav class="sidebar-nav">
          <template v-if="isAuthenticated">
            <router-link to="/" class="sidebar-link" @click="closeMobileMenu">
              <span class="sidebar-icon">🏠</span>
              Home
            </router-link>
            <router-link to="/clientes" class="sidebar-link" @click="closeMobileMenu">
              <span class="sidebar-icon">👥</span>
              Clientes
            </router-link>
            <router-link to="/manutencoes" class="sidebar-link" @click="closeMobileMenu">
              <span class="sidebar-icon">📅</span>
              Agendamento
            </router-link>
            
            <div v-if="isPro || isEnterprise" class="sidebar-divider"></div>
            
            <router-link v-if="isPro || isEnterprise" to="/pecas" class="sidebar-link sidebar-link-pro" @click="closeMobileMenu">
              <span class="sidebar-icon">📦</span>
              Estoque
              <span class="sidebar-tag">PRO</span>
            </router-link>
            
            <router-link v-if="isPro || isEnterprise" to="/loja" class="sidebar-link sidebar-link-pro" @click="closeMobileMenu">
              <span class="sidebar-icon">🛒</span>
              Loja
              <span class="sidebar-tag">PRO</span>
            </router-link>
            
            <router-link v-if="isEnterprise" to="/fornecedores" class="sidebar-link sidebar-link-enterprise" @click="closeMobileMenu">
              <span class="sidebar-icon">🤝</span>
              Fornecedores
              <span class="sidebar-tag">ENTERPRISE</span>
            </router-link>
            
            <div class="sidebar-divider"></div>
            
            <router-link v-if="!isEnterprise" to="/planos" class="sidebar-link sidebar-link-plans" @click="closeMobileMenu">
              <span class="sidebar-icon">💎</span>
              Upgrade
            </router-link>
            
            <button @click="openProfileModal; closeMobileMenu()" class="sidebar-link sidebar-button">
              <span class="sidebar-icon">⚙️</span>
              Perfil
            </button>
            
            <button @click="logout" class="sidebar-link sidebar-button sidebar-logout">
              <span class="sidebar-icon">🚪</span>
              Sair
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="sidebar-link" @click="closeMobileMenu">
              <span class="sidebar-icon">🔐</span>
              Login
            </router-link>
            <router-link to="/register" class="sidebar-link sidebar-link-primary" @click="closeMobileMenu">
              <span class="sidebar-icon">📝</span>
              Cadastrar
            </router-link>
          </template>
        </nav>
      </div>
    </nav>
    <main :class="['main-content', { 'main-auth': isAuthPage }]">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" @login="checkAuth" />
        </transition>
      </router-view>
    </main>
    
    <!-- Drawer do Carrinho -->
    <CarrinhoDrawer v-if="isAuthenticated && (isPro || isEnterprise)" />
    
    <ProfileModal 
      :show="showProfile" 
      :userData="userData"
      @close="showProfile = false"
      @update="handleProfileUpdate"
      @logout="logout"
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/api.js'
import { authStorage } from '@/utils/authStorage.js'
import ToastNotification from '@/components/ToastNotification.vue'
import ProfileModal from '@/components/ProfileModal.vue'
import LogoUploadModal from '@/components/LogoUploadModal.vue'
import CarrinhoDrawer from '@/components/CarrinhoDrawer.vue'
import { makeInitialsAvatar, withCacheBust } from '@/utils/avatarUtils'
import { useSubscription } from '@/composables/useSubscription'
import { useCarrinho } from '@/composables/useCarrinho.js'
// import logoImage from '@/assets/logo.png'  // Descomente após adicionar logo.png em src/assets/

export default {
  name: 'App',
  components: {
    ToastNotification,
    ProfileModal,
    LogoUploadModal,
    CarrinhoDrawer
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isAuthenticated = ref(false)
    const username = ref('')
    const showProfile = ref(false)
    const userData = ref({})
    const showMobileMenu = ref(false)
    
    // Estado de assinatura centralizado no composable
    const { userSubscription, isPro, isEnterprise, isFree, loadSubscription } = useSubscription()
    
    // Carrinho
    const { totalItens: totalItensCarrinho, carregarCarrinho, toggleDrawer: toggleCarrinho, migrarCarrinhoApoLogin } = useCarrinho()
    
    const showLogoModal = ref(false)
    const siteLogo = ref('')
    const siteName = ref('Moto Express')
    const isAdmin = computed(() => userData.value.is_admin || false)

    const displayName = computed(() => {
      // Prioridade: first_name + last_name > first_name sozinho > username
      if (userData.value.first_name && userData.value.last_name) {
        return `${userData.value.first_name} ${userData.value.last_name}`
      }
      if (userData.value.first_name) {
        return userData.value.first_name
      }
      return username.value
    })

    const isAuthPage = computed(() => {
      const authPages = ['Login', 'Register', 'ForgotPassword']
      return authPages.includes(route.name)
    })

    // Funções de utilidade de avatar importadas de utils/avatarUtils.js

    const avatarInitials = computed(() => makeInitialsAvatar(displayName.value || username.value))

    const getPlanName = () => {
      const planName = userSubscription.value?.plan_name
      const names = {
        'free': 'Plano Básico',
        'pro': 'Plano PRO',
        'enterprise': 'Plano Enterprise'
      }
      return names[planName] || 'Sem Plano'
    }

    const checkAuth = async () => {
      const token = authStorage.getToken()
      const user = authStorage.getUser()
      
      isAuthenticated.value = !!token
      
      if (user) {
        try {
          userData.value = user
          username.value = userData.value.username || userData.value.email
          
          // Carregar subscrição do usuário (state centralizado)
          if (token) {
            await loadSubscription()
            
            // Carregar carrinho e migrar do localStorage se necessário
            await migrarCarrinhoApoLogin()
            await carregarCarrinho()
          }
        } catch (e) {
          console.error('Erro ao fazer parse do usuário:', e)
          username.value = ''
        }
      } else if (!token) {
        // Usuário não logado: carregar carrinho do localStorage
        await carregarCarrinho()
      }
      return isAuthenticated.value
    }

    const currentPlan = computed(() => userSubscription.value?.plan_name || 'free')

    const avatarBorderClass = computed(() => {
      if (isEnterprise.value) return 'border-enterprise'
      if (isPro.value) return 'border-pro'
      return 'border-free'
    })

    const profilePlanClass = computed(() => {
      if (isEnterprise.value) return 'profile-theme-enterprise'
      if (isPro.value) return 'profile-theme-pro'
      return 'profile-theme-basic'
    })

    const openProfileModal = () => {
      showProfile.value = true
    }

    const handleProfileUpdate = (updatedUser) => {
      if (updatedUser.avatar) updatedUser.avatar = withCacheBust(updatedUser.avatar)
      if (updatedUser.avatar_thumb) updatedUser.avatar_thumb = withCacheBust(updatedUser.avatar_thumb)
      userData.value = updatedUser
      username.value = updatedUser.username || updatedUser.email
      
      // Atualizar storage com os dados mais recentes
      authStorage.setUser(updatedUser)
    }

    const openLogoModal = () => {
      showLogoModal.value = true
    }

    const handleLogoUpdate = (settings) => {
      if (settings.logo_url) {
        siteLogo.value = withCacheBust(settings.logo_url)
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
      closeMobileMenu()
      authStorage.clear()
      isAuthenticated.value = false
      username.value = ''
      userData.value = {}
      userSubscription.value = null
      showProfile.value = false
      router.push('/login')
    }

    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value
      if (showMobileMenu.value) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }

    const closeMobileMenu = () => {
      showMobileMenu.value = false
      document.body.style.overflow = ''
    }

    // Watcher para monitorar mudanças no storage (para atualizar menu após login)
    watch(
      () => authStorage.getToken(),
      async (newToken) => {
        if (newToken) {
          await checkAuth()
        }
      }
    )

    onMounted(async () => {
      await checkAuth()
      await loadSiteSettings()
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
      avatarInitials,
      avatarBorderClass,
      profilePlanClass,
      currentPlan,
      isAuthPage,
      showLogoModal,
      siteLogo,
      siteName,
      isAdmin,
      openLogoModal,
      handleLogoUpdate,
      showMobileMenu,
      toggleMobileMenu,
      closeMobileMenu,
      totalItensCarrinho,
      toggleCarrinho
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: content-box;
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

/* ========== MENU HAMBÚRGUER MOBILE ========== */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 28px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  transition: all 0.3s ease;
}

.hamburger-btn span {
  width: 100%;
  height: 3px;
  background: white;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.hamburger-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
}

.hamburger-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}

.mobile-sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mobile-sidebar-overlay.active {
  display: block;
  opacity: 1;
}

.mobile-sidebar {
  position: fixed;
  top: 0;
  left: -320px;
  width: 300px;
  height: 100vh;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  display: block;
}

.mobile-sidebar.active {
  left: 0;
}

.sidebar-header {
  padding: 1.5rem 1rem;
  background: rgba(0, 0, 0, 0.15);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.sidebar-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sidebar-username {
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.sidebar-guest {
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.sidebar-badge {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 8px;
  font-weight: 700;
  width: fit-content;
}

.sidebar-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  transition: all 0.2s;
}

.sidebar-close:hover {
  transform: rotate(90deg);
  opacity: 0.7;
}

.sidebar-nav {
  padding: 1rem 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: white;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
  border-left: 4px solid transparent;
  background: transparent;
  width: 100%;
  text-align: left;
  border-top: none;
  border-right: none;
  border-bottom: none;
  cursor: pointer;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.1);
  border-left-color: white;
  padding-left: 1.75rem;
}

.sidebar-link.router-link-active {
  background: rgba(255, 255, 255, 0.15);
  border-left-color: white;
  font-weight: 600;
}

.sidebar-icon {
  font-size: 1.3rem;
  min-width: 24px;
}

.sidebar-tag {
  margin-left: auto;
  font-size: 0.65rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.2);
  font-weight: 700;
}

.sidebar-link-pro:hover {
  background: rgba(168, 85, 247, 0.2);
}

.sidebar-link-enterprise:hover {
  background: rgba(255, 215, 0, 0.15);
}

.sidebar-link-plans {
  background: rgba(255, 105, 180, 0.1);
}

.sidebar-link-plans:hover {
  background: rgba(255, 105, 180, 0.2);
}

.sidebar-button {
  font-family: inherit;
}

.sidebar-logout {
  color: #ffcccc;
}

.sidebar-logout:hover {
  background: rgba(255, 76, 76, 0.2);
  border-left-color: #ff4c4c;
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.15);
  margin: 0.75rem 1rem;
}

.sidebar-link-primary {
  background: rgba(255, 179, 71, 0.2);
}

.sidebar-link-primary:hover {
  background: rgba(255, 159, 28, 0.3);
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

/* Botão do Carrinho */
.btn-carrinho {
  position: relative;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.5rem 0.7rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 0.5rem;
}

.btn-carrinho:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-carrinho svg {
  width: 22px;
  height: 22px;
  stroke-width: 2.5;
}

.carrinho-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  color: white;
  border-radius: 50%;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0 4px;
  box-shadow: 0 2px 8px rgba(238, 90, 111, 0.4);
  border: 2px solid white;
  animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
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
  /* Variáveis por plano: definidas em profile-theme-* */
  --profile-bg: rgba(195, 123, 236, 0.2);
  --profile-hover: rgba(18, 1, 27, 0.3);
  --profile-border: rgba(255, 255, 255, 0.25);
  --profile-badge-bg: rgba(255, 255, 255, 0.2);
  --profile-badge-color: #fff;

  background: var(--profile-bg);
  border: 2px solid var(--profile-border);
  color: white;
  padding: 0.65rem 1.1rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.98rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  white-space: nowrap;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255,255,255,0.6);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.15);
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.15rem;
  min-width: 0;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.user-plan {
  display: flex;
  align-items: center;
  font-size: 0.7rem;
}

.plan-label {
  padding: 0.15rem 0.5rem;
  border-radius: 8px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.plan-label.plan-free {
  color: #64b5f6;
}

.plan-label.plan-basico {
  background: rgba(100, 181, 246, 0.25);
  color: #a8d8ff;
  border: 1px solid rgba(100, 181, 246, 0.5);
}

.plan-label.plan-pro {
  background: rgb(6, 71, 131);
  color: #00eeff;
  border: 1px solid rgba(0, 89, 255, 0.4);
}

.plan-label.plan-enterprise {
  background: rgba(255, 215, 0, 0.25);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.5);
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
  background-image: linear-gradient(white, white), linear-gradient(135deg, #0004f8 0%, #00ccff 100%);
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
  background: var(--profile-hover);
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

.plan-badge {
  background: var(--profile-badge-bg, rgba(143, 252, 0, 0.2));
  color: var(--profile-badge-color, #fff);
  border: 1px solid var(--profile-border, rgba(255, 255, 255, 0.2));
}

/* Temas do perfil por plano: edite cores de fundo, hover e badge de forma independente */
.profile-theme-basic {
  --profile-bg: rgba(0, 195, 255, 0.336);
  --profile-hover: rgba(0, 68, 255, 0.849);
  --profile-border: rgba(79, 172, 254, 0.45);
  --profile-badge-bg: rgba(151, 151, 151, 0.87);
  --profile-badge-color: #0b3a5c;
}

.profile-theme-pro {
  --profile-bg: rgba(22, 0, 150, 0.678);
  --profile-hover: rgba(0, 60, 255, 0.32);
  --profile-border: rgba(168, 85, 247, 0.5);
  --profile-badge-bg: rgb(41, 31, 36);
  --profile-badge-color: #d609ff;
}

.profile-theme-enterprise {
  --profile-bg: rgba(255, 215, 0, 0.18);
  --profile-hover: rgba(255, 140, 0, 0.3);
  --profile-border: rgba(255, 215, 0, 0.55);
  --profile-badge-bg: rgba(255, 215, 0, 0.2);
  --profile-badge-color: #3d2500;
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
  background: rgba(11, 52, 165, 0.651);
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

/* Transições entre páginas */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Large Desktop - 1366px e abaixo */
@media (max-width: 1366px) {
  .navbar {
    padding: 0.9rem 1.2rem;
  }

  .nav-menu {
    gap: 0.35rem;
  }

  .nav-menu a {
    padding: 0.5rem 0.75rem;
    font-size: 0.92rem;
  }

  .menu-separator {
    padding: 0 0.15rem;
  }

  .nav-right {
    gap: 0.75rem;
  }

  .btn-user-profile {
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
  }
}

/* Tablet - 1024px e abaixo */
@media (max-width: 1024px) {
  .navbar {
    padding: 0.85rem 1rem;
    gap: 0.75rem;
  }

  .nav-menu {
    gap: 0.3rem;
  }

  .nav-menu a {
    padding: 0.45rem 0.65rem;
    font-size: 0.88rem;
  }

  .menu-separator {
    display: none;
  }

  .logo h1 {
    font-size: 1.4rem;
  }

  .nav-right {
    gap: 0.6rem;
  }

  .btn-user-profile {
    padding: 0.55rem 0.9rem;
    font-size: 0.9rem;
  }

  .menu-plans {
    padding: 0.45rem 0.75rem;
    font-size: 0.88rem;
  }

  .main-content {
    padding: 1.5rem;
  }
}

/* Mobile - 768px e abaixo */
@media (max-width: 768px) {
  * {
    -webkit-tap-highlight-color: transparent;
  }

  html, body {
    overflow-x: hidden;
  }

  .app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .navbar {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    padding-top: calc(0.5rem + env(safe-area-inset-top, 0px));
    border-bottom: 2px solid #f0f0f0;
    flex-wrap: nowrap;
    position: relative;
  }

  .logo {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .logo-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.15rem;
  }

  .logo h1 {
    font-size: 1.05rem;
    margin: 0;
    text-align: center;
  }

  .logo-img {
    width: 32px !important;
    height: 32px !important;
  }

  .desktop-menu {
    display: none !important;
  }

  .nav-menu {
    gap: 0.25rem;
    flex-wrap: wrap;
    width: 100%;
    list-style: none;
    padding: 0;
    margin: 0;
    justify-content: center;
  }

  .nav-menu li {
    margin: 0;
  }

  .nav-menu a {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
    display: inline-block;
  }

  .nav-menu li.menu-separator {
    display: none;
  }

  .nav-right {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    order: 2;
  }

  .hamburger-btn {
    display: flex;
    order: -1;
    margin-right: auto;
    z-index: 1;
  }

  .mobile-sidebar {
    display: block;
  }

  .menu-plans {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
  }

  .nav-actions {
    width: 100%;
    justify-content: flex-start;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .btn-user-profile {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
    max-width: 100%;
    gap: 0.4rem;
  }

  .user-name {
    font-size: 0.8rem;
    max-width: 120px;
  }

  .user-plan {
    font-size: 0.65rem;
  }

  .plan-label {
    padding: 0.1rem 0.4rem;
    font-size: 0.6rem;
  }

  .user-avatar {
    width: 24px !important;
    height: 24px !important;
  }

  .nav-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
  }

  .nav-btn-primary {
    padding: 0.4rem 0.8rem;
  }

  .main-content {
    flex: 1;
    padding: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
}

/* Smartphone pequeno - 480px e abaixo */
@media (max-width: 480px) {
  .main-content {
    padding: 0;
  }

  .navbar {
    padding: 0.5rem;
  }

  .logo h1 {
    font-size: 0.95rem;
  }

  .nav-menu a {
    padding: 0.3rem 0.5rem;
    font-size: 0.75rem;
  }

  .menu-plans {
    padding: 0.3rem 0.5rem;
    font-size: 0.75rem;
  }

  .btn-user-profile {
    padding: 0.3rem 0.5rem;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
  }

  .btn-user-profile .user-avatar {
    margin-right: 0.25rem;
  }

  .main-content {
    padding: 0.75rem;
  }

  .nav-sections {
    gap: 0.3rem;
  }

  .nav-right {
    gap: 0.3rem;
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

/* Medium screens - 1280px e abaixo */
@media (max-width: 1280px) {
  .navbar {
    padding: 0.8rem 1rem;
    gap: 0.75rem;
  }
  .nav-sections {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .nav-menu {
    gap: 0.4rem;
  }
  .nav-menu a {
    padding: 0.45rem 0.7rem;
    font-size: 0.9rem;
  }
  .menu-separator {
    display: none;
  }
  .nav-right {
    gap: 0.6rem;
    flex-wrap: wrap;
  }
}
</style>
