# 🏍️ Oficina Moto - Sistema de Gerenciamento

Sistema completo de gerenciamento de clientes e motos para oficinas, construído com **Vue 3 + Vite** (frontend) e **Django REST Framework** (backend).

## 📋 Requisitos

- **Python 3.8+** com pip
- **Node.js 16+** com npm
- **SQLite** (incluído no Python)

## 🚀 Instalação Rápida

### 1️⃣ Backend Setup

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Fazer migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
# Servidor em: http://127.0.0.1:8000
# Admin em: http://127.0.0.1:8000/admin
```

### 2️⃣ Frontend Setup

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
# Acessar em: http://127.0.0.1:5173
```

## 📱 Funcionalidades Atuais (Etapa 1)

✅ **Gerenciamento de Clientes**
- Adicionar, editar e deletar clientes
- Campos: Nome, CPF, Email, Telefone, Endereço, Cidade

✅ **Cadastro de Motos**
- Vincular motos aos clientes
- Campos: Marca, Modelo, Ano, Cor, Placa, Série

✅ **Agendamento de Manutenções**
- Agendar manutenções periódicas
- Tipos: Troca de Óleo, Reparo, Assistência, Vistoria
- Status: Pendente, Confirmado, Cancelado

✅ **Dashboard Inicial**
- Total de clientes, motos e agendamentos
- Acesso rápido aos módulos

## 🗂️ Estrutura do Projeto

```
oficinamoto/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3 (criado após migrate)
│   ├── oficinamoto_api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── clientes/
│   ├── motos/
│   └── manutencoes/
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.js
        ├── App.vue
        ├── api.js
        ├── router.js
        └── views/
            ├── HomeView.vue
            ├── ClientesView.vue
            ├── MotosView.vue
            └── ManutencaoView.vue
```

## 🔌 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/clientes/` | Listar clientes |
| POST | `/api/clientes/` | Criar cliente |
| PUT | `/api/clientes/{id}/` | Atualizar cliente |
| DELETE | `/api/clientes/{id}/` | Deletar cliente |
| GET | `/api/motos/` | Listar motos |
| POST | `/api/motos/` | Criar moto |
| GET | `/api/agendamentos/` | Listar agendamentos |
| POST | `/api/agendamentos/` | Criar agendamento |

## 🎨 Design Responsivo

A interface é completamente responsiva e otimizada para tablets:
- Cards adaptáveis
- Grid fluido
- Toque amigável
- Navegação intuitiva

## 🔮 Próximas Etapas

**Etapa 2:** Registro de Histórico de Manutenções
- Visualizar manutenções realizadas por moto
- Custos e peças utilizadas

**Etapa 3:** Banco de Dados de Peças
- Catálogo por marca/modelo/ano
- Consultar componentes da moto

**Etapa 4:** Relatórios e Análises
- Manutenções por período
- Clientes mais antigos
- Faturamento

**Etapa 5:** PWA e Offline
- Funcionamento sem internet
- Sincronização automática

**Etapa 6:** Deploy em Servidor
- Hospedagem na nuvem
- Backup automático
- Versão pró com mais recursos

## 🐛 Troubleshooting

**Frontend não conecta no Backend:**
- Certifique-se que backend está rodando em `http://127.0.0.1:8000`
- Verifique CORS em `backend/oficinamoto_api/settings.py`

**Erro de migrate:**
```bash
python manage.py migrate clientes
python manage.py migrate motos
python manage.py migrate manutencoes
```

**Porta 8000 ou 5173 já em uso:**
```bash
# Backend em porta diferente
python manage.py runserver 8001

# Frontend em porta diferente
npm run dev -- --port 5174
```

## 📄 Licença

Desenvolvido para uso em oficinas de motos.

---

**Desenvolvido com ❤️ usando Vue.js e Django**
