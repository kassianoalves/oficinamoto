from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Cliente
from .serializers import ClienteSerializer
from .group_permissions import HasGroupPermission, IsAdminGroup

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]

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
