<template>
  <div class="pecas-view">
    <div class="view-header">
      <h2>📦 Inventário de Peças</h2>
      <button @click="showFormPeca = true" class="btn-add">➕ Nova Peça</button>
    </div>

    <!-- Formulário Nova Peça -->
    <div v-if="showFormPeca" class="form-container">
      <form @submit.prevent="salvarPeca">
        <h3>{{ editingPecaId ? 'Editar Peça' : 'Nova Peça' }}</h3>
        <div class="form-grid">
          <input v-model="formPeca.nome" type="text" placeholder="Nome da peça" required>
          <input v-model="formPeca.codigo" type="text" placeholder="Código" required>
          <input v-model.number="formPeca.preco_unitario" type="number" placeholder="Preço" step="0.01" required>
          <input v-model="formPeca.categoria" type="text" placeholder="Categoria (Óleo, Filtro, etc)" required>
          <input v-model.number="formPeca.quantidade" type="number" placeholder="Quantidade em estoque" required>
          <input v-model="formPeca.marca" type="text" placeholder="Marca do produto">
          <input v-model="formPeca.fornecedor" type="text" placeholder="Fornecedor">
        </div>
        <div class="form-full">
          <textarea v-model="formPeca.descricao" placeholder="Descrição da peça"></textarea>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ editingPecaId ? 'Atualizar' : 'Salvar' }}</button>
          <button type="button" @click="resetFormPeca" class="btn btn-secondary">Cancelar</button>
        </div>
      </form>
    </div>

    <!-- Filtro por Categoria -->
    <div class="filter-section">
      <select v-model="filtroCategoria" class="filter-select">
        <option value="">Todas as Categorias</option>
        <option v-for="cat in categorias" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <!-- Lista de Peças -->
    <div v-if="pecasFiltradas.length" class="pecas-grid">
      <div v-for="peca in pecasFiltradas" :key="peca.id" class="peca-card" :class="{ 'baixo-estoque': peca.quantidade <= 5 }">
        <div class="peca-header">
          <h4>{{ peca.nome }}</h4>
          <div class="peca-actions">
            <button @click="editarPeca(peca)" class="btn-icon" title="Editar">✏️</button>
            <button @click="deletarPeca(peca.id)" class="btn-icon" title="Deletar">🗑️</button>
          </div>
        </div>
        
        <!-- Fotos -->
        <div v-if="peca.fotos && peca.fotos.length > 0" class="fotos-section">
          <h5>Fotos ({{ peca.fotos.length }}/2)</h5>
          <div class="fotos-grid">
            <div v-for="(foto, idx) in peca.fotos" :key="foto.id" class="foto-item">
              <img :src="foto.imagem" :alt="`Foto ${idx + 1}`" class="foto-thumb" />
              <button
                @click="removerFoto(peca.id, foto.id)"
                class="btn-remover-foto"
                title="Remover foto"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <!-- Adicionar Fotos -->
        <div v-if="!peca.fotos || peca.fotos.length < 2" class="add-foto-section">
          <label class="label-upload">
            <input
              type="file"
              accept="image/*"
              @change="(e) => adicionarFoto(e, peca.id)"
              style="display: none"
            />
            📸 Adicionar Foto
          </label>
        </div>
        
        <div class="peca-body">
          <p><strong>Código:</strong> {{ peca.codigo }}</p>
          <p><strong>Marca:</strong> <span class="badge">{{ peca.marca }}</span></p>
          <p><strong>Categoria:</strong> <span class="badge">{{ peca.categoria }}</span></p>
          <p><strong>Preço:</strong> R$ {{ formatarMoeda(peca.preco_unitario) }}</p>
          <p :class="{ 'estoque-baixo': peca.quantidade <= 5 }">
            <strong>Estoque:</strong> {{ peca.quantidade }} un.
            <span v-if="peca.quantidade <= 5" class="alerta">⚠️ ATENÇÃO</span>
          </p>
          <p v-if="peca.fornecedor"><strong>Fornecedor:</strong> {{ peca.fornecedor }}</p>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhuma peça cadastrada</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api.js'
import { useToast } from '@/composables/useToast'

export default {
  name: 'PecasView',
  setup() {
    const { success, error } = useToast()
    const pecas = ref([])
    const showFormPeca = ref(false)
    const editingPecaId = ref(null)
    const filtroCategoria = ref('')
    
    const formPeca = ref({
      nome: '',
      descricao: '',
      codigo: '',
      quantidade: 0,
      preco_unitario: 0,
      categoria: '',
      marca: '',
      fornecedor: '',
      ativa: true
    })

    const categorias = computed(() => {
      const cats = new Set(pecas.value.map(p => p.categoria))
      return Array.from(cats).sort()
    })

    const pecasFiltradas = computed(() => {
      if (!filtroCategoria.value) return pecas.value
      return pecas.value.filter(p => p.categoria === filtroCategoria.value)
    })

    const carregarPecas = async () => {
      try {
        const res = await api.get('/pecas/')
        pecas.value = res.data.results || res.data || []
      } catch (err) {
        console.error('Erro ao carregar peças:', err)
        error('Erro ao carregar peças')
      }
    }

    const salvarPeca = async () => {
      try {
        if (editingPecaId.value) {
          await api.put(`/pecas/${editingPecaId.value}/`, formPeca.value)
          success('Peça atualizada!')
        } else {
          await api.post('/pecas/', formPeca.value)
          success('Peça criada!')
        }
        resetFormPeca()
        carregarPecas()
      } catch (err) {
        console.error('Erro ao salvar peça:', err)
        error('Erro ao salvar peça')
      }
    }

    const editarPeca = (peca) => {
      editingPecaId.value = peca.id
      formPeca.value = { ...peca }
      showFormPeca.value = true
    }

    const deletarPeca = async (id) => {
      if (confirm('Deletar esta peça?')) {
        try {
          await api.delete(`/pecas/${id}/`)
          success('Peça deletada!')
          carregarPecas()
        } catch (err) {
          console.error('Erro ao deletar peça:', err)
          error('Erro ao deletar peça')
        }
      }
    }

    const adicionarFoto = async (event, pecaId) => {
      const file = event.target.files[0]
      if (!file) return

      const formData = new FormData()
      formData.append('imagem', file)

      try {
        await api.post(`/pecas/${pecaId}/adicionar_foto/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        success('Foto adicionada!')
        carregarPecas()
        event.target.value = ''
      } catch (err) {
        console.error('Erro ao adicionar foto:', err)
        error('Erro ao adicionar foto. Máximo de 2 fotos por peça.')
      }
    }

    const removerFoto = async (pecaId, fotoId) => {
      if (!confirm('Remover esta foto?')) return

      try {
        await api.delete(`/pecas/${pecaId}/remover_foto/?foto_id=${fotoId}`)
        success('Foto removida!')
        carregarPecas()
      } catch (err) {
        console.error('Erro ao remover foto:', err)
        error('Erro ao remover foto')
      }
    }

    const resetFormPeca = () => {
      formPeca.value = {
        nome: '',
        descricao: '',
        codigo: '',
        quantidade: 0,
        preco_unitario: 0,
        categoria: '',
        marca: '',
        fornecedor: '',
        ativa: true
      }
      editingPecaId.value = null
      showFormPeca.value = false
    }

    const formatarMoeda = (valor) => {
      const n = typeof valor === 'number' ? valor : parseFloat(valor ?? 0)
      if (Number.isNaN(n)) return '0,00'
      return n.toFixed(2).replace('.', ',')
    }

    onMounted(() => {
      carregarPecas()
    })

    return {
      pecas,
      pecasFiltradas,
      showFormPeca,
      editingPecaId,
      formPeca,
      filtroCategoria,
      categorias,
      salvarPeca,
      editarPeca,
      deletarPeca,
      adicionarFoto,
      removerFoto,
      resetFormPeca,
      formatarMoeda,
      carregarPecas
    }
  }
}
</script>

<style scoped>
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-add {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-add:hover {
  transform: translateY(-2px);
}

.form-container {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-full {
  margin-bottom: 1rem;
}

.form-grid input,
.form-full textarea {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-full textarea {
  width: 100%;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
}

.btn {
  border: none;
  padding: 0.7rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #667eea;
  color: white;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #4c51bf;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}

.filter-section {
  margin-bottom: 1.5rem;
}

.filter-select {
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.pecas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.peca-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 0.5rem;
  transition: all 0.2s;
}

.peca-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.peca-card.baixo-estoque {
  border-color: #ff9800;
  background: rgba(255, 152, 0, 0.02);
}

.peca-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 0.3rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #f0f0f0;
  gap: 0.2rem;
}

.peca-header h4 {
  color: #333;
  margin: 0;
  flex: 1;
  word-break: break-word;
  font-size: 0.95rem;
  line-height: 1.2;
}

.peca-actions {
  display: flex;
  gap: 0.12rem;
  margin-left: 0;
  flex-shrink: 0;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 0.2rem;
  min-width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  transform: scale(1.2);
}

/* Fotos */
.fotos-section {
  margin-bottom: 0.6rem;
  padding: 0.6rem;
  background: #f9f9f9;
  border-radius: 6px;
}

.fotos-section h5 {
  margin: 0 0 0.4rem 0;
  color: #333;
  font-size: 0.85rem;
  font-weight: 600;
}

.fotos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin-bottom: 0;
}

.foto-item {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 6px;
  overflow: hidden;
  border: 2px solid #ddd;
  background: #f0f0f0;
}

.foto-thumb {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  padding: 4px;
  box-sizing: border-box;
}

.btn-remover-foto {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  background: rgba(255, 107, 53, 0.95);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.foto-item:hover .btn-remover-foto {
  opacity: 1;
}

.btn-remover-foto:hover {
  background: #e55a24;
  transform: scale(1.1);
}

.add-foto-section {
  margin-bottom: 0.6rem;
}

.label-upload {
  display: block;
  padding: 0.5rem;
  background: white;
  border: 2px dashed #ff6b35;
  border-radius: 4px;
  text-align: center;
  color: #ff6b35;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s;
}

.label-upload:hover {
  background: #fff5f0;
}

.peca-body {
  padding-top: 0;
}

.peca-body p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.2;
}

.peca-body .badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 600;
}

.estoque-baixo {
  color: #ff9800;
  font-weight: 600;
}

.alerta {
  color: #ff5722;
  font-weight: bold;
  margin-left: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .pecas-view {
    padding: 0.5rem;
  }

  .view-header {
    flex-direction: column;
    gap: 0.8rem;
    padding: 0 8px;
  }

  .view-header h2 {
    font-size: 1.5rem;
    margin: 0;
  }

  .btn-add {
    width: 100%;
    padding: 0.7rem;
    font-size: 0.95rem;
  }

  .filter-section {
    padding: 0 8px 1rem;
  }

  .filter-select {
    width: 100%;
    padding: 0.7rem;
    font-size: 0.95rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }

  .form-grid input,
  .form-full textarea {
    padding: 0.7rem;
    font-size: 0.95rem;
  }

  .pecas-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    padding: 0 8px;
  }

  .peca-card {
    padding: 1.2rem;
    gap: 0.8rem;
  }

  .peca-header h4 {
    font-size: 1.05rem;
  }

  .peca-body p {
    font-size: 0.9rem;
    margin: 0.4rem 0;
  }

  .badge {
    padding: 0.2rem 0.5rem;
    font-size: 0.8rem;
  }

  .fotos-grid {
    gap: 0.6rem;
  }

  .foto-thumb {
    height: 100px;
  }

  .label-upload {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .pecas-view {
    padding: 0;
  }

  .view-header {
    flex-direction: column;
    gap: 0.6rem;
    padding: 0 8px;
    margin-bottom: 0.5rem;
  }

  .view-header h2 {
    font-size: 1.3rem;
  }

  .btn-add {
    width: 100%;
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .filter-section {
    padding: 0 8px 0.8rem;
  }

  .filter-select {
    width: 100%;
    padding: 0.6rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .form-container {
    padding: 1rem 8px;
    border-radius: 8px;
    margin-bottom: 1rem;
  }

  .form-container h3 {
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }

  .form-grid input,
  .form-full textarea {
    padding: 0.6rem;
    font-size: 0.9rem;
    border-radius: 6px;
  }

  .form-actions {
    gap: 0.6rem;
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
    padding: 0.6rem;
  }

  .pecas-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
    padding: 0 8px;
  }

  .peca-card {
    padding: 1rem;
    border-radius: 10px;
  }

  .peca-header {
    margin-bottom: 0.8rem;
    padding-bottom: 0.8rem;
    gap: 0.5rem;
  }

  .peca-header h4 {
    font-size: 0.95rem;
    line-height: 1.2;
  }

  .peca-actions {
    gap: 0.4rem;
    margin-left: 0.4rem;
    flex-shrink: 0;
  }

  .btn-icon {
    font-size: 1rem;
    padding: 0.2rem;
  }

  .peca-body {
    gap: 0.3rem;
  }

  .peca-body p {
    font-size: 0.8rem;
    margin: 0.2rem 0;
    line-height: 1.3;
  }

  .badge {
    padding: 0.15rem 0.4rem;
    font-size: 0.75rem;
    border-radius: 3px;
  }

  .estoque-baixo {
    color: #d32f2f;
    font-weight: 600;
  }

  .alerta {
    font-size: 0.75rem;
    margin-left: 0.3rem;
  }

  /* Fotos responsivas */
  .fotos-section {
    margin-bottom: 0.8rem;
  }

  .fotos-section h5 {
    font-size: 0.9rem;
    margin: 0 0 0.6rem 0;
  }

  .fotos-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .foto-item {
    position: relative;
    aspect-ratio: 1;
  }

  .foto-thumb {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 6px;
    padding: 4px;
  }

  .btn-remover-foto {
    top: 2px;
    right: 2px;
    width: 24px;
    height: 24px;
    font-size: 0.9rem;
  }

  .add-foto-section {
    margin-bottom: 0.8rem;
  }

  .label-upload {
    display: block;
    width: 100%;
    padding: 0.6rem;
    font-size: 0.85rem;
    text-align: center;
    border-radius: 6px;
  }

  .empty-state {
    padding: 2rem 1rem;
    margin: 0 8px;
  }
}

/* Tela grande - 1024px+ */
@media (min-width: 1024px) {
  .pecas-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}
</style>
