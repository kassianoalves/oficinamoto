from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Manutencao, Agendamento
from .serializers import ManutencaoSerializer, AgendamentoSerializer

class ManutencaoViewSet(viewsets.ModelViewSet):
    serializer_class = ManutencaoSerializer
    
    def get_queryset(self):
        moto_id = self.request.query_params.get('moto_id')
        if moto_id:
            return Manutencao.objects.filter(moto_id=moto_id)
        return Manutencao.objects.all()

class AgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer
    
    def get_queryset(self):
        moto_id = self.request.query_params.get('moto_id')
        status = self.request.query_params.get('status')
        
        queryset = Agendamento.objects.all()
        if moto_id:
            queryset = queryset.filter(moto_id=moto_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
