import os

# Adicionar ViewSets ao views.py
views_file = r'p:\Python\oficinamoto\oficinamoto\backend\manutencoes\views.py'

addon_code = '''

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
'''

with open(views_file, 'a', encoding='utf-8') as f:
    f.write(addon_code)

print("✅ ViewSets adicionados ao views.py")
