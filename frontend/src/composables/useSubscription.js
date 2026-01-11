import { ref, computed } from 'vue'
import api from '@/api.js'

/**
 * Composable para gerenciar informações de assinatura do usuário
 * Fornece acesso reativo aos dados de plano e permissões
 */
export const useSubscription = () => {
  const userSubscription = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  /**
   * Carrega a assinatura do usuário da API
   */
  const loadSubscription = async () => {
    try {
      isLoading.value = true
      error.value = null
      const res = await api.get('/subscription/subscription/')
      const subscription = res.data.results ? res.data.results[0] : (Array.isArray(res.data) ? res.data[0] : res.data)
      userSubscription.value = subscription
      return subscription
    } catch (err) {
      error.value = err.message
      userSubscription.value = null
      console.error('Erro ao carregar assinatura:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  // Computed properties para verificar o tipo de plano
  const isPro = computed(() => userSubscription.value?.plan_name === 'pro')
  const isEnterprise = computed(() => userSubscription.value?.plan_name === 'enterprise')
  const isFree = computed(() => userSubscription.value?.plan_name === 'free')

  // Verificar se o usuário tem uma feature específica
  const hasFeature = (featureName) => {
    if (!userSubscription.value) return false
    const planDetails = userSubscription.value.plan_details
    if (!planDetails) return false
    
    // Mapear nomes de features para os campos do modelo
    const featureMap = {
      fornecedores: 'has_fornecedores',
      whatsapp: 'has_whatsapp',
      lembretes: 'has_lembretes',
      chat_suporte: 'has_chat_suporte',
      backup_nuvem: 'has_backup_nuvem',
      ia_diagnostico: 'has_ia_diagnostico',
      plano_fidelidade: 'has_plano_fidelidade',
      agendamentos_prioritarios: 'has_agendamentos_prioritarios',
      loja: 'has_loja',
      imagem_3d: 'has_imagem_3d',
      manuais: 'has_manuais',
      app_mobile: 'has_app_mobile'
    }
    
    const fieldName = featureMap[featureName]
    return fieldName ? planDetails[fieldName] : false
  }

  // Verificar limite de recursos
  const checkLimit = (resourceType) => {
    if (!userSubscription.value) return null
    const planDetails = userSubscription.value.plan_details
    if (!planDetails) return null
    
    const limitMap = {
      clientes: 'max_clientes',
      motos: 'max_motos',
      agendamentos: 'max_agendamentos'
    }
    
    return planDetails[limitMap[resourceType]] || null
  }

  // Obter informações do plano atual
  const getPlanInfo = () => {
    return {
      name: userSubscription.value?.plan_name,
      details: userSubscription.value?.plan_details,
      status: userSubscription.value?.status,
      isActive: userSubscription.value?.is_active
    }
  }

  // Menu items disponíveis baseado no plano
  const getMenuItems = () => {
    const baseItems = [
      { name: 'Home', path: '/', icon: '🏠', requireAuth: true },
      { name: 'Clientes', path: '/clientes', icon: '👥', requireAuth: true },
      { name: 'Agendamento', path: '/manutencoes', icon: '📅', requireAuth: true }
    ]

    const proItems = [
      { name: 'Fornecedores', path: '/fornecedores', icon: '🤝', requirePro: true },
      { name: 'Loja', path: '/loja', icon: '🛒', requirePro: true },
      { name: 'Imagens 3D', path: '/imagens-3d', icon: '📸', requirePro: true },
      { name: 'Manuais', path: '/manuais', icon: '📚', requirePro: true }
    ]

    const allItems = [
      ...baseItems,
      ...proItems,
      { name: 'Upgrade', path: '/planos', icon: '💎', requireAuth: true }
    ]

    // Filtrar baseado no plano
    return allItems.filter(item => {
      if (item.requirePro) {
        return isPro.value || isEnterprise.value
      }
      return true
    })
  }

  return {
    userSubscription,
    isLoading,
    error,
    isPro,
    isEnterprise,
    isFree,
    loadSubscription,
    hasFeature,
    checkLimit,
    getPlanInfo,
    getMenuItems
  }
}
