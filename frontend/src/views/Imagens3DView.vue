<template>
  <div class="imagens-3d-container">
    <div class="header">
      <h1>🎨 Imagens 3D das Motos</h1>
      <p class="subtitle">Visualize os modelos 3D das suas motos para um melhor entendimento dos reparos</p>
    </div>

    <!-- Abas: Minhas Imagens / Galeria -->
    <div class="tabs">
      <button
        :class="['tab', { active: abaAtiva === 'minhas' }]"
        @click="abaAtiva = 'minhas'"
      >
        Minhas Imagens
      </button>
      <button
        :class="['tab', { active: abaAtiva === 'adicionar' }]"
        @click="abaAtiva = 'adicionar'"
      >
        + Adicionar Imagem
      </button>
    </div>

    <!-- Aba: Minhas Imagens -->
    <div v-if="abaAtiva === 'minhas'" class="tab-content">
      <div v-if="carregando" class="loading">
        <p>Carregando imagens...</p>
      </div>

      <div v-else-if="imagens.length > 0" class="imagens-grid">
        <div v-for="imagem in imagens" :key="imagem.id" class="imagem-card">
          <div class="imagem-preview">
            <img
              v-if="imagem.imagem_preview"
              :src="imagem.imagem_preview"
              :alt="imagem.titulo"
            />
            <div v-else class="placeholder">
              <p>🎨 3D Model</p>
            </div>
          </div>

          <div class="card-content">
            <h3>{{ imagem.titulo }}</h3>
            <p class="moto-nome">Moto: {{ imagem.moto_nome }}</p>
            <p class="descricao">{{ imagem.descricao }}</p>

            <div class="card-actions">
              <button @click="visualizar3D(imagem)" class="btn-visualizar">
                👁️ Visualizar 3D
              </button>
              <button @click="editarImagem(imagem)" class="btn-editar">
                ✏️ Editar
              </button>
              <button @click="deletarImagem(imagem.id)" class="btn-deletar">
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>Nenhuma imagem 3D cadastrada</p>
        <button @click="abaAtiva = 'adicionar'" class="btn-primary">
          Adicionar a Primeira Imagem
        </button>
      </div>
    </div>

    <!-- Aba: Adicionar Imagem -->
    <div v-if="abaAtiva === 'adicionar'" class="tab-content">
      <div class="form-container">
        <h2>Adicionar Nova Imagem 3D</h2>

        <form @submit.prevent="salvarImagem" class="form">
          <div class="form-group">
            <label for="moto">Selecione a Moto:</label>
            <select v-model="formulario.moto" id="moto" required>
              <option value="">-- Escolha uma moto --</option>
              <option v-for="moto in motos" :key="moto.id" :value="moto.id">
                {{ moto.modelo }} ({{ moto.ano }})
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="titulo">Título:</label>
            <input
              v-model="formulario.titulo"
              type="text"
              id="titulo"
              placeholder="Ex: Vista lateral do motor"
              required
            />
          </div>

          <div class="form-group">
            <label for="descricao">Descrição:</label>
            <textarea
              v-model="formulario.descricao"
              id="descricao"
              placeholder="Descrição da imagem 3D"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="arquivo-3d">Arquivo 3D (GLB/GLTF):</label>
            <input
              type="file"
              id="arquivo-3d"
              accept=".glb,.gltf,.obj,.fbx"
              @change="onFileSelected($event, 'arquivo_3d')"
            />
          </div>

          <div class="form-group">
            <label for="preview">Imagem de Prévia:</label>
            <input
              type="file"
              id="preview"
              accept="image/*"
              @change="onFileSelected($event, 'imagem_preview')"
            />
            <img
              v-if="previewUrl"
              :src="previewUrl"
              alt="Preview"
              class="preview-img"
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-salvar">💾 Salvar</button>
            <button type="button" @click="abaAtiva = 'minhas'" class="btn-cancelar">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Visualizador 3D -->
    <div v-if="modalVisualizar" class="modal">
      <div class="modal-content">
        <button @click="modalVisualizar = false" class="btn-fechar">✕</button>
        <h2>{{ imagemSelecionada.titulo }}</h2>
        <div class="visualizador-3d">
          <iframe
            v-if="imagemSelecionada.arquivo_3d"
            :src="`https://viewer.3dviewer.net/?url=${encodeURIComponent(imagemSelecionada.arquivo_3d)}`"
            width="100%"
            height="500"
            allowfullscreen
          ></iframe>
          <p v-else>Arquivo 3D não disponível</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../api.js';

export default {
  name: 'Imagens3DView',
  setup() {
    const abaAtiva = ref('minhas');
    const imagens = ref([]);
    const motos = ref([]);
    const carregando = ref(false);
    const modalVisualizar = ref(false);
    const imagemSelecionada = ref(null);
    const previewUrl = ref(null);

    const formulario = ref({
      moto: '',
      titulo: '',
      descricao: '',
      arquivo_3d: null,
      imagem_preview: null
    });

    const carregarImagens = async () => {
      carregando.value = true;
      try {
        const response = await api.get('/imagens-3d/');
        imagens.value = response.data.results || response.data;
      } catch (error) {
        console.error('Erro ao carregar imagens:', error);
      } finally {
        carregando.value = false;
      }
    };

    const carregarMotos = async () => {
      try {
        const response = await api.get('/motos/');
        motos.value = response.data.results || response.data;
      } catch (error) {
        console.error('Erro ao carregar motos:', error);
      }
    };

    const onFileSelected = (event, field) => {
      const file = event.target.files[0];
      if (file) {
        formulario.value[field] = file;

        // Mostrar preview para imagem
        if (field === 'imagem_preview') {
          const reader = new FileReader();
          reader.onload = (e) => {
            previewUrl.value = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      }
    };

    const salvarImagem = async () => {
      const formData = new FormData();
      formData.append('moto', formulario.value.moto);
      formData.append('titulo', formulario.value.titulo);
      formData.append('descricao', formulario.value.descricao);
      if (formulario.value.arquivo_3d) {
        formData.append('arquivo_3d', formulario.value.arquivo_3d);
      }
      if (formulario.value.imagem_preview) {
        formData.append('imagem_preview', formulario.value.imagem_preview);
      }

      try {
        await api.post('/imagens-3d/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        alert('✅ Imagem 3D adicionada com sucesso!');
        formulario.value = {
          moto: '',
          titulo: '',
          descricao: '',
          arquivo_3d: null,
          imagem_preview: null
        };
        previewUrl.value = null;
        abaAtiva.value = 'minhas';
        carregarImagens();
      } catch (error) {
        console.error('Erro ao salvar imagem:', error);
        alert('❌ Erro ao salvar imagem. Tente novamente.');
      }
    };

    const visualizar3D = (imagem) => {
      imagemSelecionada.value = imagem;
      modalVisualizar.value = true;
    };

    const editarImagem = (imagem) => {
      alert('Edição ainda não implementada');
    };

    const deletarImagem = async (id) => {
      if (confirm('Tem certeza que deseja deletar esta imagem?')) {
        try {
          await api.delete(`/imagens-3d/${id}/`);
          alert('✅ Imagem deletada com sucesso!');
          carregarImagens();
        } catch (error) {
          console.error('Erro ao deletar imagem:', error);
          alert('❌ Erro ao deletar imagem.');
        }
      }
    };

    onMounted(() => {
      carregarImagens();
      carregarMotos();
    });

    return {
      abaAtiva,
      imagens,
      motos,
      carregando,
      modalVisualizar,
      imagemSelecionada,
      previewUrl,
      formulario,
      carregarImagens,
      carregarMotos,
      onFileSelected,
      salvarImagem,
      visualizar3D,
      editarImagem,
      deletarImagem
    };
  }
};
</script>

<style scoped>
.imagens-3d-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 1.1em;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #ddd;
}

.tab {
  padding: 15px 25px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.tab:hover {
  color: #ff6b35;
}

.tab.active {
  color: #ff6b35;
  border-bottom-color: #ff6b35;
}

.tab-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Grid de Imagens */
.imagens-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.imagem-card {
  background: white;
  border: 2px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.imagem-card:hover {
  border-color: #ff6b35;
  box-shadow: 0 5px 20px rgba(255, 107, 53, 0.1);
  transform: translateY(-5px);
}

.imagem-preview {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.imagem-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  text-align: center;
  color: #999;
}

.card-content {
  padding: 15px;
}

.card-content h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.moto-nome {
  color: #999;
  font-size: 0.9em;
  margin: 0 0 10px 0;
}

.descricao {
  color: #666;
  font-size: 0.9em;
  line-height: 1.5;
  margin-bottom: 10px;
}

.card-actions {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.btn-visualizar,
.btn-editar,
.btn-deletar {
  flex: 1;
  min-width: 80px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.85em;
}

.btn-visualizar {
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  font-weight: bold;
}

.btn-visualizar:hover {
  opacity: 0.9;
  transform: scale(1.02);
}

.btn-editar {
  background: #e7f3ff;
  color: #004085;
}

.btn-editar:hover {
  background: #d1e7f5;
}

.btn-deletar {
  background: #ffe7e7;
  color: #721c24;
}

.btn-deletar:hover {
  background: #f8d7da;
}

/* Formulário */
.form-container {
  background: white;
  padding: 30px;
  border-radius: 12px;
  border: 2px solid #eee;
  max-width: 500px;
  margin: 0 auto;
}

.form-container h2 {
  color: #333;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #ff6b35;
  outline: none;
}

.preview-img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  margin-top: 10px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-salvar,
.btn-cancelar {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}

.btn-salvar {
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
}

.btn-salvar:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.btn-cancelar {
  background: #e9ecef;
  color: #333;
}

.btn-cancelar:hover {
  background: #dee2e6;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.btn-fechar {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #e9ecef;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2em;
}

.btn-fechar:hover {
  background: #dee2e6;
}

.visualizador-3d {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
}

/* Estados */
.loading,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-state p {
  font-size: 1.1em;
  margin-bottom: 20px;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.btn-primary:hover {
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 768px) {
  .imagens-grid {
    grid-template-columns: 1fr;
  }

  .header h1 {
    font-size: 1.8em;
  }

  .form-container {
    max-width: 100%;
  }

  .tabs {
    flex-direction: column;
  }

  .modal-content {
    width: 95%;
    max-height: 90vh;
  }
}
</style>
