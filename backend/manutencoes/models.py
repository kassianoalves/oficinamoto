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
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')],
        default='pendente'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_agendada']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'{self.moto} - {self.data_agendada.strftime("%d/%m/%Y %H:%M")}'
