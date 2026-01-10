from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade, Peca, ItemAgendamento
from .serializers import (
    ManutencaoSerializer, AgendamentoSerializer, LembreteSerializer, 
    PontosFidelidadeSerializer, PecaSerializer, ItemAgendamentoSerializer,
    AgendamentoComItensSerializer
)
from clientes.group_permissions import HasGroupPermission, IsAdminGroup

class PecaViewSet(viewsets.ModelViewSet):
    """Gerenciamento de inventário de peças"""
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        queryset = Peca.objects.all()
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        ativa = self.request.query_params.get('ativa')
        if ativa:
            queryset = queryset.filter(ativa=ativa.lower() == 'true')
        return queryset.order_by('categoria', 'nome')

class ItemAgendamentoViewSet(viewsets.ModelViewSet):
    """Gerenciamento de itens (peças) por agendamento"""
    queryset = ItemAgendamento.objects.all()
    serializer_class = ItemAgendamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]

    def get_queryset(self):
        queryset = ItemAgendamento.objects.select_related('agendamento', 'peca')
        agendamento_id = self.request.query_params.get('agendamento_id')
        if agendamento_id:
            queryset = queryset.filter(agendamento_id=agendamento_id)
        return queryset

class ManutencaoViewSet(viewsets.ModelViewSet):
    """Gerenciamento de manutenções com consultas otimizadas."""
    serializer_class = ManutencaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        # select_related evita N+1 ao acessar moto e cliente da moto
        queryset = Manutencao.objects.select_related('moto__cliente')

        moto_id = self.request.query_params.get('moto_id')
        if moto_id:
            queryset = queryset.filter(moto_id=moto_id)
        return queryset

    def get_permissions(self):
        """Apenas admin pode deletar"""
        if self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()

class AgendamentoViewSet(viewsets.ModelViewSet):
    """Gerenciamento de agendamentos com consultas otimizadas."""
    serializer_class = AgendamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        # select_related evita N+1 ao acessar moto e cliente, prefetch para lembretes
        queryset = Agendamento.objects.select_related('moto__cliente').prefetch_related('lembretes')

        moto_id = self.request.query_params.get('moto_id')
        status = self.request.query_params.get('status')
        
        if moto_id:
            queryset = queryset.filter(moto_id=moto_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Verifica limites e permissão para agendamentos prioritários"""
        # Verificar se o usuário pode criar mais agendamentos
        user_subscription = getattr(request.user, 'subscription', None)
        if user_subscription and user_subscription.plan:
            total_agendamentos = Agendamento.objects.count()
            if total_agendamentos >= user_subscription.plan.max_agendamentos:
                return Response(
                    {
                        'error': f'Limite de {user_subscription.plan.max_agendamentos} agendamentos atingido!',
                        'detail': 'Faça upgrade para o plano PRO para ter agendamentos ilimitados.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Verificar se tentou marcar como prioritário sem ser PRO
            if request.data.get('prioritario') and not user_subscription.plan.has_agendamentos_prioritarios:
                return Response(
                    {
                        'error': 'Agendamentos prioritários disponíveis apenas no plano PRO!',
                        'detail': 'Faça upgrade para desbloquear este recurso.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """Apenas admin pode deletar"""
        if self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminGroup]
        else:
            self.permission_classes = [IsAuthenticated, HasGroupPermission]
        
        return super().get_permissions()


class LembreteViewSet(viewsets.ModelViewSet):
    serializer_class = LembreteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Lembrete.objects.all()


class PontosFidelidadeViewSet(viewsets.ModelViewSet):
    serializer_class = PontosFidelidadeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PontosFidelidade.objects.all()
    
    @action(detail=True, methods=['post'])
    def adicionar_pontos(self, request, pk=None):
        """Adiciona pontos baseado no valor gasto"""
        pontos_fidelidade = self.get_object()
        valor_gasto = request.data.get('valor_gasto', 0)
        
        try:
            valor_gasto = float(valor_gasto)
            novos_pontos = pontos_fidelidade.adicionar_pontos(valor_gasto)
            return Response({
                'message': f'{novos_pontos} pontos adicionados!',
                'total_pontos': pontos_fidelidade.pontos,
                'total_gasto': str(pontos_fidelidade.total_gasto)
            })
        except ValueError:
            return Response({'error': 'Valor inválido'}, status=status.HTTP_400_BAD_REQUEST)
