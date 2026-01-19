from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade, Peca, ItemAgendamento, FotoPeca, ItemCarrinho
from .serializers import (
    ManutencaoSerializer, AgendamentoSerializer, LembreteSerializer, 
    PontosFidelidadeSerializer, PecaSerializer, ItemAgendamentoSerializer,
    AgendamentoComItensSerializer, FotoPecaSerializer, ItemCarrinhoSerializer,
    CarrinhoResumoSerializer
)
from clientes.group_permissions import HasGroupPermission, IsAdminGroup
from django.db.models import Sum, F
from django.db import transaction

class PecaViewSet(viewsets.ModelViewSet):
    """Gerenciamento de inventário de peças"""
    queryset = Peca.objects.prefetch_related('fotos').all()
    serializer_class = PecaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasGroupPermission]
    
    def get_queryset(self):
        queryset = Peca.objects.prefetch_related('fotos')
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        ativa = self.request.query_params.get('ativa')
        if ativa:
            queryset = queryset.filter(ativa=ativa.lower() == 'true')
        return queryset.order_by('categoria', 'nome')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def adicionar_foto(self, request, pk=None):
        """Adiciona uma foto à peça (máximo 2 fotos)"""
        peca = self.get_object()
        
        # Verificar limite de fotos
        fotos_count = FotoPeca.objects.filter(peca=peca).count()
        if fotos_count >= 2:
            return Response(
                {'error': 'Máximo de 2 fotos por peça'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if 'imagem' not in request.FILES:
            return Response(
                {'error': 'Nenhuma imagem foi enviada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            foto = FotoPeca.objects.create(
                peca=peca,
                imagem=request.FILES['imagem']
            )
            serializer = FotoPecaSerializer(foto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remover_foto(self, request, pk=None):
        """Remove uma foto da peça"""
        try:
            foto_id = request.query_params.get('foto_id')
            if not foto_id:
                return Response(
                    {'error': 'foto_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            foto = FotoPeca.objects.get(id=foto_id, peca_id=pk)
            foto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FotoPeca.DoesNotExist:
            return Response(
                {'error': 'Foto não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

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


class CarrinhoViewSet(viewsets.ModelViewSet):
    """Gerenciamento do carrinho de compras"""
    serializer_class = ItemCarrinhoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permite acesso anônimo

    def get_queryset(self):
        """Retorna itens do carrinho do usuário logado ou sessão anônima"""
        if self.request.user.is_authenticated:
            return ItemCarrinho.objects.filter(usuario=self.request.user).select_related('peca').prefetch_related('peca__fotos')
        else:
            # Para usuários anônimos, usa session
            session_key = self.request.session.session_key
            if not session_key:
                return ItemCarrinho.objects.none()
            return ItemCarrinho.objects.filter(sessao_id=session_key).select_related('peca').prefetch_related('peca__fotos')

    @action(detail=False, methods=['get'])
    def resumo(self, request):
        """Retorna resumo do carrinho com total"""
        itens = self.get_queryset()
        total_preco = sum(item.subtotal for item in itens)
        total_itens = sum(item.quantidade for item in itens)
        
        serializer = CarrinhoResumoSerializer({
            'itens': itens,
            'total_itens': total_itens,
            'total_preco': total_preco
        })
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def adicionar(self, request):
        """Adiciona ou atualiza item no carrinho (com logs de depuração)"""
        import logging
        logger = logging.getLogger('django')
        peca_id = request.data.get('peca_id')
        quantidade = int(request.data.get('quantidade', 1))

        logger.info(f"[CARRINHO] Requisição adicionar: user={request.user}, peca_id={peca_id}, quantidade={quantidade}")

        if not peca_id:
            logger.warning('[CARRINHO] Falha: peca_id não informado')
            return Response({'error': 'peca_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            peca = Peca.objects.get(id=peca_id, ativa=True)
        except Peca.DoesNotExist:
            logger.warning(f'[CARRINHO] Peça não encontrada: id={peca_id}')
            return Response({'error': 'Peça não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Validar estoque
        if quantidade > peca.quantidade:
            logger.warning(f'[CARRINHO] Estoque insuficiente: solicitado={quantidade}, disponivel={peca.quantidade}')
            return Response(
                {'error': f'Estoque insuficiente. Disponível: {peca.quantidade}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar ou criar item no carrinho
        if request.user.is_authenticated:
            logger.info(f'[CARRINHO] Usuário autenticado: {request.user}')
            item, created = ItemCarrinho.objects.get_or_create(
                usuario=request.user,
                peca=peca,
                defaults={'quantidade': quantidade, 'preco_unitario': peca.preco_unitario}
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            logger.info(f'[CARRINHO] Sessão anônima: {session_key}')
            item, created = ItemCarrinho.objects.get_or_create(
                sessao_id=session_key,
                peca=peca,
                defaults={'quantidade': quantidade, 'preco_unitario': peca.preco_unitario}
            )

        if not created:
            # Se já existe, atualiza quantidade
            nova_quantidade = item.quantidade + quantidade
            if nova_quantidade > peca.quantidade:
                logger.warning(f'[CARRINHO] Atualização excede estoque: nova_quantidade={nova_quantidade}, disponivel={peca.quantidade}')
                return Response(
                    {'error': f'Estoque insuficiente. Disponível: {peca.quantidade}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.quantidade = nova_quantidade
            item.save()
            logger.info(f'[CARRINHO] Quantidade atualizada: item_id={item.id}, nova_quantidade={item.quantidade}')
        else:
            logger.info(f'[CARRINHO] Novo item criado: item_id={item.id}, quantidade={item.quantidade}')

        serializer = ItemCarrinhoSerializer(item, context={'request': request})
        logger.info(f'[CARRINHO] Resposta para frontend: {serializer.data}')
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def atualizar_quantidade(self, request, pk=None):
        """Atualiza quantidade de um item"""
        item = self.get_object()
        quantidade = int(request.data.get('quantidade', 1))

        if quantidade <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if quantidade > item.peca.quantidade:
            return Response(
                {'error': f'Estoque insuficiente. Disponível: {item.peca.quantidade}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantidade = quantidade
        item.save()

        serializer = ItemCarrinhoSerializer(item, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def migrar_carrinho(self, request):
        """Migra carrinho do localStorage/sessão para o usuário logado"""
        if not request.user.is_authenticated:
            return Response({'error': 'Usuário não autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

        itens_localstorage = request.data.get('itens', [])
        
        with transaction.atomic():
            for item_data in itens_localstorage:
                peca_id = item_data.get('peca_id')
                quantidade = item_data.get('quantidade', 1)

                try:
                    peca = Peca.objects.get(id=peca_id, ativa=True)
                    
                    # Validar estoque
                    if quantidade > peca.quantidade:
                        continue  # Pula itens sem estoque

                    # Buscar ou criar item no carrinho do usuário
                    item, created = ItemCarrinho.objects.get_or_create(
                        usuario=request.user,
                        peca=peca,
                        defaults={'quantidade': quantidade, 'preco_unitario': peca.preco_unitario}
                    )

                    if not created:
                        # Se já existe, soma as quantidades
                        nova_quantidade = item.quantidade + quantidade
                        if nova_quantidade <= peca.quantidade:
                            item.quantidade = nova_quantidade
                            item.save()

                except Peca.DoesNotExist:
                    continue  # Pula peças que não existem mais

        # Retorna o carrinho atualizado
        return self.resumo(request)

    @action(detail=False, methods=['post'])
    def validar_estoque(self, request):
        """Valida se todos os itens do carrinho têm estoque disponível"""
        itens = self.get_queryset()
        erros = []

        for item in itens:
            if item.quantidade > item.peca.quantidade:
                erros.append({
                    'item_id': item.id,
                    'peca': item.peca.nome,
                    'solicitado': item.quantidade,
                    'disponivel': item.peca.quantidade
                })

        if erros:
            return Response(
                {'valid': False, 'erros': erros},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'valid': True, 'message': 'Todos os itens estão disponíveis'})

    @action(detail=False, methods=['delete'])
    def limpar(self, request):
        """Remove todos os itens do carrinho"""
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

