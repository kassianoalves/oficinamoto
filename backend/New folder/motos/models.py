from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
import re
from datetime import datetime

def validate_placa(value):
    """Valida formato de placa brasileira (ABC-1234 ou ABC1D23)"""
    placa = value.upper().replace('-', '').replace(' ', '')
    # Formato antigo: ABC1234
    # Formato Mercosul: ABC1D23
    if not re.match(r'^[A-Z]{3}\d{1}[A-Z0-9]{1}\d{2}$', placa):
        raise ValidationError('Placa inválida. Use formato ABC-1234 ou ABC1D23')
    return value

def validate_ano_moto(value):
    """Valida ano da moto"""
    ano_atual = datetime.now().year
    if value < 1900 or value > ano_atual + 1:
        raise ValidationError(f'Ano deve estar entre 1900 e {ano_atual + 1}')
    return value

class Moto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='motos')
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField(validators=[validate_ano_moto])
    cor = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True, validators=[validate_placa])
    numero_serie = models.CharField(max_length=50, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'

    def clean(self):
        # Normalizar placa
        if self.placa:
            self.placa = self.placa.upper().replace(' ', '')

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
