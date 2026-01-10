"""
========================================
MIDDLEWARE PERSONALIZADO
========================================
Middlewares customizados para a aplicação Oficina Moto
"""

from django.utils.deprecation import MiddlewareMixin


class CsrfExemptMiddleware(MiddlewareMixin):
    """
    Middleware para isentar endpoints específicos de autenticação da validação CSRF.
    
    IMPORTANTE: Apenas endpoints de autenticação inicial (login/registro) devem
    ser isentos. Endpoints que modificam dados de usuário autenticado DEVEM ter CSRF.
    
    Endpoints isentos:
    - /api/auth/login/ (POST - login de usuário)
    - /api/auth/register/ (POST - criação de conta)
    - /api/auth/forgot-password/ (POST - solicitação de reset de senha)
    - /api/auth/reset-password/ (POST - reset de senha com token)
    
    Endpoints que MANTÊM CSRF (segurança):
    - /api/auth/user/ (GET/PUT - dados do usuário autenticado)
    - /api/auth/logout/ (POST - logout)
    """
    
    # Lista de endpoints que NÃO requerem CSRF
    CSRF_EXEMPT_PATHS = [
        '/api/auth/login/',
        '/api/auth/register/',
        '/api/auth/forgot-password/',
        '/api/auth/reset-password/',
    ]
    
    def process_request(self, request):
        """
        Processa a requisição e decide se deve isentar de CSRF
        """
        # Verifica se o path está na lista de isentos
        for exempt_path in self.CSRF_EXEMPT_PATHS:
            if request.path == exempt_path:
                request._dont_enforce_csrf_checks = True
                return None
        
        # Todos os outros endpoints mantêm verificação CSRF
        return None


