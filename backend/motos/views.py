from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Moto, Peca
from .serializers import MotoSerializer, PecaSerializer
from clientes.group_permissions import HasGroupPermission, IsAdminGroup

class MotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Motos
    
    Otimizado com select_related para evitar N+1 queries
    """
    serializer_class = MotoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        """
        Retorna queryset otimizado com select_related
        Evita N+1 queries ao acessar moto.cliente
        """
        queryset = Moto.objects.select_related('cliente').all()
        
        # Filtrar por cliente se fornecido
        cliente_id = self.request.query_params.get('cliente_id')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Verifica limites do plano antes de criar moto"""
        # Verificar se o usuário pode criar mais motos
        user_subscription = getattr(request.user, 'subscription', None)
        if user_subscription and user_subscription.plan:
            total_motos = Moto.objects.count()
            if total_motos >= user_subscription.plan.max_motos:
                return Response(
                    {
                        'error': f'Limite de {user_subscription.plan.max_motos} motos atingido!',
                        'detail': 'Faça upgrade para o plano PRO para ter motos ilimitadas.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """Apenas admin pode criar, editar ou deletar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()

class PecaViewSet(viewsets.ModelViewSet):
    serializer_class = PecaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        marca = self.request.query_params.get('marca')
        modelo = self.request.query_params.get('modelo')
        ano = self.request.query_params.get('ano')
        
        queryset = Peca.objects.all()
        if marca:
            queryset = queryset.filter(marca_moto=marca)
        if modelo:
            queryset = queryset.filter(modelo_moto=modelo)
        if ano:
            queryset = queryset.filter(ano_moto=ano)
        
        return queryset

    def get_permissions(self):
        """Apenas admin pode criar, editar ou deletar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()

