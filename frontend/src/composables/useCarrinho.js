import { ref, computed } from 'vue';
import api from '@/api.js';

// Estado global do carrinho
const itensCarrinho = ref([]);
const carregandoCarrinho = ref(false);
const drawerAberto = ref(false);

export function useCarrinho() {
  const totalItens = computed(() => {
    return itensCarrinho.value.reduce((total, item) => total + item.quantidade, 0);
  });

  const totalPreco = computed(() => {
    return itensCarrinho.value.reduce((total, item) => {
      return total + (parseFloat(item.subtotal) || 0);
    }, 0);
  });

  const temItens = computed(() => itensCarrinho.value.length > 0);

  // Verifica se usuário está logado
  const usuarioLogado = computed(() => {
    return !!localStorage.getItem('token');
  });

  /**
   * Carrega carrinho do backend ou localStorage
   */
  const carregarCarrinho = async () => {
    carregandoCarrinho.value = true;
    
    try {
      if (usuarioLogado.value) {
        // Usuário logado: busca do backend
        const response = await api.get('/carrinho/');
        itensCarrinho.value = response.data;
      } else {
        // Usuário anônimo: busca do localStorage
        const carrinhoLocal = localStorage.getItem('carrinho');
        itensCarrinho.value = carrinhoLocal ? JSON.parse(carrinhoLocal) : [];
      }
    } catch (error) {
      console.error('Erro ao carregar carrinho:', error);
      // Fallback para localStorage
      const carrinhoLocal = localStorage.getItem('carrinho');
      itensCarrinho.value = carrinhoLocal ? JSON.parse(carrinhoLocal) : [];
    } finally {
      carregandoCarrinho.value = false;
    }
  };

  /**
   * Salva carrinho no localStorage (para usuários anônimos)
   */
  const salvarLocalStorage = () => {
    localStorage.setItem('carrinho', JSON.stringify(itensCarrinho.value));
  };

  /**
   * Adiciona produto ao carrinho
   */
  const adicionarAoCarrinho = async (produto, quantidade = 1) => {
    carregandoCarrinho.value = true;

    try {
      if (usuarioLogado.value) {
        // Usuário logado: usa API
        const response = await api.post('/carrinho/adicionar/', {
          peca_id: produto.id,
          quantidade: quantidade
        });

        // Atualiza lista
        await carregarCarrinho();
        
        return { sucesso: true, mensagem: 'Produto adicionado ao carrinho!' };
      } else {
        // Usuário anônimo: usa localStorage
        const itemExistente = itensCarrinho.value.find(item => item.peca === produto.id);

        if (itemExistente) {
          // Atualiza quantidade
          const novaQuantidade = itemExistente.quantidade + quantidade;
          
          if (novaQuantidade > produto.estoque) {
            return { sucesso: false, mensagem: `Estoque insuficiente. Disponível: ${produto.estoque}` };
          }

          itemExistente.quantidade = novaQuantidade;
          itemExistente.subtotal = itemExistente.quantidade * parseFloat(itemExistente.preco_unitario);
        } else {
          // Adiciona novo item
          if (quantidade > produto.estoque) {
            return { sucesso: false, mensagem: `Estoque insuficiente. Disponível: ${produto.estoque}` };
          }

          const novoItem = {
            id: Date.now(), // ID temporário para localStorage
            peca: produto.id,
            peca_nome: produto.nome,
            peca_codigo: produto.codigo,
            peca_foto: produto.fotos && produto.fotos.length > 0 ? produto.fotos[0].imagem : null,
            quantidade: quantidade,
            preco_unitario: parseFloat(produto.preco),
            subtotal: quantidade * parseFloat(produto.preco),
            estoque_disponivel: produto.estoque
          };

          itensCarrinho.value.push(novoItem);
        }

        salvarLocalStorage();
        return { sucesso: true, mensagem: 'Produto adicionado ao carrinho!' };
      }
    } catch (error) {
      console.error('Erro ao adicionar ao carrinho:', error);
      return { sucesso: false, mensagem: error.response?.data?.error || 'Erro ao adicionar produto' };
    } finally {
      carregandoCarrinho.value = false;
    }
  };

  /**
   * Atualiza quantidade de um item
   */
  const atualizarQuantidade = async (itemId, novaQuantidade) => {
    carregandoCarrinho.value = true;

    try {
      if (usuarioLogado.value) {
        // Usuário logado: usa API
        if (novaQuantidade <= 0) {
          await api.delete(`/carrinho/${itemId}/`);
        } else {
          await api.patch(`/carrinho/${itemId}/atualizar_quantidade/`, {
            quantidade: novaQuantidade
          });
        }
        await carregarCarrinho();
      } else {
        // Usuário anônimo: usa localStorage
        if (novaQuantidade <= 0) {
          itensCarrinho.value = itensCarrinho.value.filter(item => item.id !== itemId);
        } else {
          const item = itensCarrinho.value.find(i => i.id === itemId);
          if (item) {
            if (novaQuantidade > item.estoque_disponivel) {
              throw new Error(`Estoque insuficiente. Disponível: ${item.estoque_disponivel}`);
            }
            item.quantidade = novaQuantidade;
            item.subtotal = item.quantidade * parseFloat(item.preco_unitario);
          }
        }
        salvarLocalStorage();
      }

      return { sucesso: true };
    } catch (error) {
      console.error('Erro ao atualizar quantidade:', error);
      return { sucesso: false, mensagem: error.message || 'Erro ao atualizar quantidade' };
    } finally {
      carregandoCarrinho.value = false;
    }
  };

  /**
   * Remove item do carrinho
   */
  const removerItem = async (itemId) => {
    return await atualizarQuantidade(itemId, 0);
  };

  /**
   * Limpa todo o carrinho
   */
  const limparCarrinho = async () => {
    carregandoCarrinho.value = true;

    try {
      if (usuarioLogado.value) {
        await api.delete('/carrinho/limpar/');
      } else {
        itensCarrinho.value = [];
        localStorage.removeItem('carrinho');
      }

      return { sucesso: true };
    } catch (error) {
      console.error('Erro ao limpar carrinho:', error);
      return { sucesso: false };
    } finally {
      carregandoCarrinho.value = false;
    }
  };

  /**
   * Migra carrinho do localStorage para o backend após login
   */
  const migrarCarrinhoApoLogin = async () => {
    const carrinhoLocal = localStorage.getItem('carrinho');
    if (!carrinhoLocal) return;

    const itensLocal = JSON.parse(carrinhoLocal);
    if (itensLocal.length === 0) return;

    try {
      // Converte formato localStorage para formato API
      const itensParaMigrar = itensLocal.map(item => ({
        peca_id: item.peca,
        quantidade: item.quantidade
      }));

      await api.post('/carrinho/migrar_carrinho/', {
        itens: itensParaMigrar
      });

      // Limpa localStorage após migração
      localStorage.removeItem('carrinho');
      
      // Recarrega carrinho do backend
      await carregarCarrinho();

      return { sucesso: true, mensagem: 'Carrinho sincronizado!' };
    } catch (error) {
      console.error('Erro ao migrar carrinho:', error);
      return { sucesso: false, mensagem: 'Erro ao sincronizar carrinho' };
    }
  };

  /**
   * Valida estoque de todos os itens
   */
  const validarEstoque = async () => {
    try {
      if (usuarioLogado.value) {
        const response = await api.post('/carrinho/validar_estoque/');
        return { valido: response.data.valid, erros: response.data.erros || [] };
      } else {
        // Para localStorage, valida manualmente
        const erros = [];
        
        for (const item of itensCarrinho.value) {
          if (item.quantidade > item.estoque_disponivel) {
            erros.push({
              peca: item.peca_nome,
              solicitado: item.quantidade,
              disponivel: item.estoque_disponivel
            });
          }
        }

        return { valido: erros.length === 0, erros };
      }
    } catch (error) {
      console.error('Erro ao validar estoque:', error);
      return { valido: false, erros: [] };
    }
  };

  /**
   * Abre/fecha drawer do carrinho
   */
  const toggleDrawer = () => {
    drawerAberto.value = !drawerAberto.value;
  };

  const abrirDrawer = () => {
    drawerAberto.value = true;
  };

  const fecharDrawer = () => {
    drawerAberto.value = false;
  };

  return {
    // Estado
    itensCarrinho,
    carregandoCarrinho,
    drawerAberto,
    
    // Computed
    totalItens,
    totalPreco,
    temItens,
    usuarioLogado,
    
    // Métodos
    carregarCarrinho,
    adicionarAoCarrinho,
    atualizarQuantidade,
    removerItem,
    limparCarrinho,
    migrarCarrinhoApoLogin,
    validarEstoque,
    toggleDrawer,
    abrirDrawer,
    fecharDrawer
  };
}
