<template>
  <div class="manuais-container">
    <div class="header">
      <h1>📚 Base de Manuais de Reparo</h1>
      <p class="subtitle">Acesso ao banco de dados com manuais de diferentes marcas de motos</p>
    </div>

    <!-- Filtros -->
    <div class="filtros">
      <input
        v-model="filtroMarca"
        type="text"
        placeholder="🔍 Buscar por marca..."
        class="filter-input"
      />
      <select v-model="filtroTipo" class="filter-select">
        <option value="">Todos os Tipos de Reparo</option>
        <option value="motor">Motor</option>
        <option value="transmissao">Transmissão</option>
        <option value="freios">Freios</option>
        <option value="suspensao">Suspensão</option>
        <option value="eletrica">Elétrica</option>
        <option value="carroceria">Carroceria</option>
        <option value="manutencao">Manutenção</option>
      </select>
      <button @click="buscarManuais" class="btn-buscar">Buscar</button>
    </div>

    <!-- Loading -->
    <div v-if="carregando" class="loading">
      <p>Carregando manuais...</p>
    </div>

    <!-- Lista de Manuais -->
    <div v-else-if="manuaisFiltrados.length > 0" class="manuais-grid">
      <div v-for="manual in manuaisFiltrados" :key="manual.id" class="manual-card">
        <div class="card-header">
          <h3>{{ manual.marca }} {{ manual.modelo }}</h3>
          <span class="ano">{{ manual.ano }}</span>
        </div>

        <div class="card-body">
          <p class="tipo-reparo">
            <strong>Tipo:</strong> {{ manual.tipo_reparo }}
          </p>
          <p class="descricao">{{ manual.descricao }}</p>

          <div class="detalhes">
            <span class="dificuldade" :class="`dif-${manual.dificuldade}`">
              {{ nivelDificuldade(manual.dificuldade) }}
            </span>
            <span v-if="manual.tempo_estimado" class="tempo">
              ⏱️ {{ manual.tempo_estimado }}
            </span>
          </div>

          <div v-if="manual.ferramentas_necessarias" class="ferramentas">
            <strong>Ferramentas:</strong> {{ manual.ferramentas_necessarias }}
          </div>
        </div>

        <div class="card-footer">
          <a
            v-if="manual.arquivo_pdf"
            :href="manual.arquivo_pdf"
            target="_blank"
            class="btn-download"
          >
            📥 Baixar PDF
          </a>
          <a
            v-if="manual.url_externo"
            :href="manual.url_externo"
            target="_blank"
            class="btn-link"
          >
            🔗 Ver Manual Online
          </a>
        </div>
      </div>
    </div>

    <!-- Sem resultados -->
    <div v-else class="empty-state">
      <p>Nenhum manual encontrado</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import api from '../api.js';

export default {
  name: 'ManuaisView',
  setup() {
    const manuais = ref([]);
    const carregando = ref(false);
    const filtroMarca = ref('');
    const filtroTipo = ref('');

    const manuaisFiltrados = computed(() => {
      return manuais.value.filter(manual => {
        const matchMarca = manual.marca.toLowerCase().includes(filtroMarca.value.toLowerCase());
        const matchTipo = !filtroTipo.value || manual.tipo_reparo === filtroTipo.value;
        return matchMarca && matchTipo;
      });
    });

    const buscarManuais = async () => {
      carregando.value = true;
      try {
        const response = await api.get('/manuais/');
        manuais.value = response.data.results || response.data;
      } catch (error) {
        console.error('Erro ao carregar manuais:', error);
        alert('Erro ao carregar manuais. Tente novamente.');
      } finally {
        carregando.value = false;
      }
    };

    const nivelDificuldade = (nivel) => {
      const niveis = {
        facil: '🟢 Fácil',
        medio: '🟡 Médio',
        dificil: '🔴 Difícil',
        muito_dificil: '⚫ Muito Difícil'
      };
      return niveis[nivel] || nivel;
    };

    // Carregar manuais na montagem
    buscarManuais();

    return {
      manuais,
      carregando,
      filtroMarca,
      filtroTipo,
      manuaisFiltrados,
      buscarManuais,
      nivelDificuldade
    };
  }
};
</script>

<style scoped>
.manuais-container {
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
  margin-bottom: 30px;
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
  min-width: 180px;
}

.btn-buscar {
  padding: 10px 25px;
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s;
}

.btn-buscar:hover {
  transform: translateY(-2px);
}

/* Grid de manuais */
.manuais-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.manual-card {
  background: white;
  border: 2px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.manual-card:hover {
  border-color: #ff6b35;
  box-shadow: 0 5px 20px rgba(255, 107, 53, 0.1);
  transform: translateY(-5px);
}

.card-header {
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.3em;
}

.ano {
  background: rgba(255, 255, 255, 0.3);
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.9em;
}

.card-body {
  padding: 15px;
  flex: 1;
}

.tipo-reparo {
  background: #f5f5f5;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 0 0 10px 0;
  font-size: 0.95em;
}

.descricao {
  color: #666;
  line-height: 1.5;
  margin: 10px 0;
}

.detalhes {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}

.dificuldade {
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.85em;
  font-weight: bold;
}

.dif-facil {
  background: #d4edda;
  color: #155724;
}

.dif-medio {
  background: #fff3cd;
  color: #856404;
}

.dif-dificil {
  background: #f8d7da;
  color: #721c24;
}

.dif-muito_dificil {
  background: #6c757d;
  color: white;
}

.tempo {
  padding: 5px 10px;
  background: #e7f3ff;
  border-radius: 6px;
  font-size: 0.85em;
  color: #004085;
}

.ferramentas {
  background: #f9f9f9;
  padding: 10px;
  border-left: 4px solid #ff6b35;
  margin-top: 10px;
  font-size: 0.9em;
}

.card-footer {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-download,
.btn-link {
  flex: 1;
  padding: 10px;
  text-align: center;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9em;
  transition: all 0.3s;
  min-width: 120px;
}

.btn-download {
  background: linear-gradient(135deg, #ff6b35 0%, #f7b32b 100%);
  color: white;
  font-weight: bold;
}

.btn-download:hover {
  opacity: 0.9;
  transform: scale(1.02);
}

.btn-link {
  background: #e9ecef;
  color: #333;
}

.btn-link:hover {
  background: #dee2e6;
}

/* Estados */
.loading,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 1.1em;
}

/* Responsive */
@media (max-width: 768px) {
  .manuais-grid {
    grid-template-columns: 1fr;
  }

  .filtros {
    flex-direction: column;
  }

  .filter-input,
  .filter-select {
    width: 100%;
  }

  .header h1 {
    font-size: 1.8em;
  }

  .card-footer {
    flex-direction: column;
  }

  .btn-download,
  .btn-link {
    flex: 1;
  }
}
</style>
