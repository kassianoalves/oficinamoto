from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Cliente, ProdutoLoja, Imagem3D, ManualsBase
from .serializers import ClienteSerializer, ProdutoLojaSerializer, Imagem3DSerializer, ManualsBaseSerializer
from .group_permissions import HasGroupPermission, IsAdminGroup

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]

    def create(self, request, *args, **kwargs):
        """Verifica limites antes de criar cliente"""
        # Verificar se o usuário pode criar mais clientes
        user_subscription = getattr(request.user, 'subscription', None)
        if user_subscription and user_subscription.plan:
            total_clientes = Cliente.objects.filter(ativo=True).count()
            if total_clientes >= user_subscription.plan.max_clientes:
                return Response(
                    {
                        'error': f'Limite de {user_subscription.plan.max_clientes} clientes atingido!',
                        'detail': 'Faça upgrade para o plano PRO para ter clientes ilimitados.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """
        Define permissões por ação:
        - GET (list, retrieve, ativos): todos autenticados
        - POST, PUT, PATCH, DELETE: apenas admin
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'desativar']:
            # Apenas admin pode modificar
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            # Qualquer um autenticado pode visualizar
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas clientes ativos"""
        queryset = Cliente.objects.filter(ativo=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa um cliente (apenas admin)"""
        cliente = self.get_object()
        cliente.ativo = False
        cliente.save()

class ProdutoLojaViewSet(viewsets.ModelViewSet):
    """ViewSet para Produtos da Loja (Enterprise)"""
    serializer_class = ProdutoLojaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Cada usuário vê apenas seus próprios produtos"""
        return ProdutoLoja.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Cria um novo produto (automático user=request.user)"""
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Define automaticamente o user como request.user"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Atualiza o produto se pertencer ao usuário"""
        if serializer.instance.user != self.request.user:
            return Response(
                {'error': 'Você não pode editar um produto que não é seu'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Deleta o produto se pertencer ao usuário"""
        if instance.user != self.request.user:
            return Response(
                {'error': 'Você não pode deletar um produto que não é seu'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class Imagem3DViewSet(viewsets.ModelViewSet):
    """ViewSet para Imagens 3D das Motos (Enterprise)"""
    serializer_class = Imagem3DSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna imagens das motos do usuário"""
        from motos.models import Moto
        usuario_motos = Moto.objects.filter(cliente__user=self.request.user)
        return Imagem3D.objects.filter(moto__in=usuario_motos)


class ManualsBaseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet apenas leitura para Base de Manuais (disponível para todos)"""
    queryset = ManualsBase.objects.filter(ativo=True)
    serializer_class = ManualsBaseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Apenas admin pode criar/editar/deletar manuais"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def por_marca(self, request):
        """Filtro por marca de moto"""
        marca = request.query_params.get('marca', None)
        if marca:
            queryset = self.get_queryset().filter(marca=marca)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_tipo_reparo(self, request):
        """Filtro por tipo de reparo"""
        tipo = request.query_params.get('tipo', None)
        if tipo:
            queryset = self.get_queryset().filter(tipo_reparo=tipo)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)