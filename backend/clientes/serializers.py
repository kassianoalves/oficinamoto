from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'email', 'telefone', 'endereco', 'cidade', 'ativo', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
