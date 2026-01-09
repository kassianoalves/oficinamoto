# 🏍️ Sistema de Gerenciamento de Oficina de Motos

Sistema completo e profissional para gerenciamento de oficinas de motocicletas, desenvolvido com Django REST Framework e Vue.js 3.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0+-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Funcionalidades

### 👥 Gestão de Clientes
- ✅ Cadastro completo com validação de CPF
- ✅ Máscara automática para CPF e telefone
- ✅ Busca e filtros em tempo real
- ✅ Histórico de manutenções por cliente

### 🏍️ Gestão de Motos
- ✅ Registro detalhado de motocicletas
- ✅ Validação de placas (formato brasileiro)
- ✅ Vinculação com proprietários
- ✅ Controle de ano e modelo

### 🔧 Manutenções e Agendamentos
- ✅ Agendamento de serviços
- ✅ Controle de status (Pendente, Confirmado, Cancelado)
- ✅ Tipos de serviço: Troca de Óleo, Reparo, Assistência, Vistoria
- ✅ Observações e histórico completo
- ✅ Filtros por status e data

### 🔐 Sistema de Autenticação
- ✅ Registro de usuários
- ✅ Login com token JWT
- ✅ Recuperação de senha por email
- ✅ Sistema de permissões (Admin/Funcionário)
- ✅ Controle de acesso granular

### 🎨 Interface Moderna
- ✅ Design responsivo e intuitivo
- ✅ Notificações toast elegantes
- ✅ Validações em tempo real
- ✅ Máscaras automáticas de input
- ✅ Feedback visual consistente

## 🚀 Tecnologias Utilizadas

### Backend
- **Django 6.0.1** - Framework web robusto
- **Django REST Framework 3.16.1** - API RESTful
- **SQLite** - Banco de dados (produção: PostgreSQL)
- **Token Authentication** - Autenticação segura

### Frontend
- **Vue.js 3** - Framework progressivo
- **Vue Router** - Gerenciamento de rotas
- **Axios** - Cliente HTTP
- **Vite 5.4** - Build tool rápido

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior
- Node.js 16+ e npm

### 1. Clone o repositório
```bash
git clone <repository-url>
cd oficinamoto
```

### 2. Configure o Backend

```bash
# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
cd oficinamoto/backend
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie grupos de permissões
python manage.py setup_groups

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

O backend estará disponível em: `http://127.0.0.1:8000`

### 3. Configure o Frontend

```bash
# Em outro terminal, navegue até o frontend
cd oficinamoto/frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

## 🔧 Configuração de Produção

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do backend:

```env
# Segurança
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# CORS
CORS_ORIGINS=https://seudominio.com

# Banco de Dados (PostgreSQL recomendado)
DATABASE_URL=postgres://usuario:senha@host:porta/nome_banco

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

### Deploy Backend (Django)

1. **Colete arquivos estáticos:**
```bash
python manage.py collectstatic --noinput
```

2. **Use o arquivo de settings de produção:**
```bash
export DJANGO_SETTINGS_MODULE=oficinamoto_api.settings_prod
```

3. **Configure um servidor WSGI:**
   - Gunicorn (recomendado)
   - uWSGI
   - mod_wsgi

Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn oficinamoto_api.wsgi:application --bind 0.0.0.0:8000
```

### Deploy Frontend (Vue.js)

1. **Build para produção:**
```bash
npm run build
```

2. **Configure o servidor web** (Nginx, Apache) para servir os arquivos do diretório `dist/`

Exemplo de configuração Nginx:
```nginx
server {
    listen 80;
    server_name seudominio.com;

    root /caminho/para/oficinamoto/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 👥 Sistema de Permissões

O sistema possui dois níveis de acesso:

### 🔑 Admin
- Acesso total ao sistema
- Pode criar, editar e deletar:
  - Clientes
  - Motos
  - Manutenções
  - Agendamentos
- Gerencia usuários e permissões

### 👤 Funcionário
- Acesso de leitura para:
  - Clientes
  - Motos
- Pode criar e editar:
  - Manutenções
  - Agendamentos
- Não pode deletar registros

## 📱 API Endpoints

### Autenticação
```
POST /api/auth/register/         - Registro de usuário
POST /api/auth/login/            - Login
POST /api/auth/logout/           - Logout
POST /api/auth/forgot-password/  - Solicitar recuperação de senha
POST /api/auth/reset-password/   - Resetar senha
GET  /api/auth/user/             - Dados do usuário atual
```

### Clientes
```
GET    /api/clientes/          - Listar clientes
POST   /api/clientes/          - Criar cliente
GET    /api/clientes/{id}/     - Detalhes do cliente
PUT    /api/clientes/{id}/     - Atualizar cliente
DELETE /api/clientes/{id}/     - Deletar cliente
```

### Motos
```
GET    /api/motos/             - Listar motos
POST   /api/motos/             - Registrar moto
GET    /api/motos/{id}/        - Detalhes da moto
PUT    /api/motos/{id}/        - Atualizar moto
DELETE /api/motos/{id}/        - Deletar moto
```

### Agendamentos
```
GET    /api/agendamentos/              - Listar agendamentos
POST   /api/agendamentos/              - Criar agendamento
GET    /api/agendamentos/{id}/         - Detalhes do agendamento
PUT    /api/agendamentos/{id}/         - Atualizar agendamento
DELETE /api/agendamentos/{id}/         - Cancelar agendamento
GET    /api/agendamentos/?status=...   - Filtrar por status
```

## 🧪 Testes

### Backend
```bash
python manage.py test
```

### Frontend
```bash
npm run test
```

## 📊 Estrutura do Projeto

```
oficinamoto/
├── backend/
│   ├── clientes/               # App de clientes
│   ├── motos/                  # App de motos
│   ├── manutencoes/            # App de manutenções
│   ├── oficinamoto_api/        # Configurações principais
│   ├── db.sqlite3              # Banco de dados (dev)
│   ├── manage.py               # Gerenciador Django
│   └── requirements.txt        # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/         # Componentes Vue
│   │   ├── views/              # Views/Páginas
│   │   ├── composables/        # Composables (useToast)
│   │   ├── router.js           # Rotas
│   │   ├── api.js              # Configuração Axios
│   │   └── App.vue             # Componente raiz
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através de:
- Email: suporte@oficinamoto.com
- Issues: [GitHub Issues](https://github.com/seu-usuario/oficinamoto/issues)

## 🎯 Roadmap

- [ ] Integração com WhatsApp para notificações
- [ ] Relatórios em PDF
- [ ] Dashboard com gráficos e estatísticas
- [ ] App mobile (React Native)
- [ ] Sistema de estoque de peças
- [ ] Integração com sistemas de pagamento

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!

Desenvolvido com ❤️ por [Seu Nome]
