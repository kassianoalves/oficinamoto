<template>
  <teleport to="body">
    <div class="toast-container">
      <transition-group name="toast">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          :class="['toast', `toast-${notification.type}`]"
          @click="removeToast(notification.id)"
        >
          <div class="toast-icon">
            <span v-if="notification.type === 'success'">✓</span>
            <span v-else-if="notification.type === 'error'">✕</span>
            <span v-else-if="notification.type === 'warning'">⚠</span>
            <span v-else>ℹ</span>
          </div>
          <div class="toast-message">{{ notification.message }}</div>
          <button class="toast-close" @click.stop="removeToast(notification.id)">×</button>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script>
import { useToast } from '@/composables/useToast'

export default {
  name: 'ToastNotification',
  setup() {
    const { notifications, removeToast } = useToast()
    
    return {
      notifications,
      removeToast
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  max-width: 500px;
  pointer-events: all;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toast:hover {
  transform: translateX(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
  flex-shrink: 0;
}

.toast-success {
  border-left: 4px solid #10b981;
}

.toast-success .toast-icon {
  background: #d1fae5;
  color: #065f46;
}

.toast-error {
  border-left: 4px solid #ef4444;
}

.toast-error .toast-icon {
  background: #fee2e2;
  color: #991b1b;
}

.toast-warning {
  border-left: 4px solid #f59e0b;
}

.toast-warning .toast-icon {
  background: #fef3c7;
  color: #92400e;
}

.toast-info {
  border-left: 4px solid #3b82f6;
}

.toast-info .toast-icon {
  background: #dbeafe;
  color: #1e40af;
}

.toast-message {
  flex: 1;
  color: #374151;
  font-size: 14px;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  color: #374151;
}

/* Animações */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.8);
}

@media (max-width: 640px) {
  .toast-container {
    right: 10px;
    left: 10px;
  }
  
  .toast {
    min-width: auto;
  }
}
</style>
