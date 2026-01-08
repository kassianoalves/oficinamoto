from rest_framework import serializers
from .models import Manutencao, Agendamento

class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = ['id', 'moto', 'tipo_servico', 'descricao', 'data_manutencao', 'data_proxima', 'custo', 'concluida', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'moto', 'tipo_servico', 'data_agendada', 'observacoes', 'status', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
