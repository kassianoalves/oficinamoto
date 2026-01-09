from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from clientes.views import ClienteViewSet
from clientes.auth_views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView, UserDetailView, LogoutView
from motos.views import MotoViewSet, PecaViewSet
from manutencoes.views import ManutencaoViewSet, AgendamentoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'motos', MotoViewSet, basename='moto')
router.register(r'pecas', PecaViewSet, basename='peca')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')

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
    path('api/', include(router.urls)),
    path('api/auth/', include(auth_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
