from rest_framework import serializers
from .models import Cliente, ProdutoLoja, ManualsBase
from motos.models import Moto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'email', 'telefone', 'endereco', 'cidade', 'ativo', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']


class ProdutoLojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoLoja
        fields = ['id', 'user', 'nome', 'descricao', 'preco', 'estoque', 'imagem', 'categoria', 'sku', 'ativo', 'data_criacao']
        read_only_fields = ['id', 'user', 'data_criacao']

    def create(self, validated_data):
        """Define automaticamente o user como o usuário logado"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ManualsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualsBase
        fields = ['id', 'marca', 'modelo', 'ano', 'tipo_reparo', 'descricao', 'arquivo_pdf', 'url_externo', 'dificuldade', 'tempo_estimado', 'ferramentas_necessarias', 'ativo']
        read_only_fields = ['id']
