<template>
  <Teleport to="body">
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>Editar Perfil</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>

        <form @submit.prevent="updateProfile" class="modal-form">
          <div class="modal-body">
          <div class="avatar-section">
            <div class="avatar-preview" :class="{ 'has-avatar': avatarPreview || userData.avatar }">
              <img :src="avatarPreview || userData.avatar || avatarInitials" alt="Avatar" />
            </div>
            <div class="avatar-controls">
              <label class="avatar-upload">
                Trocar foto
                <input type="file" accept="image/*" @change="onFileChange" />
              </label>
              <div class="avatar-hint">
                <span>Máx. 3MB • Formatos: JPG/PNG/WEBP</span>
                <span v-if="avatarInfo">Selecionado: {{ avatarInfo }}</span>
              </div>
              <div v-if="avatarError" class="avatar-error">{{ avatarError }}</div>
            </div>
          </div>

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
            <div v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</div>
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
              @input="form.telefone = formatTelefone(form.telefone)"
              type="tel"
              placeholder="(11) 99999-9999"
              maxlength="20"
            />
            <div v-if="fieldErrors.telefone" class="field-error">{{ fieldErrors.telefone }}</div>
          </div>

          </div>
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="loading || !!avatarError || !!fieldErrors.email || !!fieldErrors.telefone">
              {{ loading ? 'Salvando...' : 'Salvar' }}
            </button>
            <button type="button" class="btn-cancel" @click="closeModal" :disabled="loading">
              Cancelar
            </button>
            <button type="button" class="btn-logout" @click="$emit('logout')" :disabled="loading">
              Sair
            </button>
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { ref, watch, computed } from 'vue'
import api from '@/api'
import { useToast } from '@/composables/useToast'
import { makeInitialsAvatar, withCacheBust } from '@/utils/avatarUtils'
import { formatTelefone } from '@/utils/formatters'
import { authStorage } from '@/utils/authStorage.js'

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
  emits: ['close', 'update', 'logout'],
  setup(props, { emit }) {
    const showModal = computed(() => props.show)
    const loading = ref(false)
    const error = ref('')
    const avatarFile = ref(null)
    const avatarPreview = ref('')
    const avatarError = ref('')
    const avatarInfo = ref('')
    const MAX_FILE_SIZE = 3 * 1024 * 1024
    const { showToast } = useToast()
    const fieldErrors = ref({ email: '', telefone: '' })
    const avatarInitials = ref('')

    const form = ref({
      first_name: props.userData.first_name || '',
      last_name: props.userData.last_name || '',
      email: props.userData.email || '',
      idade: props.userData.idade || null,
      telefone: props.userData.telefone || ''
    })

    // Funções de utilidade importadas de utils/
    // makeInitialsAvatar, withCacheBust, formatTelefone

    watch(
      () => props.show,
      (newVal) => {
        if (newVal) {
          form.value = {
            first_name: props.userData.first_name || '',
            last_name: props.userData.last_name || '',
            email: props.userData.email || '',
            idade: props.userData.idade || null,
            telefone: props.userData.telefone || ''
          }
          avatarPreview.value = ''
          error.value = ''
          const name = `${props.userData.first_name || ''} ${props.userData.last_name || ''}`.trim() || props.userData.username || props.userData.email || ''
          avatarInitials.value = makeInitialsAvatar(name)
        }
      },
      { immediate: true }
    )

    const closeModal = () => {
      emit('close')
    }

    const updateProfile = async () => {
      loading.value = true
      error.value = ''
      // Validações simples de campos
      fieldErrors.value.email = ''
      fieldErrors.value.telefone = ''
      if (form.value.email && !/^\S+@\S+\.\S+$/.test(form.value.email)) {
        fieldErrors.value.email = 'Email inválido'
      }
      const telDigits = (form.value.telefone || '').replace(/\D/g, '')
      if (telDigits && !(telDigits.length === 10 || telDigits.length === 11)) {
        fieldErrors.value.telefone = 'Telefone deve ter 10 ou 11 dígitos'
      }
      if (fieldErrors.value.email || fieldErrors.value.telefone || avatarError.value) {
        loading.value = false
        return
      }

      try {
        // Usar FormData para enviar imagem + campos
        const formData = new FormData()
        if (form.value.first_name) formData.append('first_name', form.value.first_name)
        if (form.value.last_name) formData.append('last_name', form.value.last_name)
        if (form.value.email) formData.append('email', form.value.email)
        if (form.value.idade) formData.append('idade', form.value.idade)
        if (form.value.telefone) formData.append('telefone', form.value.telefone)
        if (avatarFile.value) formData.append('avatar', avatarFile.value)

        const response = await api.put('/auth/user/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        console.log('Resposta recebida:', response.data)
        // Cache bust nas URLs do avatar
        const updated = { ...response.data }
        if (updated.avatar) updated.avatar = withCacheBust(updated.avatar)
        if (updated.avatar_thumb) updated.avatar_thumb = withCacheBust(updated.avatar_thumb)

        authStorage.setUser(updated)
        showToast('Perfil atualizado com sucesso!', 'success')
        emit('update', updated)
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

    const onFileChange = (event) => {
      const file = event.target.files[0]
      avatarError.value = ''
      avatarInfo.value = ''
      if (!file) {
        avatarFile.value = null
        avatarPreview.value = ''
        return
      }
      if (!file.type || !file.type.startsWith('image/')) {
        avatarError.value = 'Arquivo inválido. Selecione uma imagem.'
        return
      }
      if (file.size > MAX_FILE_SIZE) {
        const mb = (file.size / (1024 * 1024)).toFixed(2)
        avatarError.value = `Imagem muito grande (${mb}MB). Limite: 3MB.`
        return
      }
      avatarInfo.value = `${(file.size / (1024 * 1024)).toFixed(2)}MB`
      // Redimensionar para 256x256 no cliente para reduzir tamanho
      resizeImageToSquare(file, 256)
        .then((resized) => {
          avatarFile.value = resized.blob
          avatarPreview.value = resized.dataUrl
        })
        .catch(() => {
          // Fallback para arquivo original
          avatarFile.value = file
          avatarPreview.value = URL.createObjectURL(file)
        })
    }

    const resizeImageToSquare = (file, size = 256) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => {
          const img = new Image()
          img.onload = () => {
            const canvas = document.createElement('canvas')
            canvas.width = size
            canvas.height = size
            const ctx = canvas.getContext('2d')
            if (!ctx) return reject(new Error('Canvas não suportado'))

            // Crop central quadrado
            const w = img.width
            const h = img.height
            const minSide = Math.min(w, h)
            const sx = (w - minSide) / 2
            const sy = (h - minSide) / 2

            ctx.drawImage(img, sx, sy, minSide, minSide, 0, 0, size, size)

            canvas.toBlob(
              (blob) => {
                if (!blob) return reject(new Error('Falha ao gerar imagem'))
                const dataUrl = canvas.toDataURL('image/jpeg', 0.85)
                // Preservar nome base
                const baseName = (file.name || 'avatar').replace(/\.[^/.]+$/, '')
                const finalBlob = new File([blob], `${baseName}.jpg`, { type: 'image/jpeg' })
                resolve({ blob: finalBlob, dataUrl })
              },
              'image/jpeg',
              0.85
            )
          }
          img.onerror = () => reject(new Error('Imagem inválida'))
          img.src = reader.result
        }
        reader.onerror = () => reject(new Error('Falha ao ler arquivo'))
        reader.readAsDataURL(file)
      })
    }

    return {
      showModal,
      loading,
      error,
      form,
      avatarPreview,
      avatarError,
      avatarInfo,
      avatarInitials,
      avatarPlaceholder: '', // Não mais necessário
      fieldErrors,
      closeModal,
      updateProfile,
      onFileChange,
      resizeImageToSquare,
      formatTelefone  // Importado de utils/formatters.js
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
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 92%;
  max-width: 560px;
  max-height: 86vh;
  display: flex;
  flex-direction: column;
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
  display: flex;
  flex-direction: column;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
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
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar-preview {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 2px solid #e5e7eb;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 2rem;
  color: #9ca3af;
}

.avatar-controls {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.avatar-upload {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 0.55rem 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(118, 75, 162, 0.3);
}

.avatar-upload input {
  display: none;
}

.avatar-hint {
  display: flex;
  gap: 8px;
  color: #6b7280;
  font-size: 0.85rem;
}

.avatar-error {
  color: #c62828;
  background: #ffebee;
  border-left: 4px solid #f44336;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.admin-section {
  margin-top: 24px;
  padding: 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
}

.admin-header {
  margin-bottom: 12px;
}

.admin-badge {
  display: inline-block;
  padding: 6px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}

.btn-edit-logo {
  width: 100%;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit-logo:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.form-actions {
  display: flex;
  gap: 10px;
  padding: 12px 20px;
  border-top: 1px solid #e6e6e6;
  background: #fafafa;
  position: sticky;
  bottom: 0;
}

.btn-save,
.btn-cancel,
.btn-logout {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #5568d3;
}

.btn-save:disabled {
  opacity: 0.9;
  cursor: not-allowed;
}

.btn-cancel {
  background: #fbff00b9;
  color: #333;
}

.btn-cancel:hover:not(:disabled) {
  background: #fbff00;
}

.btn-logout {
  background: #ff0026bb;
  color: #ffffff;
}

.btn-logout:hover:not(:disabled) {
  background: #ff0019;
}

.btn-logout:disabled {
  opacity: 0.9;
  cursor: not-allowed;
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
