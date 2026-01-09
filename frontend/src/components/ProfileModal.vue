<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h2>Editar Perfil</h2>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>

      <form @submit.prevent="updateProfile" class="modal-form">
        <div class="form-group">
          <label for="first_name">Nome</label>
          <input
            id="first_name"
            v-model="form.first_name"
            type="text"
            placeholder="Seu nome"
            maxlength="150"
          />
        </div>

        <div class="form-group">
          <label for="last_name">Sobrenome</label>
          <input
            id="last_name"
            v-model="form.last_name"
            type="text"
            placeholder="Seu sobrenome"
            maxlength="150"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="seu.email@example.com"
          />
        </div>

        <div class="form-group">
          <label for="idade">Idade</label>
          <input
            id="idade"
            v-model.number="form.idade"
            type="number"
            min="1"
            max="150"
            placeholder="Sua idade"
          />
        </div>

        <div class="form-group">
          <label for="telefone">Telefone</label>
          <input
            id="telefone"
            v-model="form.telefone"
            type="tel"
            placeholder="(11) 99999-9999"
            maxlength="20"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-save" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar' }}
          </button>
          <button type="button" class="btn-cancel" @click="closeModal" :disabled="loading">
            Cancelar
          </button>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import api from '@/api'
import { useToast } from '@/composables/useToast'

export default {
  name: 'ProfileModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    userData: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['close', 'update'],
  setup(props, { emit }) {
    const showModal = ref(props.show)
    const loading = ref(false)
    const error = ref('')
    const { showToast } = useToast()

    const form = ref({
      first_name: props.userData.first_name || '',
      last_name: props.userData.last_name || '',
      email: props.userData.email || '',
      idade: props.userData.idade || null,
      telefone: props.userData.telefone || ''
    })

    watch(
      () => props.show,
      (newVal) => {
        showModal.value = newVal
        if (newVal) {
          form.value = {
            first_name: props.userData.first_name || '',
            last_name: props.userData.last_name || '',
            email: props.userData.email || '',
            idade: props.userData.idade || null,
            telefone: props.userData.telefone || ''
          }
          error.value = ''
        }
      }
    )

    const closeModal = () => {
      showModal.value = false
      emit('close')
    }

    const updateProfile = async () => {
      loading.value = true
      error.value = ''

      try {
        // Preparar dados para envio (remover campos vazios)
        const dataToSend = {}
        if (form.value.first_name) dataToSend.first_name = form.value.first_name
        if (form.value.last_name) dataToSend.last_name = form.value.last_name
        if (form.value.email) dataToSend.email = form.value.email
        if (form.value.idade) dataToSend.idade = form.value.idade
        if (form.value.telefone) dataToSend.telefone = form.value.telefone

        console.log('Enviando dados:', dataToSend)
        
        const response = await api.put('/auth/user/', dataToSend)
        console.log('Resposta recebida:', response.data)
        
        localStorage.setItem('user', JSON.stringify(response.data))
        showToast('Perfil atualizado com sucesso!', 'success')
        emit('update', response.data)
        closeModal()
      } catch (err) {
        console.error('Erro completo:', err)
        console.error('Response data:', err.response?.data)
        console.error('Status:', err.response?.status)
        
        let errorMsg = 'Erro ao atualizar perfil. Tente novamente.'
        
        if (err.response?.data?.email?.[0]) {
          errorMsg = err.response.data.email[0]
        } else if (err.response?.data?.idade?.[0]) {
          errorMsg = err.response.data.idade[0]
        } else if (err.response?.data?.detail) {
          errorMsg = err.response.data.detail
        } else if (err.response?.status === 401) {
          errorMsg = 'Autenticação expirada. Faça login novamente.'
        } else if (err.message) {
          errorMsg = err.message
        }
        
        error.value = errorMsg
        showToast(error.value, 'error')
      } finally {
        loading.value = false
      }
    }

    return {
      showModal,
      loading,
      error,
      form,
      closeModal,
      updateProfile
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #000;
}

.modal-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-save,
.btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #5568d3;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
}

.btn-cancel:hover:not(:disabled) {
  background: #e0e0e0;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background: #ffebee;
  border-left: 4px solid #f44336;
  color: #c62828;
  border-radius: 4px;
  font-size: 0.9rem;
}
</style>
