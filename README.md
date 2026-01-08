# 🏍️ Oficina Moto - Sistema de Gerenciamento

Sistema completo de gerenciamento para oficinas de motos, desenvolvido com Django REST Framework e Vue.js 3.

## 🚀 Início Rápido

**Execute o script na raiz do projeto pai:**
```bash
P:\Python\oficinamoto\INICIAR_SERVIDORES.bat
```

Esse script iniciará automaticamente o backend e frontend em janelas separadas.

## 📦 Tecnologias

- **Backend:** Django 6.0.1 + Django REST Framework 3.16.1
- **Frontend:** Vue 3 + Vite 5.4.21
- **Banco de Dados:** SQLite3
- **Python:** 3.14.2

## 🔗 Acessos

- **Frontend:** http://localhost:5174
- **API Backend:** http://127.0.0.1:8000/api/
- **Admin Django:** http://127.0.0.1:8000/admin

## 👤 Credenciais Admin

- **Usuário:** kassiano
- **Senha:** admin123

## 📚 Funcionalidades

- ✅ Gerenciamento de Clientes (CRUD completo)
- ✅ Cadastro de Motos por Cliente
- ✅ Controle de Manutenções e Peças
- ✅ Sistema de Agendamento
- ✅ Interface Vue.js responsiva
- ✅ API RESTful documentada

## 🛠️ Instalação Manual

Se precisar configurar do zero, consulte [SETUP.md](SETUP.md) para instruções detalhadas.

## 📁 Estrutura do Projeto

```
oficinamoto/
├── backend/          # Django + DRF
│   ├── clientes/     # App de clientes
│   ├── motos/        # App de motos
│   ├── manutencoes/  # App de manutenções
│   └── db.sqlite3    # Banco de dados
├── frontend/         # Vue.js + Vite
│   └── src/
│       ├── views/    # Componentes de página
│       └── api.js    # Configuração API
├── README.md         # Este arquivo
└── SETUP.md          # Guia de instalação
```

## 🔧 Comandos Úteis

### Backend
```bash
cd oficinamoto/backend
python manage.py migrate              # Aplicar migrações
python manage.py createsuperuser      # Criar novo admin
python manage.py runserver            # Iniciar servidor
```

### Frontend
```bash
cd oficinamoto/frontend
npm install                           # Instalar dependências
npm run dev                           # Servidor desenvolvimento
npm run build                         # Build produção
```

## 📝 API Endpoints

- `GET/POST /api/clientes/` - Listar/criar clientes
- `GET/PUT/DELETE /api/clientes/{id}/` - Cliente específico
- `GET/POST /api/motos/` - Listar/criar motos
- `GET/POST /api/manutencoes/` - Listar/criar manutenções
- `GET/POST /api/agendamentos/` - Listar/criar agendamentos
- `GET/POST /api/pecas/` - Listar/criar peças

## 💡 Suporte

Para problemas ou dúvidas, consulte a documentação em SETUP.md ou verifique os logs no terminal.
