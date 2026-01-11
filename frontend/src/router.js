import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ClientesView from '@/views/ClientesView.vue'
import ManutencaoView from '@/views/ManutencaoView.vue'
import PecasView from '@/views/PecasView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ForgotPasswordView from '@/views/ForgotPasswordView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import PlansView from '@/views/PlansView.vue'
import FornecedoresView from '@/views/FornecedoresView.vue'
import LojaView from '@/views/LojaView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPasswordView,
    meta: { requiresAuth: false }
  },
  {
    path: '/reset-password/:uid/:token',
    name: 'ResetPassword',
    component: ResetPasswordView,
    meta: { requiresAuth: false }
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: ClientesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/manutencoes',
    name: 'Agendamento',
    component: ManutencaoView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pecas',
    name: 'Peças',
    component: PecasView,
    meta: { requiresAuth: true }
  },
  {
    path: '/planos',
    name: 'Upgrade',
    component: PlansView,
    meta: { requiresAuth: true }
  },
  {
    path: '/fornecedores',
    name: 'Fornecedores',
    component: FornecedoresView,
    meta: { requiresAuth: true }
  },
  {
    path: '/loja',
    name: 'Loja',
    component: LojaView,
    meta: { requiresAuth: true }
  }
]

import { authStorage } from './utils/authStorage.js'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de autenticação
router.beforeEach((to, from, next) => {
  const isAuthenticated = authStorage.isAuthenticated()
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (!to.meta.requiresAuth && isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
    next('/')
  } else {
    next()
  }
})

export default router
