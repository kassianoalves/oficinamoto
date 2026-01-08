from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nome} - {self.cpf}'
