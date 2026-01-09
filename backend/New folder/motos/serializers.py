from rest_framework import serializers
from .models import Moto, Peca

class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = ['id', 'cliente', 'marca', 'modelo', 'ano', 'cor', 'placa', 'numero_serie', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = ['id', 'marca_moto', 'modelo_moto', 'ano_moto', 'nome_peca', 'descricao', 'codigo_original']
        read_only_fields = ['id']
