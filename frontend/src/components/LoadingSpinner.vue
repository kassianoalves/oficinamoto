<template>
  <div class="loading-spinner-overlay" v-if="overlay" @click="handleClick">
    <div class="spinner-container" :class="size">
      <div class="spinner" :style="spinnerStyle"></div>
      <p v-if="message" class="loading-message">{{ message }}</p>
    </div>
  </div>
  <div v-else class="spinner-inline" :class="size">
    <div class="spinner" :style="spinnerStyle"></div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    overlay: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    message: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: '#667eea'
    }
  },
  computed: {
    spinnerStyle() {
      return {
        borderTopColor: this.color
      }
    }
  },
  methods: {
    handleClick(e) {
      if (e.target.classList.contains('loading-spinner-overlay')) {
        this.$emit('close')
      }
    }
  }
}
</script>

<style scoped>
.loading-spinner-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.spinner-container {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
}

.spinner {
  border-radius: 50%;
  border-style: solid;
  border-color: #f3f3f3;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
}

.small .spinner {
  width: 24px;
  height: 24px;
  border-width: 3px;
}

.medium .spinner {
  width: 48px;
  height: 48px;
  border-width: 4px;
}

.large .spinner {
  width: 72px;
  height: 72px;
  border-width: 6px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-message {
  margin: 0;
  color: #2d3748;
  font-size: 0.95rem;
  font-weight: 500;
  text-align: center;
}

.loading-spinner-overlay .loading-message {
  color: #4a5568;
}

/* Tablet - 768px e abaixo */
@media (max-width: 768px) {
  .loading-spinner-overlay {
    inset: 0;
  }

  .spinner-container {
    padding: 1.5rem;
    border-radius: 12px;
    gap: 0.75rem;
    max-width: 90%;
  }

  .spinner-inline {
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .small .spinner {
    width: 20px;
    height: 20px;
    border-width: 2px;
  }

  .medium .spinner {
    width: 40px;
    height: 40px;
    border-width: 3px;
  }

  .large .spinner {
    width: 60px;
    height: 60px;
    border-width: 5px;
  }

  .loading-message {
    font-size: 0.85rem;
  }
}

/* Smartphone pequeno - 480px e abaixo */
@media (max-width: 480px) {
  .spinner-container {
    padding: 1.25rem;
    border-radius: 10px;
    gap: 0.5rem;
    max-width: 95%;
  }

  .spinner-inline {
    gap: 0.4rem;
    padding: 0.5rem;
  }

  .small .spinner {
    width: 18px;
    height: 18px;
    border-width: 2px;
  }

  .medium .spinner {
    width: 36px;
    height: 36px;
    border-width: 3px;
  }

  .large .spinner {
    width: 48px;
    height: 48px;
    border-width: 4px;
  }

  .loading-message {
    font-size: 0.8rem;
  }
}
</style>
