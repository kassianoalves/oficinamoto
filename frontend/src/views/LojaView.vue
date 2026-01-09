<template>
  <div class="loja-container">
    <div class="header">
      <h1>🛍️ Minha Loja</h1>
      <p class="subtitle">Gerencie seus produtos e venda peças para clientes</p>
    </div>

    <!-- Abas: Meus Produtos / Adicionar Produto -->
    <div class="tabs">
      <button
        :class="['tab', { active: abaAtiva === 'produtos' }]"
        @click="abaAtiva = 'produtos'"
      >
        Meus Produtos ({{ produtos.length }})
      </button>
      <button
        :class="['tab', { active: abaAtiva === 'adicionar' }]"
        @click="abaAtiva = 'adicionar'"
      >
        + Adicionar Produto
      </button>
    </div>

    <!-- Aba: Meus Produtos -->
    <div v-if="abaAtiva === 'produtos'" class="tab-content">
      <!-- Filtros -->
      <div class="filtros">
        <input
          v-model="filtroNome"
          type="text"
          placeholder="🔍 Buscar por nome..."
          class="filter-input"
        />
        <select v-model="filtroCategoria" class="filter-select">
          <option value="">Todas as Categorias</option>
          <option>Motores</option>
          <option>Suspensão</option>
          <option>Freios</option>
          <option>Elétrica</option>
          <option>Carroceria</option>
          <option>Acessórios</option>
        </select>
      </div>

      <div v-if="carregando" class="loading">
        <p>Carregando produtos...</p>
      </div>

      <div v-else-if="produtosFiltrados.length > 0" class="produtos-grid">
        <div v-for="produto in produtosFiltrados" :key="produto.id" class="produto-card">
          <div class="produto-imagem">
            <img v-if="produto.imagem" :src="produto.imagem" :alt="produto.nome" />
            <div v-else class="placeholder">
              <p>📦 Sem imagem</p>
            </div>
            <div v-if="!produto.ativo" class="badge-inativo">Inativo</div>
          </div>

          <div class="produto-info">
            <h3>{{ produto.nome }}</h3>
            <p class="categoria">{{ produto.categoria }}</p>
            <p class="descricao">{{ produto.descricao }}</p>

            <div class="info-row">
              <span class="preco">R$ {{ produto.preco.toFixed(2) }}</span>
              <span class="estoque" :class="{ 'estoque-baixo': produto.estoque < 5 }">
                📦 {{ produto.estoque }} un
              </span>
            </div>

            <div v-if="produto.sku" class="sku">SKU: {{ produto.sku }}</div>

            <div class="produto-actions">
              <button @click="editarProduto(produto)" class="btn-editar">
                ✏️ Editar
              </button>
              <button @click="deletarProduto(produto.id)" class="btn-deletar">
                🗑️ Deletar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>Você ainda não tem produtos cadastrados</p>
        <button @click="abaAtiva = 'adicionar'" class="btn-primary">
          Adicione o Primeiro Produto
        </button>
      </div>
    </div>

    <!-- Aba: Adicionar Produto -->
    <div v-if="abaAtiva === 'adicionar'" class="tab-content">
      <div class="form-container">
        <h2>{{ editando ? 'Editar Produto' : 'Novo Produto' }}</h2>

        <form @submit.prevent="salvarProduto" class="form">
          <div class="form-group">
            <label for="nome">Nome do Produto:</label>
            <input
              v-model="formulario.nome"
              type="text"
              id="nome"
              placeholder="Ex: Corrente de transmissão"
              required
            />
          </div>

          <div class="form-group">
            <label for="categoria">Categoria:</label>
            <select v-model="formulario.categoria" id="categoria" required>
              <option value="">-- Selecione uma categoria --</option>
              <option>Motores</option>
              <option>Suspensão</option>
              <option>Freios</option>
              <option>Elétrica</option>
              <option>Carroceria</option>
              <option>Acessórios</option>
            </select>
          </div>

          <div class="form-group">
            <label for="descricao">Descrição:</label>
            <textarea
              v-model="formulario.descricao"
              id="descricao"
              placeholder="Descreva o produto detalhadamente"
              rows="4"
              required
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="preco">Preço (R$):</label>
              <input
                v-model.number="formulario.preco"
                type="number"
                id="preco"
                step="0.01"
                min="0"
                required
              />
            </div>

            <div class="form-group">
              <label for="estoque">Estoque (un):</label>
              <input
                v-model.number="formulario.estoque"
                type="number"
                id="estoque"
                min="0"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="sku">SKU (Código do Produto):</label>
            <input
              v-model="formulario.sku"
              type="text"
              id="sku"
              placeholder="Ex: PRD-001"
            />
          </div>

          <div class="form-group">
            <label for="imagem">Foto do Produto:</label>
            <input
              type="file"
              id="imagem"
              accept="image/*"
              @change="onFileSelected"
            />
            <img
              v-if="previewUrl"
              :src="previewUrl"
              alt="Preview"
              class="preview-img"
            />
          </div>

          <div class="form-group checkbox">
            <input v-model="formulario.ativo" type="checkbox" id="ativo" />
            <label for="ativo">Produto Ativo</label>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-salvar">
              {{ editando ? '💾 Atualizar' : '💾 Criar Produto' }}
            </button>
            <button type="button" @click="cancelarEdicao" class="btn-cancelar">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '../api.js';

export default {
  name: 'LojaView',
  setup() {
    const abaAtiva = ref('produtos');
    const produtos = ref([]);
    const carregando = ref(false);
    const editando = ref(false);
    const produtoEditando = ref(null);
    const filtroNome = ref('');
    const filtroCategoria = ref('');
    const previewUrl = ref(null);

    const formulario = ref({
      nome: '',
      categoria: '',
      descricao: '',
      preco: 0,
      estoque: 0,
      sku: '',
      imagem: null,
      ativo: true
    });

    const produtosFiltrados = computed(() => {
      return produtos.value.filter(p => {
        const matchNome = p.nome.toLowerCase().includes(filtroNome.value.toLowerCase());
        const matchCategoria = !filtroCategoria.value || p.categoria === filtroCategoria.value;
        return matchNome && matchCategoria;
      });
    });

    const carregarProdutos = async () => {
      carregando.value = true;
      try {
        const response = await api.get('/produtos-loja/');
        produtos.value = response.data.results || response.data;
      } catch (error) {
        console.error('Erro ao carregar produtos:', error);
      } finally {
        carregando.value = false;
      }
    };

    const onFileSelected = (event) => {
      const file = event.target.files[0];
      if (file) {
        formulario.value.imagem = file;

        const reader = new FileReader();
        reader.onload = (e) => {
          previewUrl.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const salvarProduto = async () => {
      const formData = new FormData();
      formData.append('nome', formulario.value.nome);
      formData.append('categoria', formulario.value.categoria);
      formData.append('descricao', formulario.value.descricao);
      formData.append('preco', formulario.value.preco);
      formData.append('estoque', formulario.value.estoque);
      formData.append('sku', formulario.value.sku);
      formData.append('ativo', formulario.value.ativo);

      if (formulario.value.imagem && typeof formulario.value.imagem === 'object') {
        formData.append('imagem', formulario.value.imagem);
      }

      try {
        if (editando.value) {
          await api.put(`/produtos-loja/${produtoEditando.value.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          alert('✅ Produto atualizado com sucesso!');
        } else {
          await api.post('/produtos-loja/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          alert('✅ Produto criado com sucesso!');
        }

        resetarFormulario();
        abaAtiva.value = 'produtos';
        carregarProdutos();
      } catch (error) {
        console.error('Erro ao salvar produto:', error);
        alert('❌ Erro ao salvar produto. Tente novamente.');
      }
    };

    const editarProduto = (produto) => {
      editando.value = true;
      produtoEditando.value = produto;
      formulario.value = {
        nome: produto.nome,
        categoria: produto.categoria,
        descricao: produto.descricao,
        preco: produto.preco,
        estoque: produto.estoque,
        sku: produto.sku,
        imagem: null,
        ativo: produto.ativo
      };
      if (produto.imagem) {
        previewUrl.value = produto.imagem;
      }
      abaAtiva.value = 'adicionar';
    };

    const deletarProduto = async (id) => {
      if (confirm('Tem certeza que deseja deletar este produto?')) {
        try {
          await api.delete(`/produtos-loja/${id}/`);
          alert('✅ Produto deletado com sucesso!');
          carregarProdutos();
        } catch (error) {
          console.error('Erro ao deletar produto:', error);
          alert('❌ Erro ao deletar produto.');
        }
      }
    };

    const resetarFormulario = () => {
      editando.value = false;
      produtoEditando.value = null;
      formulario.value = {
        nome: '',
        categoria: '',
        descricao: '',
        preco: 0,
        estoque: 0,
        sku: '',
        imagem: null,
        ativo: true
      };
      previewUrl.value = null;
    };

    const cancelarEdicao = () => {
      resetarFormulario();
      abaAtiva.value = 'produtos';
    };

    onMounted(() => {
      carregarProdutos();
    });

    return {
      abaAtiva,
      produtos,
      carregando,
      editando,
      filtroNome,
      filtroCategoria,
      previewUrl,
      formulario,
      produtosFiltrados,
      carregarProdutos,
      onFileSelected,
      salvarProduto,
      editarProduto,
      deletarProduto,
      cancelarEdicao
    };
  }
};
</script>

<style scoped>
.loja-container {
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

/* Filtros */
.filtros {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 10px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s;
}

.filter-input:focus,
.filter-select:focus {
  border-color: #ff6b35;
  outline: none;
}

.filter-input {
  flex: 1;
  min-width: 200px;
}

.filter-select {
  min-width: 150px;
}

/* Grid de Produtos */
.produtos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.produto-card {
  background: white;
  border: 2px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.produto-card:hover {
  border-color: #ff6b35;
  box-shadow: 0 5px 20px rgba(255, 107, 53, 0.1);
  transform: translateY(-5px);
}

.produto-imagem {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.produto-imagem img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  text-align: center;
  color: #999;
}

.badge-inativo {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.8em;
}

.produto-info {
  padding: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.produto-info h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.categoria {
  color: #999;
  font-size: 0.85em;
  margin: 0 0 10px 0;
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.descricao {
  color: #666;
  font-size: 0.9em;
  line-height: 1.5;
  margin-bottom: 10px;
  flex: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 6px;
}

.preco {
  font-size: 1.3em;
  font-weight: bold;
  color: #ff6b35;
}

.estoque {
  font-size: 0.9em;
  color: #28a745;
}

.estoque-baixo {
  color: #ff6b35;
  font-weight: bold;
}

.sku {
  font-size: 0.8em;
  color: #999;
  margin-bottom: 10px;
}

.produto-actions {
  display: flex;
  gap: 10px;
}

.btn-editar,
.btn-deletar {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9em;
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
  max-width: 600px;
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
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #ff6b35;
  outline: none;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  margin-top: 10px;
}

.form-group.checkbox input {
  width: auto;
  margin-right: 10px;
}

.form-group.checkbox label {
  margin: 0;
}

.preview-img {
  max-width: 100%;
  max-height: 250px;
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
  font-size: 1em;
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
  .produtos-grid {
    grid-template-columns: 1fr;
  }

  .header h1 {
    font-size: 1.8em;
  }

  .form-container {
    max-width: 100%;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .tabs {
    flex-direction: column;
  }

  .filtros {
    flex-direction: column;
  }

  .filter-input,
  .filter-select {
    width: 100%;
  }
}
</style>
