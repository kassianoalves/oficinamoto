import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ClientesView from '@/views/ClientesView.vue'
import MotosView from '@/views/MotosView.vue'
import ManutencaoView from '@/views/ManutencaoView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: ClientesView
  },
  {
    path: '/motos',
    name: 'Motos',
    component: MotosView
  },
  {
    path: '/manutencoes',
    name: 'Manutenções',
    component: ManutencaoView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
