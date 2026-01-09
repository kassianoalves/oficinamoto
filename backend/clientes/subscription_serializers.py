from rest_framework import serializers
from .models import Plan, Subscription, Fornecedor


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_details = PlanSerializer(source='plan', read_only=True)
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_name', 'plan_details', 'status', 'data_inicio', 
                  'data_renovacao', 'is_active']
        read_only_fields = ['id', 'data_inicio', 'data_renovacao']
    
    def get_is_active(self, obj):
        return obj.is_active()


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'nome', 'email', 'telefone', 'cnpj', 'endereco', 'cidade', 
                  'especialidade', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
