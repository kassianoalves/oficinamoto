from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Moto, Peca
from .serializers import MotoSerializer, PecaSerializer

class MotoViewSet(viewsets.ModelViewSet):
    serializer_class = MotoSerializer
    
    def get_queryset(self):
        cliente_id = self.request.query_params.get('cliente_id')
        if cliente_id:
            return Moto.objects.filter(cliente_id=cliente_id)
        return Moto.objects.all()

class PecaViewSet(viewsets.ModelViewSet):
    serializer_class = PecaSerializer
    
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
