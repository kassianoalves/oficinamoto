<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay" @click="$emit('close')">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>🎨 Editar Logo do Site</h2>
          <button @click="$emit('close')" class="close-btn">&times;</button>
        </div>

        <form @submit.prevent="uploadLogo" class="modal-form">
          <div class="modal-body">
            <div class="logo-section">
              <div class="logo-preview">
                <img :src="logoPreview || currentLogo || placeholderLogo" alt="Logo Preview" />
              </div>
              <div class="logo-controls">
                <label class="logo-upload">
                  📤 Selecionar Nova Logo
                  <input type="file" accept="image/*" @change="onFileChange" />
                </label>
                <div class="logo-hint">
                  <span>Máx. 2MB • Formatos: PNG/SVG/JPG</span>
                  <span v-if="logoInfo">Selecionado: {{ logoInfo }}</span>
                </div>
                <div v-if="logoError" class="logo-error">{{ logoError }}</div>
              </div>
            </div>

            <div class="form-group">
              <label for="site_name">Nome do Site</label>
              <input
                id="site_name"
                v-model="form.site_name"
                type="text"
                placeholder="Nome do seu site"
                maxlength="100"
              />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="loading || !!logoError">
              {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
            <button type="button" class="btn-cancel" @click="$emit('close')" :disabled="loading">
              Cancelar
            </button>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { ref, watch } from 'vue'
import api from '@/api'
import { useToast } from '@/composables/useToast'

export default {
  name: 'LogoUploadModal',
  props: {
    show: Boolean,
    currentLogo: String,
    siteName: String
  },
  emits: ['close', 'update'],
  setup(props, { emit }) {
    const loading = ref(false)
    const error = ref('')
    const logoFile = ref(null)
    const logoPreview = ref('')
    const logoError = ref('')
    const logoInfo = ref('')
    const MAX_FILE_SIZE = 2 * 1024 * 1024 // 2MB
    const { showToast } = useToast()
    
    const form = ref({
      site_name: props.siteName || 'Moto Express'
    })

    const placeholderLogo = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="90" viewBox="0 0 200 90"%3E%3Crect fill="%23f0f0f0" width="200" height="90"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="14" fill="%23999"%3ESua Logo%3C/text%3E%3C/svg%3E'

    watch(() => props.show, (newVal) => {
      if (newVal) {
        form.value.site_name = props.siteName || 'Moto Express'
        logoPreview.value = ''
        logoFile.value = null
        error.value = ''
        logoError.value = ''
        logoInfo.value = ''
      }
    })

    const onFileChange = (event) => {
      const file = event.target.files[0]
      logoError.value = ''
      logoInfo.value = ''
      
      if (!file) {
        logoFile.value = null
        logoPreview.value = ''
        return
      }

      if (!file.type.startsWith('image/')) {
        logoError.value = 'Arquivo inválido. Selecione uma imagem.'
        return
      }

      if (file.size > MAX_FILE_SIZE) {
        const mb = (file.size / (1024 * 1024)).toFixed(2)
        logoError.value = `Imagem muito grande (${mb}MB). Limite: 2MB.`
        return
      }

      logoInfo.value = `${(file.size / (1024 * 1024)).toFixed(2)}MB`
      logoFile.value = file
      logoPreview.value = URL.createObjectURL(file)
    }

    const uploadLogo = async () => {
      loading.value = true
      error.value = ''

      try {
        const formData = new FormData()
        if (form.value.site_name) {
          formData.append('site_name', form.value.site_name)
        }
        if (logoFile.value) {
          formData.append('logo', logoFile.value)
        }

        const response = await api.put('/subscription/site-settings/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        showToast('Logo atualizada com sucesso!', 'success')
        emit('update', response.data.data)
        emit('close')
      } catch (err) {
        console.error('Erro ao atualizar logo:', err)
        let errorMsg = 'Erro ao atualizar logo. Tente novamente.'
        
        if (err.response?.data?.detail) {
          errorMsg = err.response.data.detail
        } else if (err.response?.status === 403) {
          errorMsg = 'Você não tem permissão para editar as configurações do site.'
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
      loading,
      error,
      form,
      logoPreview,
      logoError,
      logoInfo,
      placeholderLogo,
      onFileChange,
      uploadLogo
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
  max-width: 500px;
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
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

.modal-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.logo-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.logo-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  min-height: 120px;
}

.logo-preview img {
  max-width: 100%;
  max-height: 90px;
  object-fit: contain;
}

.logo-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.logo-upload {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.logo-upload:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.logo-upload input {
  display: none;
}

.logo-hint {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.85rem;
  color: #666;
}

.logo-error {
  color: #ef4444;
  font-size: 0.875rem;
  font-weight: 500;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e0e0e0;
  background: #f9fafb;
}

.btn-save,
.btn-cancel {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
}

.btn-cancel:hover:not(:disabled) {
  background: #e5e7eb;
}

.error-message {
  margin: 0 24px 16px;
  padding: 12px;
  background: #fee2e2;
  border: 1px solid #fca5a5;
  border-radius: 6px;
  color: #dc2626;
  font-size: 0.875rem;
}
</style>
