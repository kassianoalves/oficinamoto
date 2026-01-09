<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>🏍️ Oficina Moto</h1>
        <p>Sistema de Gerenciamento</p>
      </div>

      <div class="auth-form">
        <h2>Entrar na Conta</h2>
        
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="email">Email:</label>
            <input 
              v-model="form.email" 
              type="email" 
              id="email" 
              placeholder="seu@email.com"
              required
            >
          </div>

          <div class="form-group">
            <label for="password">Senha:</label>
            <input 
              v-model="form.password" 
              type="password" 
              id="password" 
              placeholder="Sua senha"
              required
            >
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>

        <div class="auth-links">
          <router-link to="/forgot-password">Esqueceu a senha?</router-link>
          <span> | </span>
          <router-link to="/register">Criar Conta</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api.js'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const form = ref({
      email: '',
      password: ''
    })
    const error = ref('')
    const loading = ref(false)

    const login = async () => {
      error.value = ''
      loading.value = true

      try {
        const response = await api.post('/auth/login/', form.value)
        
        // Armazenar token no localStorage
        localStorage.setItem('authToken', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        // Redirecionar para home
        router.push('/')
      } catch (err) {
        console.error('Erro:', err)
        error.value = err.response?.data?.email?.[0] || 
                     err.response?.data?.password?.[0] || 
                     err.response?.data?.non_field_errors?.[0] ||
                     'Erro ao fazer login'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      error,
      loading,
      login
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.auth-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-size: 2rem;
  color: #667eea;
  margin: 0;
}

.auth-header p {
  color: #999;
  margin: 0.5rem 0 0 0;
}

.auth-form h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  margin: 1rem 0;
  text-align: center;
}

.auth-links {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.auth-links a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s;
}

.auth-links a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.auth-links span {
  margin: 0 0.5rem;
  color: #ddd;
}

@media (max-width: 600px) {
  .auth-box {
    margin: 1rem;
  }

  .auth-header h1 {
    font-size: 1.5rem;
  }
}
</style>
