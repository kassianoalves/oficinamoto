from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view

from clientes.views import ClienteViewSet, ProdutoLojaViewSet
from clientes.auth_views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView, UserDetailView, LogoutView
from motos.views import MotoViewSet, PecaViewSet
from manutencoes.views import ManutencaoViewSet, AgendamentoViewSet, LembreteViewSet, PontosFidelidadeViewSet, PecaViewSet as PecaManuViewSet, ItemAgendamentoViewSet

# View para retornar a URL da API dinamicamente
@api_view(['GET'])
def get_api_config(request):
    """
    Retorna informações de configuração da API incluindo:
    - URL base da API
    - IP local detectado
    - Host da requisição
    """
    from oficinamoto_api.settings import get_local_ip
    
    local_ip = get_local_ip()
    request_host = request.get_host()  # IP ou hostname + porta vindo da requisição
    
    # Detectar protocolo (http ou https)
    protocol = 'https' if request.is_secure() else 'http'
    
    # Construir URL da API baseado no host da requisição
    if ':' in request_host:
        host, port = request_host.rsplit(':', 1)
        api_url = f"{protocol}://{request_host}/api"
    else:
        api_url = f"{protocol}://{request_host}/api"
    
    return Response({
        'api_url': api_url,
        'local_ip': local_ip,
        'request_host': request_host,
        'protocol': protocol,
        'debug': settings.DEBUG,
    })

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'motos', MotoViewSet, basename='moto')
router.register(r'pecas', PecaManuViewSet, basename='peca')
router.register(r'itens-agendamento', ItemAgendamentoViewSet, basename='item-agendamento')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
router.register(r'lembretes', LembreteViewSet, basename='lembrete')
router.register(r'pontos-fidelidade', PontosFidelidadeViewSet, basename='pontos-fidelidade')
router.register(r'produtos-loja', ProdutoLojaViewSet, basename='produto-loja')


# Rotas de autenticação
auth_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/config/', get_api_config, name='api-config'),
    path('api/', include(router.urls)),
    path('api/auth/', include(auth_urls)),
    path('api/subscription/', include('clientes.subscription_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
