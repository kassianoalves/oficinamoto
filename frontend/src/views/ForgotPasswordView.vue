<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <h1>🏍️ Moto Express</h1>
      </div>

      <div class="auth-form">
        <h2>Recuperação de Senha</h2>
        <p class="help-text">Insira seu email cadastrado para receber um link de recuperação.</p>
        
        <form @submit.prevent="sendReset">
          <div class="form-group">
            <label for="email">Email:</label>
            <input 
              v-model="email" 
              type="email" 
              id="email" 
              placeholder="seu@email.com"
              required
            >
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Enviando...' : 'Enviar Email de Recuperação' }}
          </button>
        </form>

        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>

        <div v-if="success" class="success-message">
          ✅ Email enviado com sucesso! Verifique sua caixa de entrada.
        </div>

        <div class="auth-links">
          <router-link to="/login">Voltar para Login</router-link>
        </div>
      </div>

      <div v-if="showConsoleMessage" class="console-message">
        <h3>📧 Email Enviado (Console)</h3>
        <p>Em desenvolvimento, os emails aparecem no console do terminal do Django.</p>
        <p>Para produção, configure um servidor SMTP real.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '@/api.js'

export default {
  name: 'ForgotPasswordView',
  setup() {
    const email = ref('')
    const error = ref('')
    const success = ref(false)
    const loading = ref(false)
    const showConsoleMessage = ref(false)

    const sendReset = async () => {
      error.value = ''
      success.value = false
      loading.value = true

      try {
        const response = await api.post('/auth/forgot-password/', { email: email.value })
        
        success.value = true
        showConsoleMessage.value = true
        email.value = ''
        
        // Mostrar mensagem por mais tempo
        setTimeout(() => {
          showConsoleMessage.value = false
        }, 10000)
      } catch (err) {
        console.error('Erro:', err)
        error.value = err.response?.data?.email?.[0] || 
                     err.response?.data?.detail || 
                     'Erro ao enviar email'
      } finally {
        loading.value = false
      }
    }

    return {
      email,
      error,
      success,
      loading,
      showConsoleMessage,
      sendReset
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

.auth-header p {
  color: #999;
  margin: 0.5rem 0 0 0;
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

.success-message {
  background: #efe;
  color: #3c3;
  padding: 0.75rem;
  border-radius: 6px;
  margin: 1rem 0;
  text-align: center;
}

.console-message {
  background: #f0f0f0;
  border-left: 4px solid #667eea;
  padding: 1rem;
  margin-top: 1.5rem;
  border-radius: 6px;
  font-size: 0.85rem;
}

.console-message h3 {
  margin: 0 0 0.5rem 0;
  color: #667eea;
}

.console-message p {
  margin: 0.3rem 0;
  color: #666;
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

@media (max-width: 600px) {
  .auth-box {
    margin: 1rem;
  }

  .auth-header h1 {
    font-size: 1.5rem;
  }
}
</style>
