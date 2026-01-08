from django.db import models
from clientes.models import Cliente

class Moto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='motos')
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    numero_serie = models.CharField(max_length=50, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.ano}) - {self.placa}'


class Peca(models.Model):
    marca_moto = models.CharField(max_length=100)
    modelo_moto = models.CharField(max_length=100)
    ano_moto = models.IntegerField()
    nome_peca = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    codigo_original = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['marca_moto', 'modelo_moto', 'ano_moto']
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'

    def __str__(self):
        return f'{self.nome_peca} - {self.marca_moto} {self.modelo_moto} {self.ano_moto}'
