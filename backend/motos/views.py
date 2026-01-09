from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Moto, Peca
from .serializers import MotoSerializer, PecaSerializer
from clientes.group_permissions import HasGroupPermission, IsAdminGroup

class MotoViewSet(viewsets.ModelViewSet):
    serializer_class = MotoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente_id')
        if cliente_id:
            return Moto.objects.filter(cliente_id=cliente_id)
        return Moto.objects.all()

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

