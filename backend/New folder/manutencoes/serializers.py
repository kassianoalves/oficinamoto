from rest_framework import serializers
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade

class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = ['id', 'moto', 'tipo_servico', 'descricao', 'data_manutencao', 'data_proxima', 'custo', 'concluida', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'moto', 'tipo_servico', 'data_agendada', 'observacoes', 'prioritario', 'status', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class LembreteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lembrete
        fields = ['id', 'agendamento', 'tipo', 'destinatario', 'mensagem', 'data_envio_programada', 'enviado', 'data_envio_real', 'erro']
        read_only_fields = ['id', 'enviado', 'data_envio_real']

class PontosFidelidadeSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = PontosFidelidade
        fields = ['id', 'cliente', 'cliente_nome', 'pontos', 'total_gasto', 'data_atualizacao']
        read_only_fields = ['id', 'data_atualizacao']
