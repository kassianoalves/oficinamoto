<template>
  <transition name="drawer-overlay">
    <div v-if="drawerAberto" class="drawer-overlay" @click="fecharDrawer"></div>
  </transition>

  <transition name="drawer-slide">
    <div v-if="drawerAberto" class="drawer-container">
      <div class="drawer-header">
        <h2>🛒 Meu Carrinho</h2>
        <button class="btn-fechar" @click="fecharDrawer">✕</button>
      </div>

      <div v-if="carregandoCarrinho" class="drawer-loading">
        <p>Carregando...</p>
      </div>

      <div v-else-if="!temItens" class="drawer-empty">
        <p>🛒</p>
        <p>Seu carrinho está vazio</p>
        <button @click="fecharDrawer" class="btn-continuar">Continuar comprando</button>
      </div>

      <div v-else class="drawer-content">
        <div class="itens-lista">
          <div v-for="item in itensCarrinho" :key="item.id" class="item-card">
            <div class="item-foto">
              <img v-if="item.peca_foto" :src="item.peca_foto" :alt="item.peca_nome" />
              <div v-else class="foto-placeholder">📦</div>
            </div>

            <div class="item-info">
              <h4>{{ item.peca_nome }}</h4>
              <p class="item-codigo">Cód: {{ item.peca_codigo }}</p>
              <p class="item-preco">R$ {{ parseFloat(item.preco_unitario).toFixed(2) }}</p>
              
              <div class="item-quantidade">
                <button 
                  @click="diminuirQuantidade(item)" 
                  class="btn-qty"
                  :disabled="carregandoCarrinho"
                >
                  −
                </button>
                <input 
                  type="number" 
                  v-model.number="item.quantidade" 
                  @change="atualizarQty(item)"
                  min="1"
                  :max="item.estoque_disponivel"
                  class="input-qty"
                  :disabled="carregandoCarrinho"
                />
                <button 
                  @click="aumentarQuantidade(item)" 
                  class="btn-qty"
                  :disabled="carregandoCarrinho || item.quantidade >= item.estoque_disponivel"
                >
                  +
                </button>
              </div>

              <p v-if="item.quantidade >= item.estoque_disponivel" class="aviso-estoque">
                ⚠️ Estoque máximo
              </p>
            </div>

            <div class="item-acoes">
              <p class="item-subtotal">R$ {{ parseFloat(item.subtotal).toFixed(2) }}</p>
              <button 
                @click="remover(item)" 
                class="btn-remover"
                :disabled="carregandoCarrinho"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>

        <div class="drawer-footer">
          <div class="resumo">
            <div class="resumo-linha">
              <span>Subtotal ({{ totalItens }} {{ totalItens === 1 ? 'item' : 'itens' }}):</span>
              <span class="resumo-valor">R$ {{ totalPreco.toFixed(2) }}</span>
            </div>
          </div>

          <button @click="finalizar" class="btn-finalizar" :disabled="carregandoCarrinho">
            Finalizar Compra
          </button>

          <button @click="limpar" class="btn-limpar" :disabled="carregandoCarrinho">
            Limpar Carrinho
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>

import { useCarrinho } from '@/composables/useCarrinho';

export default {
  name: 'CarrinhoDrawer',
  setup() {
    const {
      itensCarrinho,
      carregandoCarrinho,
      drawerAberto,
      totalItens,
      totalPreco,
      temItens,
      atualizarQuantidade,
      removerItem,
      limparCarrinho,
      fecharDrawer,
      validarEstoque
    } = useCarrinho();

    // Log para depuração: exibe os itens do carrinho sempre que o componente renderiza
    console.log('[CARRINHO][DRAWER] itensCarrinho:', itensCarrinho.value);

    const aumentarQuantidade = async (item) => {
      await atualizarQuantidade(item.id, item.quantidade + 1);
    };

    const diminuirQuantidade = async (item) => {
      await atualizarQuantidade(item.id, item.quantidade - 1);
    };

    const atualizarQty = async (item) => {
      if (item.quantidade <= 0) {
        await removerItem(item.id);
      } else {
        await atualizarQuantidade(item.id, item.quantidade);
      }
    };

    const remover = async (item) => {
      // TODO: Adicionar feedback visual se necessário
      await removerItem(item.id);
    };

    const limpar = async () => {
      // TODO: Adicionar feedback visual (snackbar/toast) se necessário
      const resultado = await limparCarrinho();
      // if (resultado.sucesso) { ... }
    };

    const finalizar = async () => {
      const { valido, erros } = await validarEstoque();

      if (!valido) {
        // TODO: Adicionar feedback visual de erro de estoque
        return;
      }

      // TODO: Implementar checkout/pagamento
    };

    return {
      itensCarrinho,
      carregandoCarrinho,
      drawerAberto,
      totalItens,
      totalPreco,
      temItens,
      fecharDrawer,
      aumentarQuantidade,
      diminuirQuantidade,
      atualizarQty,
      remover,
      limpar,
      finalizar
    };
  }
};
</script>

<style scoped>
/* Overlay */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* Drawer Container */
.drawer-container {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 400px;
  max-width: 90vw;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

/* Header */
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
}

.drawer-header h2 {
  margin: 0;
  font-size: 1.3em;
  color: #333;
}

.btn-fechar {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #999;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.btn-fechar:hover {
  color: #333;
}

/* Loading/Empty */
.drawer-loading,
.drawer-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #999;
}

.drawer-empty p:first-child {
  font-size: 4em;
  margin-bottom: 10px;
}

.btn-continuar {
  margin-top: 20px;
  padding: 12px 24px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-continuar:hover {
  background: #e55a24;
  transform: translateY(-2px);
}

/* Content */
.drawer-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.itens-lista {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

/* Item Card */
.item-card {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  border: 1px solid #eee;
}

.item-foto {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-foto img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px;
}

.foto-placeholder {
  font-size: 2em;
  color: #ccc;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-info h4 {
  margin: 0;
  font-size: 0.95em;
  color: #333;
  line-height: 1.3;
}

.item-codigo {
  font-size: 0.8em;
  color: #999;
  margin: 0;
}

.item-preco {
  font-size: 0.9em;
  font-weight: 600;
  color: #ff6b35;
  margin: 4px 0;
}

.item-quantidade {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.btn-qty {
  width: 28px;
  height: 28px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
  color: #333;
  transition: all 0.3s;
}

.btn-qty:hover:not(:disabled) {
  background: #f0f0f0;
  border-color: #ff6b35;
}

.btn-qty:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.input-qty {
  width: 50px;
  height: 28px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9em;
}

.aviso-estoque {
  font-size: 0.75em;
  color: #ff6b35;
  margin: 2px 0 0 0;
}

.item-acoes {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
}

.item-subtotal {
  font-size: 1em;
  font-weight: bold;
  color: #333;
  margin: 0;
}


.btn-remover {
  background: transparent;
  color: #e53935;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.2em;
  transition: color 0.3s, background 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remover:hover:not(:disabled) {
  color: #b71c1c;
  background: transparent;
}

.btn-remover:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Footer */
.drawer-footer {
  border-top: 2px solid #f0f0f0;
  padding: 15px;
  background: linear-gradient(135deg, #f9f9f9 0%, #f0f0f0 100%);
}

.resumo {
  margin-bottom: 12px;
}

.resumo-linha {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
}

.resumo-valor {
  color: #ff6b35;
  font-size: 1.2em;
}

.btn-finalizar,
.btn-limpar {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1em;
  transition: all 0.3s;
  margin-bottom: 8px;
}

.btn-finalizar {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.btn-finalizar:hover:not(:disabled) {
  background: linear-gradient(135deg, #218838 0%, #1aa179 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.25);
}

.btn-limpar {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
}

.btn-limpar:hover:not(:disabled) {
  background: linear-gradient(135deg, #c82333 0%, #bd2130 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.25);
}

.btn-finalizar:disabled,
.btn-limpar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Animations */
.drawer-overlay-enter-active,
.drawer-overlay-leave-active {
  transition: opacity 0.3s;
}

.drawer-overlay-enter-from,
.drawer-overlay-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.3s;
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

/* Responsive */
@media (max-width: 768px) {
  .drawer-container {
    width: 90vw;
    max-width: 400px;
  }

  .drawer-header {
    padding: 12px 16px;
  }

  .drawer-header h2 {
    font-size: 1.2rem;
  }

  .itens-lista {
    max-height: calc(100vh - 280px);
  }

  .item-card {
    padding: 10px;
    gap: 10px;
  }

  .item-foto {
    width: 60px;
    height: 60px;
  }

  .item-info h4 {
    font-size: 0.9rem;
  }

  .item-quantidade {
    gap: 4px;
  }

  .btn-qty,
  .input-qty {
    font-size: 0.9rem;
    padding: 4px 6px;
  }

  .item-subtotal {
    font-size: 0.9rem;
  }

  .btn-remover {
    font-size: 1rem;
    padding: 4px;
  }

  .resumo-valor {
    font-size: 1rem;
  }

  .btn-finalizar,
  .btn-limpar {
    padding: 10px 14px;
    font-size: 0.95rem;
  }

  .drawer-footer {
    padding: 12px;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .drawer-container {
    width: 100vw;
    max-width: 100vw;
    border-radius: 16px 16px 0 0;
  }

  .drawer-header {
    padding: 10px 12px;
  }

  .drawer-header h2 {
    font-size: 1rem;
  }

  .itens-lista {
    max-height: calc(100vh - 260px);
  }

  .item-card {
    flex-direction: row;
    padding: 8px;
  }

  .item-foto {
    width: 50px;
    height: 50px;
    flex-shrink: 0;
  }

  .item-info {
    flex: 1;
    gap: 4px;
  }

  .item-info h4 {
    font-size: 0.85rem;
    margin: 0;
  }

  .item-codigo {
    font-size: 0.75rem;
    margin: 2px 0;
  }

  .item-preco {
    font-size: 0.85rem;
    font-weight: 600;
    margin: 2px 0;
  }

  .item-quantidade {
    gap: 2px;
    margin-top: 4px;
  }

  .btn-qty {
    padding: 2px 4px;
    font-size: 0.8rem;
    width: 24px;
    height: 24px;
  }

  .input-qty {
    width: 40px;
    font-size: 0.8rem;
    padding: 2px;
  }

  .aviso-estoque {
    font-size: 0.7rem;
    margin: 2px 0 0 0;
  }

  .item-acoes {
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
    gap: 4px;
  }

  .item-subtotal {
    font-size: 0.85rem;
    font-weight: 600;
  }

  .btn-remover {
    font-size: 0.95rem;
    padding: 3px;
  }

  .resumo {
    padding: 8px;
  }

  .resumo-linha {
    font-size: 0.9rem;
    gap: 8px;
  }

  .resumo-valor {
    font-size: 0.95rem;
  }

  .btn-finalizar,
  .btn-limpar {
    padding: 8px 12px;
    font-size: 0.9rem;
  }

  .drawer-footer {
    padding: 10px;
    gap: 6px;
  }

  .btn-fechar {
    font-size: 1.2rem;
  }
}
</style>
