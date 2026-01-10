import os
from pathlib import Path
import socket
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================================
# CONFIGURAÇÕES DE SEGURANÇA
# ========================================
# IMPORTANTE: Nunca exponha SECRET_KEY ou credenciais no código!
# Use variáveis de ambiente (.env) para valores sensíveis

# Secret Key - OBRIGATÓRIO em produção
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-only-key-CHANGE-IN-PRODUCTION')

# Debug Mode - SEMPRE False em produção
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ========================================
# HOSTS PERMITIDOS
# ========================================
def get_allowed_hosts():
    """
    Gera lista de hosts permitidos automaticamente
    Em desenvolvimento: detecta e aceita localhost, IP local, hostname, e wildcard
    Em produção: APENAS hosts definidos em .env
    """
    env_hosts = os.getenv('ALLOWED_HOSTS', '')
    
    if env_hosts:
        # Produção: usar apenas hosts do .env
        return [host.strip() for host in env_hosts.split(',') if host.strip()]
    
    # Desenvolvimento: detectar automaticamente
    # Começar com hosts base + wildcard para aceitar qualquer request em DEBUG
    hosts = ['127.0.0.1', 'localhost', '192.168.1.99']
    
    if DEBUG:
        # Sempre aceitar wildcard em DEBUG
        hosts.append('*')
        
        # Detectar hostname
        try:
            hostname = socket.gethostname()
            if hostname and hostname not in hosts:
                hosts.append(hostname)
        except Exception as e:
            print(f"Aviso: Não foi possível detectar hostname: {e}")
        
        # Detectar IP local
        try:
            # Método 1: Conectar a socket UDP externo (sem enviar dados)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            if local_ip and local_ip not in hosts and local_ip != '127.0.0.1':
                hosts.append(local_ip)
                print(f"✓ IP Local detectado: {local_ip}")
        except Exception as e:
            print(f"Aviso: Não foi possível detectar IP local (Método 1): {e}")
            
            # Método 2: Fallback - usar hostname
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
                if local_ip and local_ip not in hosts and local_ip != '127.0.0.1':
                    hosts.append(local_ip)
                    print(f"✓ IP Local detectado (fallback): {local_ip}")
            except Exception as e2:
                print(f"Aviso: Fallback também falhou: {e2}")
    
    return list(set(hosts))

def get_local_ip():
    """
    Retorna o IP local da máquina
    Usado para comunicação entre frontend e backend
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return '127.0.0.1'

ALLOWED_HOSTS = get_allowed_hosts()

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'clientes',
    'motos',
    'manutencoes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oficinamoto_api.middleware.CsrfExemptMiddleware',
]

ROOT_URLCONF = 'oficinamoto_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'oficinamoto_api.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================================
# CONFIGURAÇÕES DE CORS
# ========================================
# Cross-Origin Resource Sharing para permitir frontend acessar backend

# Em desenvolvimento, permitir todas as origens
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Em produção, usar apenas origens específicas
    CORS_ALLOW_ALL_ORIGINS = False
    cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True

# ========================================
# CONFIGURAÇÕES DE EMAIL (SMTP)
# ========================================
# IMPORTANTE: Nunca exponha credenciais de email!
# Configure no arquivo .env

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# ========================================
# DJANGO REST FRAMEWORK
# ========================================
REST_FRAMEWORK = {
    # Renderizadores - JSON apenas (remove browsable API em produção)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
    # Autenticação padrão
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    
    # Permissões padrão (requer autenticação)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Paginação
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    
    # Rate Limiting (Proteção contra abuso)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',    # Usuários anônimos: 100 requests/hora
        'user': '1000/hour',   # Usuários autenticados: 1000 requests/hora
    }
}

