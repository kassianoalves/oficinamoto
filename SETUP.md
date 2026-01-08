# 🚀 GUIA DE INSTALAÇÃO - Oficina Moto

## Windows - Passo a Passo

### 1. Instalar Dependências

#### Python (Backend)
- Baixe Python 3.10+ em https://www.python.org/downloads/
- **Importante**: Marque "Add Python to PATH" durante instalação

#### Node.js (Frontend)
- Baixe Node.js LTS em https://nodejs.org/
- npm já vem incluído

Verifique as instalações:
```bash
python --version
node --version
npm --version
```

### 2. Preparar Backend

Abra PowerShell ou CMD na pasta `backend/`:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Fazer migrações do banco de dados
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser
# Preencha: username, email, password (2x)

# Iniciar servidor
python manage.py runserver
# Resultado: http://127.0.0.1:8000/
```

### 3. Preparar Frontend

Abra PowerShell ou CMD na pasta `frontend/`:

```bash
# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
# Resultado: http://127.0.0.1:5173/
```

### 4. Testar Sistema

Abra seu navegador:
- **Frontend**: http://127.0.0.1:5173
- **Backend**: http://127.0.0.1:8000/api/clientes/
- **Admin**: http://127.0.0.1:8000/admin

Faça login com o superusuário criado na etapa 2.

## ⚡ Forma Rápida (Automática)

Após primeira instalação, você pode usar:

```bash
# Windows (CMD/PowerShell)
start.bat
# ou
.\start.ps1
```

Isso abre os dois servidores automaticamente!

## 📍 Portas Padrão

| Serviço | URL | Porta |
|---------|-----|-------|
| Frontend | http://127.0.0.1:5173 | 5173 |
| Backend API | http://127.0.0.1:8000 | 8000 |
| Admin | http://127.0.0.1:8000/admin | 8000 |

Se a porta estiver em uso, Django muda automaticamente para 8001, 8002, etc.

## 🆘 Troubleshooting

### "venv não é reconhecido"
```bash
# Use o caminho completo
python -m venv venv
venv\Scripts\activate.bat
```

### "pip não é reconhecido"
```bash
# Use o Python do venv
venv\Scripts\pip.exe install -r requirements.txt
```

### "Port already in use"
```bash
# Backend em porta diferente
python manage.py runserver 8001

# Frontend em porta diferente
npm run dev -- --port 5174
```

### "CORS Error - Frontend não conecta Backend"
- Certifique-se que o backend está rodando
- Verifique `backend/oficinamoto_api/settings.py`
- Verifique que as URLs estão corretas em `frontend/src/api.js`

### "npm install falha"
```bash
# Limpar cache
npm cache clean --force
rm -r node_modules package-lock.json
npm install
```

## 🔄 Estrutura de Dados

### Fluxo de Uso:

1. **Cadastrar Cliente** (Clientes)
   - Nome, CPF, Telefone, Email, Endereço

2. **Registrar Moto** (Motos)
   - Seleciona o Cliente
   - Marca, Modelo, Ano, Placa, Série

3. **Agendar Manutenção** (Manutenções)
   - Seleciona a Moto
   - Tipo de Serviço, Data/Hora
   - Status: Pendente → Confirmado → Cancelado

4. **Consultar Histórico**
   - Por cliente ou por moto
   - Ver todas as manutenções realizadas

## 📱 Usando em Tablet

1. Abra http://127.0.0.1:5173 no navegador do tablet
2. Interface totalmente responsiva
3. Funciona em iPhone, iPad, Android tablets

Para compartilhar entre dispositivos:
```bash
# No terminal do Frontend, configure:
npm run dev -- --host
# Acesse de outro dispositivo:
# http://<seu-ip-do-pc>:5173
```

## 🎯 Próximas Etapas

Após ter tudo funcionando:
1. Consulte [README.md](./README.md) para mais detalhes
2. Etapa 2: Histórico de Manutenções
3. Etapa 3: Catálogo de Peças por Marca/Modelo
4. Etapa 4: PWA (funcionar offline)
5. Etapa 5: Deploy em servidor

## 📞 Dúvidas?

Verifique os logs:
- **Backend**: Consola do servidor Django
- **Frontend**: Console do navegador (F12 → Console)

---

**Sucesso na instalação! 🎉**
