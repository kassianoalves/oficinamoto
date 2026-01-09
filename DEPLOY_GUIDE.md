# 🚀 Guia Completo de Deploy - Oficina Moto

Este guia detalha o processo completo de deploy do sistema em um servidor de produção.

## 📋 Índice

1. [Preparação do Servidor](#preparação-do-servidor)
2. [Instalação de Dependências](#instalação-de-dependências)
3. [Configuração do Backend](#configuração-do-backend)
4. [Configuração do Frontend](#configuração-do-frontend)
5. [Configuração do Nginx](#configuração-do-nginx)
6. [SSL/HTTPS com Let's Encrypt](#ssl-https-com-lets-encrypt)
7. [Configuração do Systemd](#configuração-do-systemd)
8. [Backup e Monitoramento](#backup-e-monitoramento)

---

## 1. Preparação do Servidor

### Requisitos Mínimos
- **OS:** Ubuntu 20.04+ / Debian 11+
- **RAM:** 2GB (recomendado 4GB)
- **Disco:** 20GB
- **CPU:** 2 cores

### Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Criar Usuário (opcional, mas recomendado)
```bash
sudo adduser oficinamoto
sudo usermod -aG sudo oficinamoto
sudo su - oficinamoto
```

---

## 2. Instalação de Dependências

### Python e Pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### Node.js e npm
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### PostgreSQL (Recomendado para Produção)
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Nginx
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Certbot (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Git
```bash
sudo apt install git -y
```

---

## 3. Configuração do Backend

### Clonar Repositório
```bash
cd /var/www
sudo git clone <seu-repositorio> oficinamoto
sudo chown -R $USER:$USER /var/www/oficinamoto
cd /var/www/oficinamoto
```

### Criar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar Dependências Python
```bash
cd backend
pip install -r requirements.txt
pip install gunicorn psycopg2-binary dj-database-url python-decouple
```

### Configurar Banco de Dados PostgreSQL
```bash
sudo -u postgres psql

# No prompt do PostgreSQL:
CREATE DATABASE oficinamoto_db;
CREATE USER oficinamoto_user WITH PASSWORD 'senha_forte_aqui';
ALTER ROLE oficinamoto_user SET client_encoding TO 'utf8';
ALTER ROLE oficinamoto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE oficinamoto_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE oficinamoto_db TO oficinamoto_user;
\q
```

### Criar Arquivo .env
```bash
cd /var/www/oficinamoto/backend
nano .env
```

Adicione:
```env
# Django
SECRET_KEY=gere-uma-chave-secreta-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DJANGO_SETTINGS_MODULE=oficinamoto_api.settings_prod

# CORS
CORS_ORIGINS=https://seudominio.com,https://www.seudominio.com

# Database
DATABASE_URL=postgres://oficinamoto_user:senha_forte_aqui@localhost:5432/oficinamoto_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

**Gerar SECRET_KEY:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Executar Migrações
```bash
source /var/www/oficinamoto/.venv/bin/activate
cd /var/www/oficinamoto/backend
export DJANGO_SETTINGS_MODULE=oficinamoto_api.settings_prod
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Testar Backend
```bash
gunicorn oficinamoto_api.wsgi:application --bind 127.0.0.1:8000
# Ctrl+C para parar
```

---

## 4. Configuração do Frontend

### Build do Frontend
```bash
cd /var/www/oficinamoto/frontend
npm install
npm run build
```

Os arquivos de produção estarão em `/var/www/oficinamoto/frontend/dist`

### Configurar API URL (se necessário)
Antes do build, edite `frontend/src/api.js` se a API estiver em domínio diferente:
```javascript
const api = axios.create({
  baseURL: 'https://api.seudominio.com/api',  // Ajustar se necessário
  // ...
})
```

---

## 5. Configuração do Nginx

### Copiar Arquivo de Configuração
```bash
sudo cp /var/www/oficinamoto/nginx.conf /etc/nginx/sites-available/oficinamoto
```

### Editar Configuração
```bash
sudo nano /etc/nginx/sites-available/oficinamoto
```

Substitua `seudominio.com` pelo seu domínio real.

### Ativar Site
```bash
sudo ln -s /etc/nginx/sites-available/oficinamoto /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove site padrão
```

### Testar Configuração
```bash
sudo nginx -t
```

### Reiniciar Nginx
```bash
sudo systemctl restart nginx
```

---

## 6. SSL/HTTPS com Let's Encrypt

### Obter Certificado
```bash
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

Siga as instruções interativas. Escolha redirecionar HTTP para HTTPS.

### Renovação Automática
```bash
sudo certbot renew --dry-run  # Testar renovação
```

O Certbot cria um cron job automático para renovação.

---

## 7. Configuração do Systemd

### Criar Diretório de Logs
```bash
sudo mkdir -p /var/log/oficinamoto
sudo chown -R www-data:www-data /var/log/oficinamoto
```

### Copiar Service File
```bash
sudo cp /var/www/oficinamoto/oficinamoto.service /etc/systemd/system/
```

### Ajustar Permissões
```bash
sudo chown -R www-data:www-data /var/www/oficinamoto
```

### Iniciar Serviço
```bash
sudo systemctl daemon-reload
sudo systemctl start oficinamoto
sudo systemctl enable oficinamoto
```

### Verificar Status
```bash
sudo systemctl status oficinamoto
```

### Ver Logs
```bash
sudo journalctl -u oficinamoto -f
```

---

## 8. Backup e Monitoramento

### Script de Backup Automático
```bash
sudo nano /usr/local/bin/backup-oficinamoto.sh
```

Adicione:
```bash
#!/bin/bash
BACKUP_DIR="/backup/oficinamoto"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup banco de dados
sudo -u postgres pg_dump oficinamoto_db > $BACKUP_DIR/db_$DATE.sql

# Backup arquivos
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /var/www/oficinamoto

# Manter apenas últimos 7 dias
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
sudo chmod +x /usr/local/bin/backup-oficinamoto.sh
```

### Agendar Backup Diário
```bash
sudo crontab -e
```

Adicione:
```
0 2 * * * /usr/local/bin/backup-oficinamoto.sh >> /var/log/backup-oficinamoto.log 2>&1
```

### Monitoramento com Logs
```bash
# Ver logs do Django
tail -f /var/log/oficinamoto/error.log

# Ver logs do Nginx
tail -f /var/log/nginx/oficinamoto_error.log

# Ver logs do Systemd
journalctl -u oficinamoto -f
```

---

## 🔧 Comandos Úteis

### Reiniciar Serviços
```bash
sudo systemctl restart oficinamoto  # Backend
sudo systemctl restart nginx         # Webserver
```

### Atualizar Código
```bash
cd /var/www/oficinamoto
git pull
source .venv/bin/activate

# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart oficinamoto

# Frontend
cd ../frontend
npm install
npm run build
```

### Ver Logs em Tempo Real
```bash
sudo journalctl -u oficinamoto -f
```

### Verificar Uso de Recursos
```bash
htop
df -h
free -h
```

---

## 🔐 Segurança

### Firewall
```bash
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw enable
```

### Fail2ban (Proteção contra brute-force)
```bash
sudo apt install fail2ban -y
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### Atualizar Sistema Regularmente
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 📞 Troubleshooting

### Backend não inicia
```bash
# Verificar logs
sudo journalctl -u oficinamoto -n 50

# Verificar variáveis de ambiente
cat /var/www/oficinamoto/backend/.env

# Testar manualmente
cd /var/www/oficinamoto/backend
source ../.venv/bin/activate
gunicorn oficinamoto_api.wsgi:application
```

### Nginx retorna 502 Bad Gateway
```bash
# Verificar se o backend está rodando
sudo systemctl status oficinamoto

# Verificar logs do Nginx
sudo tail -f /var/log/nginx/oficinamoto_error.log
```

### Problemas com Permissões
```bash
sudo chown -R www-data:www-data /var/www/oficinamoto
sudo chmod -R 755 /var/www/oficinamoto
```

---

## ✅ Checklist Final

- [ ] Servidor atualizado
- [ ] Dependências instaladas
- [ ] Banco de dados configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Frontend buildado
- [ ] Nginx configurado
- [ ] SSL/HTTPS ativo
- [ ] Systemd service ativo
- [ ] Firewall configurado
- [ ] Backups agendados
- [ ] Monitoramento configurado
- [ ] Testes de funcionalidade realizados

---

Desenvolvido com ❤️ para sua oficina de motos!
