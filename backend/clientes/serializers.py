
from rest_framework import serializers
from .models import Cliente, ProdutoLoja, Fornecedor
from motos.models import Moto

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = [
            'id', 'user', 'nome', 'email', 'telefone', 'cnpj', 'endereco',
            'cep', 'bairro', 'estado', 'cidade', 'especialidade',
            'representante_nome', 'representante_telefone', 'data_criacao'
        ]
        read_only_fields = ['id', 'user', 'data_criacao']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

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
