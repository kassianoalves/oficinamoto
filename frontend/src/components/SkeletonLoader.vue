<template>
  <div class="skeleton-loader">
    <div v-for="n in count" :key="n" class="skeleton-item" :class="variant">
      <div v-if="variant === 'card'" class="skeleton-card">
        <div class="skeleton-header"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line short"></div>
        <div class="skeleton-footer"></div>
      </div>
      <div v-else-if="variant === 'list'" class="skeleton-list">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-content">
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
      <div v-else-if="variant === 'table'" class="skeleton-table">
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
      </div>
      <div v-else class="skeleton-rectangle"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    count: {
      type: Number,
      default: 3
    },
    variant: {
      type: String,
      default: 'card',
      validator: (value) => ['card', 'list', 'table', 'rectangle'].includes(value)
    }
  }
}
</script>

<style scoped>
@keyframes shimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.skeleton-loader {
  display: grid;
  gap: 1.5rem;
  padding: 1rem 0;
}

.skeleton-item {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.skeleton-header {
  height: 24px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  border-radius: 4px;
  margin-bottom: 1rem;
  width: 60%;
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.skeleton-line.short {
  width: 40%;
}

.skeleton-footer {
  height: 40px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  border-radius: 8px;
  margin-top: 1rem;
}

.skeleton-list {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.skeleton-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  flex-shrink: 0;
}

.skeleton-content {
  flex: 1;
}

.skeleton-table {
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.skeleton-rectangle {
  height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  border-radius: 8px;
}

/* Tablet - 768px e abaixo */
@media (max-width: 768px) {
  .skeleton-loader {
    gap: 1rem;
    padding: 0.75rem 0;
  }

  .skeleton-card {
    padding: 1rem;
    border-radius: 8px;
  }

  .skeleton-header {
    height: 20px;
    margin-bottom: 0.75rem;
  }

  .skeleton-line {
    height: 14px;
    margin-bottom: 0.5rem;
  }

  .skeleton-footer {
    height: 36px;
    margin-top: 0.75rem;
  }

  .skeleton-list {
    padding: 0.75rem;
    gap: 0.75rem;
  }

  .skeleton-avatar {
    width: 48px;
    height: 48px;
  }

  .skeleton-rectangle {
    height: 150px;
  }
}

/* Smartphone pequeno - 480px e abaixo */
@media (max-width: 480px) {
  .skeleton-loader {
    gap: 0.75rem;
  }

  .skeleton-card {
    padding: 0.75rem;
    border-radius: 6px;
  }

  .skeleton-header {
    height: 18px;
    margin-bottom: 0.5rem;
  }

  .skeleton-line {
    height: 12px;
    margin-bottom: 0.4rem;
  }

  .skeleton-footer {
    height: 32px;
    margin-top: 0.5rem;
  }

  .skeleton-list {
    padding: 0.6rem;
    gap: 0.6rem;
  }

  .skeleton-avatar {
    width: 40px;
    height: 40px;
  }

  .skeleton-rectangle {
    height: 120px;
  }
}
</style>
