from rest_framework import serializers
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade, Peca, ItemAgendamento, FotoPeca, ItemCarrinho

class FotoPecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoPeca
        fields = ['id', 'imagem', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class PecaSerializer(serializers.ModelSerializer):
    fotos = FotoPecaSerializer(many=True, read_only=True)
    estoque = serializers.IntegerField(source='quantidade', read_only=True)
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Peca
        fields = ['id', 'nome', 'descricao', 'codigo', 'quantidade', 'estoque', 'preco_unitario', 'preco', 'categoria', 'marca', 'fornecedor', 'sku', 'ativa', 'fotos', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

    def get_preco(self, obj):
        """Retorna preco_unitario como preco (compatibilidade com frontend)"""
        return float(obj.preco_unitario) if obj.preco_unitario else 0.0

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


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    peca_nome = serializers.CharField(source='peca.nome', read_only=True)
    peca_codigo = serializers.CharField(source='peca.codigo', read_only=True)
    peca_foto = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    estoque_disponivel = serializers.IntegerField(source='peca.quantidade', read_only=True)

    class Meta:
        model = ItemCarrinho
        fields = [
            'id', 'peca', 'peca_nome', 'peca_codigo', 'peca_foto',
            'quantidade', 'preco_unitario', 'subtotal', 'estoque_disponivel',
            'data_adicao', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_adicao', 'data_atualizacao', 'preco_unitario']

    def get_peca_foto(self, obj):
        """Retorna a primeira foto da peça se existir"""
        foto = obj.peca.fotos.first()
        if foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(foto.imagem.url)
            return foto.imagem.url
        return None

    def create(self, validated_data):
        # Define o preço unitário atual da peça
        peca = validated_data['peca']
        validated_data['preco_unitario'] = peca.preco_unitario
        
        # Define usuário ou sessão_id
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['usuario'] = request.user
        else:
            # Para usuários anônimos, usa session key
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            validated_data['sessao_id'] = session_key
        
        return super().create(validated_data)


class CarrinhoResumoSerializer(serializers.Serializer):
    """Serializer para resumo do carrinho"""
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total_itens = serializers.IntegerField()
    total_preco = serializers.DecimalField(max_digits=10, decimal_places=2)

