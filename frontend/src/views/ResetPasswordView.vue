<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>🏍️ Moto Express</h1>
      </div>

      <div class="auth-form">
        <h2>Redefinir Senha</h2>
        <p class="help-text">Insira sua nova senha abaixo.</p>
        
        <form @submit.prevent="resetPassword" v-if="!success">
          <div class="form-group">
            <label for="password">Nova Senha:</label>
            <input 
              v-model="form.password" 
              type="password" 
              id="password" 
              placeholder="Mínimo 8 caracteres"
              required
              minlength="8"
            >
          </div>

          <div class="form-group">
            <label for="password_confirm">Confirmar Senha:</label>
            <input 
              v-model="form.password_confirm" 
              type="password" 
              id="password_confirm" 
              placeholder="Confirme sua senha"
              required
              minlength="8"
            >
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Redefinindo...' : 'Redefinir Senha' }}
          </button>
        </form>

        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>

        <div v-if="success" class="success-message">
          <h3>✅ Senha redefinida com sucesso!</h3>
          <p>Você será redirecionado para o login em 3 segundos...</p>
        </div>

        <div class="auth-links">
          <router-link to="/login">Voltar para Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api.js'

export default {
  name: 'ResetPasswordView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const form = ref({
      password: '',
      password_confirm: ''
    })
    const error = ref('')
    const success = ref(false)
    const loading = ref(false)
    const uid = ref('')
    const token = ref('')

    onMounted(() => {
      // Extrair uid e token da URL
      uid.value = route.params.uid
      token.value = route.params.token

      console.log('UID:', uid.value)
      console.log('Token:', token.value)

      if (!uid.value || !token.value) {
        error.value = 'Link de recuperação inválido ou expirado'
      }
    })

    const resetPassword = async () => {
      error.value = ''
      
      if (form.value.password !== form.value.password_confirm) {
        error.value = 'Senhas não conferem'
        return
      }

      if (form.value.password.length < 8) {
        error.value = 'Senha deve ter no mínimo 8 caracteres'
        return
      }

      loading.value = true

      try {
        const response = await api.post('/auth/reset-password/', {
          uid: uid.value,
          token: token.value,
          password: form.value.password,
          password_confirm: form.value.password_confirm
        })

        success.value = true
        
        // Redirecionar após 3 segundos
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      } catch (err) {
        console.error('Erro:', err)
        error.value = err.response?.data?.detail || 
                     err.response?.data?.non_field_errors?.[0] ||
                     'Erro ao redefinir senha. Link pode estar expirado.'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      error,
      success,
      loading,
      resetPassword
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

.auth-form h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  text-align: center;
}

.help-text {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
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
  margin-bottom: 1rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 500;
}

.success-message {
  background: #efe;
  border: 1px solid #cfc;
  color: #3c3;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  text-align: center;
}

.success-message h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.success-message p {
  margin: 0;
  font-size: 0.9rem;
}

.auth-links {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.auth-links a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
}

.auth-links a:hover {
  color: #764ba2;
  text-decoration: underline;
}
</style>
