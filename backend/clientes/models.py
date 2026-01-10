from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import re

# Import SiteSettings
from .site_models import SiteSettings

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
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_thumb = models.ImageField(upload_to='avatars/thumbs/', blank=True, null=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Redimensionar avatar para 256x256 (quadrado) se existir
        if self.avatar:
            try:
                img = Image.open(self.avatar)
                # Preferir salvar em WEBP para reduzir tamanho (fallback para JPEG)
                save_format = 'WEBP'
                # Converter para RGB se necessário
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                # Crop central para quadrado
                width, height = img.size
                min_side = min(width, height)
                left = (width - min_side) // 2
                top = (height - min_side) // 2
                right = left + min_side
                bottom = top + min_side
                img = img.crop((left, top, right, bottom))
                # Redimensionar para 256x256
                img = img.resize((256, 256), Image.LANCZOS)
                # Salvar em memória e substituir arquivo
                buffer = BytesIO()
                try:
                    img.save(buffer, format=save_format, quality=85)
                    ext_main = 'webp'
                except Exception:
                    # Fallback
                    img.save(buffer, format='JPEG', quality=85)
                    ext_main = 'jpg'
                buffer.seek(0)
                # Manter mesmo nome de arquivo
                file_name = self.avatar.name.split('/')[-1]
                base, _ext = file_name.rsplit('.', 1) if '.' in file_name else (file_name, 'jpg')
                new_name = f"{base}.{ext_main}"
                self.avatar.save(new_name, ContentFile(buffer.read()), save=False)
                # Gerar thumbnail 64x64
                thumb = img.copy().resize((64, 64), Image.LANCZOS)
                tbuffer = BytesIO()
                try:
                    thumb.save(tbuffer, format=save_format, quality=85)
                    ext_thumb = 'webp'
                except Exception:
                    thumb.save(tbuffer, format='JPEG', quality=85)
                    ext_thumb = 'jpg'
                tbuffer.seek(0)
                thumb_name = f"{base}_thumb.{ext_thumb}"
                self.avatar_thumb.save(thumb_name, ContentFile(tbuffer.read()), save=False)
                super().save(update_fields=['avatar', 'avatar_thumb'])
            except Exception:
                # Em caso de problema no processamento da imagem, mantém original
                pass


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal unificado para criar e atualizar perfil do usuário.
    
    - Se criado: cria UserProfile e Subscription gratuita
    - Se atualizado: garante que profile existe e está salvo
    """
    if created:
        # Criar perfil do usuário
        UserProfile.objects.get_or_create(user=instance)
        
        # Criar subscrição gratuita para novos usuários
        free_plan = Plan.objects.filter(name='free').first()
        if free_plan:
            Subscription.objects.get_or_create(
                user=instance,
                defaults={
                    'plan': free_plan,
                    'status': 'ativa'
                }
            )
    else:
        # Garantir que profile existe para usuários existentes
        if not hasattr(instance, 'profile'):
            UserProfile.objects.get_or_create(user=instance)


class Plan(models.Model):
    """Planos de assinatura (Gratuito, PRO e Enterprise)"""
    PLAN_CHOICES = [
        ('free', 'Gratuito'),
        ('pro', 'PRO'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Limites de recursos por plano
    max_clientes = models.IntegerField(default=100, help_text='Número máximo de clientes')
    max_motos = models.IntegerField(default=100, help_text='Número máximo de motos')
    max_agendamentos = models.IntegerField(default=100, help_text='Número máximo de agendamentos')
    
    # Funcionalidades do plano
    has_app_mobile = models.BooleanField(default=False, help_text='Acesso via aplicativo móvel')
    has_whatsapp = models.BooleanField(default=False, help_text='Integração com WhatsApp')
    has_lembretes = models.BooleanField(default=False, help_text='Sistema de lembretes automáticos')
    has_fornecedores = models.BooleanField(default=False, help_text='Gerenciamento de fornecedores')
    has_chat_suporte = models.BooleanField(default=False, help_text='Chat de suporte prioritário')
    has_backup_nuvem = models.BooleanField(default=False, help_text='Backup automático na nuvem')
    has_ia_diagnostico = models.BooleanField(default=False, help_text='IA para diagnóstico de problemas')
    has_plano_fidelidade = models.BooleanField(default=False, help_text='Sistema de fidelidade de clientes')
    has_agendamentos_prioritarios = models.BooleanField(default=False, help_text='Agendamentos com prioridade')
    has_loja = models.BooleanField(default=False, help_text='Loja para vender produtos')
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.get_name_display()} - R$ {self.price}"


class Subscription(models.Model):
    """Assinatura do usuário"""
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('inativa', 'Inativa'),
        ('cancelada', 'Cancelada'),
        ('pendente', 'Pendente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_renovacao = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = 'Assinaturas'
    
    def is_active(self):
        return self.status == 'ativa' and (not self.data_renovacao or self.data_renovacao > timezone.now())
    
    def renew(self, days=30):
        from datetime import timedelta
        self.data_renovacao = timezone.now() + timedelta(days=days)
        self.status = 'ativa'
        self.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class Fornecedor(models.Model):
    """Fornecedores/Parceiros da oficina"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fornecedores')
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=18, blank=True)
    endereco = models.TextField()
    cidade = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Fornecedor'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


class ProdutoLoja(models.Model):
    """Produtos na loja do usuário (Enterprise)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos_loja')
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.CharField(max_length=100)  # óleo, pneu, peça, etc
    sku = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Loja'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"