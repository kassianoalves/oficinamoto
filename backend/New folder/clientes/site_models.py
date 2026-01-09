from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


class SiteSettings(models.Model):
    """Configurações globais do site (singleton)"""
    site_name = models.CharField(max_length=100, default='Moto Express')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'

    def save(self, *args, **kwargs):
        # Garantir que só existe uma instância (singleton)
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Já existe uma configuração de site. Edite a existente.')
        
        # Redimensionar logo se necessário
        if self.logo:
            self._resize_logo()
        
        super().save(*args, **kwargs)

    def _resize_logo(self):
        """Redimensiona logo para dimensões otimizadas preservando transparência"""
        if not self.logo:
            return
        
        img = Image.open(self.logo)
        original_mode = img.mode
        
        # Preservar transparência para RGBA e LA
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # Redimensionar mantendo aspect ratio (altura máx 90px)
        max_height = 90
        if img.height > max_height:
            ratio = max_height / img.height
            new_width = int(img.width * ratio)
            img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)
        
        # Salvar otimizado preservando transparência
        output = BytesIO()
        
        # Usar PNG para preservar transparência
        if img.mode in ('RGBA', 'LA'):
            img.save(output, format='PNG', optimize=True)
        else:
            img.save(output, format='PNG', optimize=True)
        
        output.seek(0)
        
        # Atualizar field com imagem otimizada
        self.logo.save(
            self.logo.name,
            ContentFile(output.read()),
            save=False
        )

    @classmethod
    def get_settings(cls):
        """Retorna a instância única de configurações"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings

    def __str__(self):
        return f'Configurações: {self.site_name}'
