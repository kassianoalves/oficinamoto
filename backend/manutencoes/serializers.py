from rest_framework import serializers
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade, Peca, ItemAgendamento

class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = ['id', 'nome', 'descricao', 'codigo', 'quantidade', 'preco_unitario', 'categoria', 'fornecedor', 'ativa', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class ItemAgendamentoSerializer(serializers.ModelSerializer):
    peca_nome = serializers.CharField(source='peca.nome', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ItemAgendamento
        fields = ['id', 'agendamento', 'peca', 'peca_nome', 'quantidade_usada', 'preco_unitario', 'subtotal', 'data_adicao']
        read_only_fields = ['id', 'data_adicao']

class AgendamentoComItensSerializer(serializers.ModelSerializer):
    itens_peca = ItemAgendamentoSerializer(many=True, read_only=True)
    custo_peca_total = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = ['id', 'moto', 'tipo_servico', 'data_agendada', 'observacoes', 'prioritario', 'status', 'data_criacao', 'itens_peca', 'custo_peca_total']
        read_only_fields = ['id', 'data_criacao']

    def get_custo_peca_total(self, obj):
        return sum(item.subtotal for item in obj.itens_peca.all())

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
