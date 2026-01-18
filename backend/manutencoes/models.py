from django.db import models
from motos.models import Moto
from django.core.exceptions import ValidationError
from django.conf import settings

class Peca(models.Model):
    """Inventário de peças disponíveis"""
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    codigo = models.CharField(max_length=100, unique=True)
    quantidade = models.IntegerField(default=0)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True, help_text='Ex: Óleo, Filtro, Corrente, Freio')
    marca = models.CharField(max_length=255, blank=True, help_text='Marca do produto')
    fornecedor = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, unique=True, default='', blank=True)

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f'{self.nome} ({self.codigo}) - Qtd: {self.quantidade}'

    def clean(self):
        # Validar máximo de 2 fotos
        if self.pk:
            fotos_count = FotoPeca.objects.filter(peca=self).count()
            if fotos_count > 2:
                raise ValidationError('Máximo de 2 fotos por peça')


class FotoPeca(models.Model):
    """Fotos de peças para venda na loja"""
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='pecas/')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto de Peça'
        verbose_name_plural = 'Fotos de Peças'
        ordering = ['data_criacao']
        unique_together = ['peca', 'imagem']

    def clean(self):
        # Validar máximo de 2 fotos por peça
        if self.peca:
            fotos_count = FotoPeca.objects.filter(peca=self.peca).exclude(pk=self.pk).count()
            if fotos_count >= 2:
                raise ValidationError('Máximo de 2 fotos por peça')

    def __str__(self):
        return f'Foto - {self.peca.nome}'


class ItemAgendamento(models.Model):
    """Peças usadas em cada agendamento"""
    agendamento = models.ForeignKey('Agendamento', on_delete=models.CASCADE, related_name='itens_peca')
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade_usada = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Preço no momento do uso
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item de Agendamento'
        verbose_name_plural = 'Itens de Agendamento'

    def __str__(self):
        return f'{self.agendamento} - {self.peca.nome} x{self.quantidade_usada}'

    @property
    def subtotal(self):
        return self.quantidade_usada * self.preco_unitario


class Manutencao(models.Model):
    TIPO_SERVICO = [
        ('troca', 'Troca de Óleo'),
        ('reparo', 'Reparo'),
        ('assistencia', 'Assistência'),
        ('vistoria', 'Vistoria'),
        ('manutencao', 'Manutenção Periódica'),
    ]

    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='manutencoes')
    tipo_servico = models.CharField(max_length=20, choices=TIPO_SERVICO)
    descricao = models.TextField()
    data_manutencao = models.DateTimeField()
    data_proxima = models.DateTimeField(blank=True, null=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    concluida = models.BooleanField(default=True)

    class Meta:
        ordering = ['-data_manutencao']
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'

    def __str__(self):
        return f'{self.moto} - {self.tipo_servico} ({self.data_manutencao.strftime("%d/%m/%Y")})'


class Agendamento(models.Model):
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='agendamentos')
    tipo_servico = models.CharField(max_length=20, choices=Manutencao.TIPO_SERVICO)
    data_agendada = models.DateTimeField()
    observacoes = models.TextField(blank=True)
    prioritario = models.BooleanField(default=False, help_text='Agendamento prioritário (PRO)')
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')],
        default='pendente'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-prioritario', 'data_agendada']  # Prioritários primeiro
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        prioridade = '⚡ ' if self.prioritario else ''
        return f'{prioridade}{self.moto} - {self.data_agendada.strftime("%d/%m/%Y %H:%M")}'


class Lembrete(models.Model):
    """Lembretes automáticos para agendamentos (PRO)"""
    TIPO_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
    ]
    
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='lembretes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    destinatario = models.CharField(max_length=255)  # Telefone ou email
    mensagem = models.TextField()
    data_envio_programada = models.DateTimeField()
    enviado = models.BooleanField(default=False)
    data_envio_real = models.DateTimeField(null=True, blank=True)
    erro = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Lembrete'
        verbose_name_plural = 'Lembretes'
    
    def __str__(self):
        status = '✅' if self.enviado else '⏳'
        return f'{status} {self.tipo} - {self.agendamento}'


class PontosFidelidade(models.Model):
    """Sistema de pontos de fidelidade (PRO)"""
    cliente = models.OneToOneField('clientes.Cliente', on_delete=models.CASCADE, related_name='pontos_fidelidade')
    pontos = models.IntegerField(default=0)
    total_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Pontos de Fidelidade'
    
    def __str__(self):
        return f'{self.cliente.nome} - {self.pontos} pontos'
    
    def adicionar_pontos(self, valor_gasto):
        """Adiciona pontos baseado no valor gasto (1 ponto a cada R$ 10)"""
        novos_pontos = int(valor_gasto / 10)
        self.pontos += novos_pontos
        self.total_gasto += valor_gasto
        self.save()
        return novos_pontos


class ItemCarrinho(models.Model):
    """Itens do carrinho de compras"""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='itens_carrinho',
        null=True,
        blank=True,
        help_text='Null para carrinhos anônimos (localStorage)'
    )
    sessao_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='ID de sessão para usuários não logados'
    )
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Preço no momento da adição ao carrinho'
    )
    data_adicao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        ordering = ['-data_adicao']
        unique_together = [['usuario', 'peca'], ['sessao_id', 'peca']]

    def __str__(self):
        user_ref = self.usuario.username if self.usuario else f'Sessão: {self.sessao_id}'
        return f'{user_ref} - {self.peca.nome} x{self.quantidade}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def clean(self):
        # Validar que tem usuário OU sessão_id
        if not self.usuario and not self.sessao_id:
            raise ValidationError('Item deve ter usuário ou sessão_id')
        
        # Validar estoque disponível
        if self.quantidade > self.peca.quantidade:
            raise ValidationError(f'Estoque insuficiente. Disponível: {self.peca.quantidade}')

