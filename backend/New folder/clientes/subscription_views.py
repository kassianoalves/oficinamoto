from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Plan, Subscription, Fornecedor
from .subscription_serializers import PlanSerializer, SubscriptionSerializer, FornecedorSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None  # Desabilitar paginação
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def get_object(self):
        return self.request.user.subscription


class FornecedorViewSet(viewsets.ModelViewSet):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        return Fornecedor.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upgrade_pro(request):
    """
    Inicia o processo de upgrade para PRO
    Integração com MercadoPago virá aqui
    """
    try:
        user = request.user
        pro_plan = Plan.objects.get(name='pro')
        
        # Aqui vai integração com MercadoPago/Stripe
        # Por enquanto, vamos simular
        
        return Response({
            'message': 'Redirecionando para pagamento',
            'plan': PlanSerializer(pro_plan).data,
            'payment_url': 'https://seu-gateway-pagamento.com/checkout'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """Cancelar subscrição"""
    try:
        subscription = request.user.subscription
        subscription.status = 'cancelada'
        subscription.save()
        return Response({'message': 'Subscrição cancelada'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
