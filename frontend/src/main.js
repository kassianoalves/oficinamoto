import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router.js'

const app = createApp(App)
app.use(router)
app.mount('#app')

// Registrar Service Worker para PWA
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registrado com sucesso:', registration.scope)
        
        // Verificar atualizações
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // Nova versão disponível
              if (confirm('Nova versão disponível! Deseja atualizar?')) {
                window.location.reload()
              }
            }
          })
        })
      })
      .catch((error) => {
        console.log('Falha ao registrar Service Worker:', error)
      })
  })
}

// Verificar se pode instalar PWA
let deferredPrompt
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault()
  deferredPrompt = e
  
  // Mostrar botão de instalação customizado se desejar
  console.log('PWA pode ser instalado')
})

// Detectar quando o PWA foi instalado
window.addEventListener('appinstalled', () => {
  console.log('PWA instalado com sucesso!')
  deferredPrompt = null
})

