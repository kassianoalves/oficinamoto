from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

def validate_cpf(value):
    """Valida formato de CPF (000.000.000-00 ou 00000000000)"""
    cpf = re.sub(r'\D', '', value)
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    return value

def validate_telefone(value):
    """Valida formato de telefone brasileiro"""
    telefone = re.sub(r'\D', '', value)
    if len(telefone) < 10 or len(telefone) > 11:
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos')
    return value

class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, validators=[validate_telefone])
    endereco = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def clean(self):
        # Limpar CPF removendo pontos e traços
        if self.cpf:
            self.cpf = re.sub(r'\D', '', self.cpf)
        # Limpar telefone
        if self.telefone:
            self.telefone = re.sub(r'\D', '', self.telefone)

    def __str__(self):
        return f'{self.nome} - {self.cpf}'

class UserProfile(models.Model):
    """Perfil do usuário com informações adicionais"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    idade = models.IntegerField(null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria o perfil do usuário automaticamente"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil do usuário"""
    if hasattr(instance, 'profile'):
        instance.profile.save()