from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Manutencao, Agendamento
from .serializers import ManutencaoSerializer, AgendamentoSerializer
from clientes.group_permissions import HasGroupPermission, IsAdminGroup

class ManutencaoViewSet(viewsets.ModelViewSet):
    serializer_class = ManutencaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        moto_id = self.request.query_params.get('moto_id')
        if moto_id:
            return Manutencao.objects.filter(moto_id=moto_id)
        return Manutencao.objects.all()

    def get_permissions(self):
        """Apenas admin pode deletar"""
        if self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()

class AgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        moto_id = self.request.query_params.get('moto_id')
        status = self.request.query_params.get('status')
        
        queryset = Agendamento.objects.all()
        if moto_id:
            queryset = queryset.filter(moto_id=moto_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

    def get_permissions(self):
        """Apenas admin pode deletar"""
        if self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()
