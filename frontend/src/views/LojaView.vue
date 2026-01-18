<template>
  <div class="loja-container">
    <div class="header">
      <h1>🛍️ Minha Loja</h1>
      <p class="subtitle">Produtos disponíveis do Estoque para venda</p>
    </div>

    <!-- Filtros -->
    <div class="filtros">
      <input
        v-model="filtroNome"
        type="text"
        placeholder="🔍 Buscar por nome, marca ou categoria..."
        class="filter-input"
      />
      <select v-model="filtroCategoria" class="filter-select">
        <option value="">Todas as Categorias</option>
        <option v-for="cat in categoriasDisponiveis" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
    </div>

    <div v-if="carregando" class="loading">
      <p>Carregando produtos...</p>
    </div>

    <div v-else-if="produtosFiltrados.length > 0" class="produtos-grid">
      <div v-for="produto in produtosFiltrados" :key="produto.id" class="produto-card" @click="abrirModal(produto)">
        <!-- Carousel de fotos -->
        <div class="produto-carousel">
          <div class="carousel-container">
            <img 
              v-if="fotosProduto[produto.id] && fotosProduto[produto.id].length > 0"
              :src="fotosProduto[produto.id][indexFoto[produto.id] || 0]" 
              :alt="produto.nome"
              class="carousel-img"
            />
            <div v-else class="placeholder">
              <p>📦 Sem fotos</p>
            </div>
          </div>
          
          <!-- Navegação de fotos -->
          <div v-if="fotosProduto[produto.id] && fotosProduto[produto.id].length > 1" class="carousel-nav">
            <span class="carousel-indicator">
              {{ (indexFoto[produto.id] || 0) + 1 }} / {{ fotosProduto[produto.id].length }}
            </span>
          </div>
        </div>

        <div class="produto-info">
          <h3>{{ produto.nome }}</h3>

          <div class="info-row">
            <span class="preco">R$ {{ parseFloat(produto.preco).toFixed(2) }}</span>
          </div>

          <!-- Status de Disponibilidade -->
          <div v-if="produto.estoque === 0" class="status indisponivel">
            ❌ Indisponível
          </div>
          <div v-else-if="produto.estoque > 0 && produto.estoque < 5" class="status atencao">
            ⚠️ {{ produto.estoque }} unidades!
          </div>
          <div v-else class="status disponivel">
            ✅ Disponível
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Nenhum produto disponível no estoque</p>
    </div>

    <!-- Modal de Detalhes do Produto -->
    <div v-if="produtoSelecionado" class="modal-overlay" @click.self="fecharModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ produtoSelecionado.nome }}</h2>
          <button class="modal-close" @click="fecharModal">✕</button>
        </div>

        <!-- Carrossel de fotos -->
        <div class="modal-carousel">
          <img 
            v-if="fotosProduto[produtoSelecionado.id] && fotosProduto[produtoSelecionado.id].length > 0"
            :src="fotosProduto[produtoSelecionado.id][indexFotoModal[produtoSelecionado.id] || 0]"
            :alt="produtoSelecionado.nome"
            class="modal-carousel-img"
            @click="expandirFoto"
          />
          <div v-else class="modal-placeholder">
            <p>📦 Sem fotos</p>
          </div>

          <!-- Navegação de fotos no modal -->
          <div v-if="fotosProduto[produtoSelecionado.id] && fotosProduto[produtoSelecionado.id].length > 1" class="modal-carousel-nav">
            <button @click="mudarFotoModal(produtoSelecionado.id, -1)" class="modal-carousel-btn">◀</button>
            <span>{{ (indexFotoModal[produtoSelecionado.id] || 0) + 1 }} / {{ fotosProduto[produtoSelecionado.id].length }}</span>
            <button @click="mudarFotoModal(produtoSelecionado.id, 1)" class="modal-carousel-btn">▶</button>
          </div>
        </div>

        <div class="modal-body">
          <div class="modal-info-row">
            <label>Preço:</label>
            <span class="modal-preco">R$ {{ parseFloat(produtoSelecionado.preco).toFixed(2) }}</span>
          </div>

          <div class="modal-info-row">
            <label>Categoria:</label>
            <span>{{ produtoSelecionado.categoria }}</span>
          </div>

          <div v-if="produtoSelecionado.fornecedor" class="modal-info-row">
            <label>Marca/Fornecedor:</label>
            <span>{{ produtoSelecionado.fornecedor }}</span>
          </div>

          <div class="modal-info-row">
            <label>Unidades disponíveis:</label>
            <span>{{ produtoSelecionado.estoque }}</span>
          </div>

          <div v-if="produtoSelecionado.descricao" class="modal-descricao">
            <label>Descrição:</label>
            <p>{{ produtoSelecionado.descricao }}</p>
          </div>

          <div v-if="produtoSelecionado.codigo" class="modal-info-row">
            <label>Código:</label>
            <span>{{ produtoSelecionado.codigo }}</span>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-carrinho" @click="adicionarAoCarrinho">
            🛒 Adicionar
          </button>
          <button class="btn-cancelar" @click="fecharModal">
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <!-- Lightbox para foto expandida -->
    <div v-if="fotoExpandida" class="lightbox-overlay" @click="fecharLightbox">
      <div class="lightbox-container" @click.stop>
        <img :src="fotoExpandida" :alt="produtoSelecionado.nome" class="lightbox-img" />
        <button class="lightbox-close" @click="fecharLightbox">✕</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '../api.js';
import { useCarrinho } from '@/composables/useCarrinho.js';

export default {
  name: 'LojaView',
  setup() {
    const produtos = ref([]);
    const carregando = ref(false);
    const filtroNome = ref('');
    const filtroCategoria = ref('');
    const fotosProduto = ref({});
    const indexFoto = ref({});
    const produtoSelecionado = ref(null);
    const indexFotoModal = ref({});
    const fotoExpandida = ref(null);

    const produtosFiltrados = computed(() => {
      return produtos.value.filter(p => {
        const searchTerm = filtroNome.value.toLowerCase();
        const matchNome = p.nome.toLowerCase().includes(searchTerm);
        const matchFornecedor = (p.fornecedor || '').toLowerCase().includes(searchTerm);
        const matchCategoria = (p.categoria || '').toLowerCase().includes(searchTerm);
        
        const matchBusca = matchNome || matchFornecedor || matchCategoria;
        const matchCategoriaFiltro = !filtroCategoria.value || p.categoria === filtroCategoria.value;
        
        return matchBusca && matchCategoriaFiltro;
      });
    });

    const categoriasDisponiveis = computed(() => {
      const categorias = new Set();
      produtos.value.forEach(p => {
        if (p.categoria) {
          categorias.add(p.categoria);
        }
      });
      return Array.from(categorias).sort();
    });

    const carregarProdutos = async () => {
      carregando.value = true;
      try {
        // Buscar produtos do endpoint de peças (estoque)
        const response = await api.get('/pecas/');
        produtos.value = response.data.results || response.data;
        
        // Inicializar índices de fotos baseado nas fotos do backend
        produtos.value.forEach(produto => {
          indexFoto.value[produto.id] = 0;
          fotosProduto.value[produto.id] = (produto.fotos || []).map(f => f.imagem);
        });
      } catch (error) {
        console.error('Erro ao carregar produtos do estoque:', error);
      } finally {
        carregando.value = false;
      }
    };

    const mudarFoto = (produtoId, direcao) => {
      if (!fotosProduto.value[produtoId] || fotosProduto.value[produtoId].length === 0) {
        return;
      }

      let novoIndex = (indexFoto.value[produtoId] || 0) + direcao;
      const totalFotos = fotosProduto.value[produtoId].length;

      if (novoIndex < 0) {
        novoIndex = totalFotos - 1;
      } else if (novoIndex >= totalFotos) {
        novoIndex = 0;
      }

      indexFoto.value[produtoId] = novoIndex;
    };

    const abrirModal = (produto) => {
      produtoSelecionado.value = produto;
      indexFotoModal.value[produto.id] = 0;
    };

    const fecharModal = () => {
      produtoSelecionado.value = null;
    };

    const mudarFotoModal = (produtoId, direcao) => {
      if (!fotosProduto.value[produtoId] || fotosProduto.value[produtoId].length === 0) {
        return;
      }

      let novoIndex = (indexFotoModal.value[produtoId] || 0) + direcao;
      const totalFotos = fotosProduto.value[produtoId].length;

      if (novoIndex < 0) {
        novoIndex = totalFotos - 1;
      } else if (novoIndex >= totalFotos) {
        novoIndex = 0;
      }

      indexFotoModal.value[produtoId] = novoIndex;
    };

    const adicionarAoCarrinho = () => {
      console.log('Produto adicionado ao carrinho:', produtoSelecionado.value);
      // Integrar com o sistema de carrinho
      useCarrinho().adicionarAoCarrinho(produtoSelecionado.value, 1).then(resultado => {
        if (resultado.sucesso) {
          alert(resultado.mensagem);
          fecharModal();
        } else {
          alert(resultado.mensagem);
        }
      });
    };

    const expandirFoto = () => {
      if (produtoSelecionado.value && fotosProduto.value[produtoSelecionado.value.id]) {
        const fotos = fotosProduto.value[produtoSelecionado.value.id];
        const indexAtual = indexFotoModal.value[produtoSelecionado.value.id] || 0;
        fotoExpandida.value = fotos[indexAtual];
      }
    };

    const fecharLightbox = () => {
      fotoExpandida.value = null;
    };

    onMounted(() => {
      carregarProdutos();
    });

    return {
      produtos,
      carregando,
      filtroNome,
      filtroCategoria,
      fotosProduto,
      indexFoto,
      produtosFiltrados,
      categoriasDisponiveis,
      carregarProdutos,
      mudarFoto,
      produtoSelecionado,
      indexFotoModal,
      abrirModal,
      fecharModal,
      mudarFotoModal,
      adicionarAoCarrinho,
      fotoExpandida,
      expandirFoto,
      fecharLightbox
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
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.produto-card {
  background: white;
  border: 2px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.produto-card:hover {
  border-color: #ff6b35;
  box-shadow: 0 5px 20px rgba(255, 107, 53, 0.15);
  transform: translateY(-5px);
}

/* Carousel de fotos */
.produto-carousel {
  width: 100%;
  background: #f5f5f5;
  position: relative;
}

.carousel-container {
  width: 100%;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
  position: relative;
  border-bottom: 1px solid #e8e8e8;
}

.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  transition: opacity 0.3s;
  padding: 8px;
  box-sizing: border-box;
}

.placeholder {
  text-align: center;
  color: #999;
  font-size: 3em;
}

.carousel-nav {
  position: absolute;
  left: 50%;
  bottom: 6px;
  transform: translateX(-50%);
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  border-radius: 14px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.carousel-btn {
  background: #ff6b35;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.carousel-btn:hover {
  background: #e55a24;
  transform: scale(1.1);
}

.carousel-indicator {
  color: #fff;
  font-size: 0.8em;
  font-weight: 600;
  letter-spacing: 0.2px;
}

.produto-info {
  padding: 10px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.produto-info h3 {
  margin: 0 0 6px 0;
  color: #333;
  font-size: 0.9em;
  line-height: 1.2;
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
  margin-bottom: 12px;
  flex: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 0;
  background: transparent;
  border-radius: 0;
}

.preco {
  font-size: 1em;
  font-weight: bold;
  color: #ff6b35;
}

/* Status de Disponibilidade */
.status {
  font-size: 0.75em;
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
  font-weight: 600;
  margin-bottom: 8px;
}

.status.disponivel {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status.indisponivel {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status.atencao {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.sku {
  font-size: 0.8em;
  color: #999;
  margin-bottom: 15px;
}

/* Ações do Produto */
.produto-actions {
  display: flex;
  gap: 10px;
}

.btn-comprar {
  flex: 1;
  padding: 8px;
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
  font-size: 0.8em;
}

.btn-comprar:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
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
}

/* Responsive */
@media (max-width: 1024px) {
  .produtos-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
    padding: 12px;
  }

  .filtros {
    gap: 10px;
    padding: 0 12px;
  }

  .filter-input,
  .filter-select {
    font-size: 0.95rem;
    padding: 8px 10px;
  }
}

@media (max-width: 768px) {
  .loja-container {
    padding: 8px;
  }

  .header {
    padding: 16px 12px;
  }

  .header h1 {
    font-size: 1.6em;
    margin-bottom: 8px;
  }

  .header .subtitle {
    font-size: 0.9em;
  }

  .produtos-grid {
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 10px;
    padding: 10px;
  }

  .filtros {
    flex-direction: column;
    gap: 8px;
    padding: 0 12px 12px;
  }

  .filter-input,
  .filter-select {
    width: 100%;
    font-size: 0.95rem;
    padding: 10px;
  }

  .carousel-container {
    height: 140px;
  }

  .produto-card {
    border-radius: 8px;
  }

  .produto-info {
    padding: 8px 10px;
  }

  .produto-info h3 {
    font-size: 0.85em;
    margin-bottom: 4px;
  }

  .preco {
    font-size: 0.95em;
  }

  .carousel-indicator {
    font-size: 0.75em;
  }

  .status {
    font-size: 0.7em;
    padding: 3px 6px;
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.25);
  max-width: 500px;
  width: 100%;
  overflow: hidden;
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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.3em;
  color: #333;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.modal-close:hover {
  color: #333;
}

.modal-carousel {
  width: 100%;
  background: linear-gradient(135deg, #f9f9f9 0%, #f0f0f0 100%);
  position: relative;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-carousel-img {
  width: 100%;
  height: 200px;
  object-fit: contain;
  object-position: center;
  cursor: pointer;
  transition: transform 0.3s;
  border-radius: 8px;
}

.modal-carousel-img:hover {
  transform: scale(1.02);
}

.modal-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
  color: #ccc;
  font-size: 2.5em;
  border-radius: 8px;
}

.modal-carousel-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 10px 0 0 0;
  background: transparent;
  border-top: none;
}

.modal-carousel-btn {
  background: #ff6b35;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9em;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-carousel-btn:hover {
  background: #e55a24;
  transform: scale(1.1);
}

.modal-body {
  padding: 18px 20px;
  border-bottom: 1px solid #f0f0f0;
  max-height: 300px;
  overflow-y: auto;
}

.modal-info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 15px;
}

.modal-info-row label {
  font-weight: 600;
  color: #555;
  min-width: 120px;
  font-size: 0.95em;
}

.modal-info-row span {
  color: #777;
  flex: 1;
  text-align: right;
  font-size: 0.95em;
}

.modal-preco {
  font-size: 1.2em;
  font-weight: bold;
  color: #ff6b35;
}

.modal-descricao {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.modal-descricao label {
  font-weight: 600;
  color: #555;
  display: block;
  margin-bottom: 8px;
  font-size: 0.95em;
}

.modal-descricao p {
  color: #777;
  line-height: 1.5;
  margin: 0;
  font-size: 0.95em;
}

.modal-footer {
  padding: 15px 20px;
  display: flex;
  gap: 10px;
  background: linear-gradient(135deg, #f9f9f9 0%, #f0f0f0 100%);
}

.btn-carrinho {
  flex: 1;
  padding: 10px 16px;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95em;
  transition: all 0.3s;
}

.btn-carrinho:hover {
  background: linear-gradient(135deg, #218838 0%, #1aa179 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.25);
}

.btn-cancelar {
  flex: 1;
  padding: 10px 16px;
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95em;
  transition: all 0.3s;
}

.btn-cancelar:hover {
  background: linear-gradient(135deg, #c82333 0%, #bd2130 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.25);
}

/* Lightbox para foto expandida */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  padding: 20px;
  cursor: pointer;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.lightbox-container {
  position: relative;
  max-width: 70vw;
  max-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-img {
  max-width: 50%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  color: #333;
  font-size: 1.5em;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  z-index: 1002;
}

.lightbox-close:hover {
  background: white;
  transform: scale(1.1);
}

@media (max-width: 600px) {
  .modal-content {
    max-width: 95vw;
  }

  .modal-carousel-img {
    height: 150px;
  }

  .modal-placeholder {
    height: 150px;
  }

  .modal-info-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .modal-info-row span {
    text-align: left;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
