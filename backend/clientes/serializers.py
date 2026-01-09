from rest_framework import serializers
from .models import Cliente, ProdutoLoja, Imagem3D, ManualsBase
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


class Imagem3DSerializer(serializers.ModelSerializer):
    moto_nome = serializers.CharField(source='moto.modelo', read_only=True)
    
    class Meta:
        model = Imagem3D
        fields = ['id', 'moto', 'moto_nome', 'titulo', 'descricao', 'arquivo_3d', 'imagem_preview', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']


class ManualsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualsBase
        fields = ['id', 'marca', 'modelo', 'ano', 'tipo_reparo', 'descricao', 'arquivo_pdf', 'url_externo', 'dificuldade', 'tempo_estimado', 'ferramentas_necessarias', 'ativo']
        read_only_fields = ['id']
