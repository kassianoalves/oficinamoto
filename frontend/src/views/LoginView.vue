<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>Moto Express</h1>
      </div>
      <div class="auth-form">

        <h2>Entrar na Conta</h2>

        <form @submit.prevent="login">
          <div class="form-group">
            <label for="login">Login (Email ou Usuário):</label>
            <input
              v-model="form.login"
              type="text"
              id="login"
              placeholder="seu email ou usuário"
              required
            >
          </div>

          <div class="form-group">
            <label for="password">Senha:</label>
            <input
              v-model="form.password"
              type="password"
              id="password"
              placeholder="sua senha"
              required
            >
          </div>

          <div class="form-group checkbox-group">
            <label for="rememberMe" class="checkbox-label">
              <input
                v-model="form.rememberMe"
                type="checkbox"
                id="rememberMe"
              >
              <span>Manter-se logado</span>
            </label>
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
import { authStorage } from '@/utils/authStorage.js'

export default {
  name: 'LoginView',
  emits: ['login'],
  setup(props, { emit }) {
    const router = useRouter()
    const form = ref({
      login: '',
      password: '',
      rememberMe: false
    })
    const error = ref('')
    const loading = ref(false)

    const login = async () => {
      error.value = ''
      loading.value = true

      try {
        const loginValue = form.value.login.trim()
        const payload = {
          password: form.value.password
        }

        // Detectar se é email ou username
        if (loginValue.includes('@')) {
          payload.email = loginValue
        } else {
          payload.username = loginValue
        }

        const response = await api.post('/auth/login/', payload)

        // Definir tipo de armazenamento baseado na checkbox
        authStorage.setStorageType(form.value.rememberMe ? 'local' : 'session')

        // Armazenar token e usuário
        authStorage.setToken(response.data.token)
        authStorage.setUser(response.data.user)

        // Emitir evento para App.vue atualizar imediatamente
        emit('login')

        // Redirecionar para home
        router.push('/')
      } catch (err) {
        console.error('Erro:', err)
        error.value = err.response?.data?.email?.[0] ||
                     err.response?.data?.username?.[0] ||
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
  padding: 1rem;
}

.auth-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 380px;
  padding: 1.8rem 1.5rem;
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
  margin-bottom: 1.5rem;
}

.auth-header h1 {
  font-size: 1.8rem;
  color: #667eea;
  margin: 0;
}

.auth-header p {
  color: #999;
  margin: 0.5rem 0 0 0;
}

.auth-form h2 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 1.2rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: 0.65rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.checkbox-group {
  margin: 1.2rem 0;
  padding: 0;
  display: flex;
  justify-content: center;
}

.checkbox-group label {
  display: flex;
  margin-bottom: 0;
}

.checkbox-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  cursor: pointer;
  font-weight: 500;
  color: #333;
  user-select: none;
  transition: all 0.2s ease;
  padding: 0;
  margin: 0;
  white-space: nowrap;
}

.checkbox-label:hover {
  color: #667eea;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  min-width: 18px;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  border: 2px solid #ddd;
  border-radius: 3px;
  background-color: white;
  position: relative;
  margin: 0;
  padding: 0;
  top: 0;
}

.checkbox-label input[type="checkbox"]:hover {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.checkbox-label input[type="checkbox"]:checked {
  background-color: #667eea;
  border-color: #667eea;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 11-1.06-1.06l7.25-7.25a.75.75 0 011.06 0z'/%3E%3Cpath d='M2.22 9.22a.75.75 0 011.06 0l2.97 2.97a.75.75 0 11-1.06 1.06L2.22 10.28a.75.75 0 010-1.06z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 12px;
}

.checkbox-label input[type="checkbox"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15);
}

.checkbox-label span {
  font-size: 0.95rem;
  letter-spacing: 0.2px;
  margin: 0;
  line-height: 1.2;
}

.btn-submit {
  width: 100%;
  padding: 0.65rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  margin: 1rem 0;
  text-align: center;
  font-weight: 500;
  font-size: 0.9rem;
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

/* Responsivo para Tablets */
@media (max-width: 768px) {
  .auth-container {
    padding: 1.5rem;
  }

  .auth-box {
    max-width: 450px;
    padding: 2rem 1.5rem;
  }

  .auth-header h1 {
    font-size: 1.8rem;
  }

  .auth-form h2 {
    font-size: 1.3rem;
  }
}

/* Responsivo para Smartphones */
@media (max-width: 480px) {
  .auth-container {
    padding: 1rem;
    align-items: flex-start;
    padding-top: 2rem;
  }

  .auth-box {
    max-width: 100%;
    padding: 1.5rem;
    border-radius: 8px;
  }

  .auth-header {
    margin-bottom: 1.5rem;
  }

  .auth-header h1 {
    font-size: 1.5rem;
  }

  .auth-form h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    font-size: 0.9rem;
  }

  .form-group input {
    padding: 0.65rem;
    font-size: 0.95rem;
  }

  .btn-submit {
    padding: 0.65rem;
    font-size: 0.95rem;
  }

  .auth-links {
    margin-top: 1rem;
    font-size: 0.85rem;
  }
}

/* Smartphones pequenos */
@media (max-width: 360px) {
  .auth-box {
    padding: 1rem;
  }

  .auth-header h1 {
    font-size: 1.3rem;
  }

  .auth-form h2 {
    font-size: 1.1rem;
  }
}
</style>
