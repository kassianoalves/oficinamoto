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
        <div class="peca-body">
          <p><strong>Código:</strong> {{ peca.codigo }}</p>
          <p><strong>Categoria:</strong> <span class="badge">{{ peca.categoria }}</span></p>
          <p><strong>Preço:</strong> R$ {{ formatarMoeda(peca.preco_unitario) }}</p>
          <p :class="{ 'estoque-baixo': peca.quantidade <= 5 }">
            <strong>Estoque:</strong> {{ peca.quantidade }} un.
            <span v-if="peca.quantidade <= 5" class="alerta">⚠️ Reorder</span>
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

    const resetFormPeca = () => {
      formPeca.value = {
        nome: '',
        descricao: '',
        codigo: '',
        quantidade: 0,
        preco_unitario: 0,
        categoria: '',
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.peca-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
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
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.peca-header h4 {
  color: #333;
  margin: 0;
  flex: 1;
  word-break: break-word;
}

.peca-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-icon:hover {
  transform: scale(1.2);
}

.peca-body p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.95rem;
}

.peca-body .badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.85rem;
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
  .view-header {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-add {
    width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .pecas-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 430px) {
  .form-container {
    padding: 1rem;
  }

  .peca-card {
    padding: 1rem;
  }

  .peca-header h4 {
    font-size: 1rem;
  }

  .peca-body p {
    font-size: 0.85rem;
  }
}
</style>
