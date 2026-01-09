// Composable para notificações toast
import { ref } from 'vue'

const notifications = ref([])
let idCounter = 0

export function useToast() {
  const showToast = (message, type = 'info', duration = 3000) => {
    const id = idCounter++
    const notification = {
      id,
      message,
      type, // 'success', 'error', 'warning', 'info'
      duration
    }
    
    notifications.value.push(notification)
    
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    
    return id
  }
  
  const removeToast = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }
  
  const success = (message, duration) => showToast(message, 'success', duration)
  const error = (message, duration) => showToast(message, 'error', duration)
  const warning = (message, duration) => showToast(message, 'warning', duration)
  const info = (message, duration) => showToast(message, 'info', duration)
  
  return {
    notifications,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
}
