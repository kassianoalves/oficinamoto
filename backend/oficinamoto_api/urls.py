from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from clientes.views import ClienteViewSet
from motos.views import MotoViewSet, PecaViewSet
from manutencoes.views import ManutencaoViewSet, AgendamentoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'motos', MotoViewSet, basename='moto')
router.register(r'pecas', PecaViewSet, basename='peca')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
