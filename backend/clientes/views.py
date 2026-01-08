from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas clientes ativos"""
        queryset = Cliente.objects.filter(ativo=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa um cliente"""
        cliente = self.get_object()
        cliente.ativo = False
        cliente.save()
        return Response({'status': 'cliente desativado'})
