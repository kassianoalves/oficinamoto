from django.db import models
from motos.models import Moto

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
        choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')],
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
        ordering = ['data_envio_programada']
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
        verbose_name = 'Pontos de Fidelidade'
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
