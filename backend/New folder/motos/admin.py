from django.contrib import admin
from .models import Moto, Peca

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'ano', 'placa', 'cliente', 'data_criacao']
    list_filter = ['marca', 'ano', 'data_criacao']
    search_fields = ['placa', 'numero_serie', 'cliente__nome']

@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ['nome_peca', 'marca_moto', 'modelo_moto', 'ano_moto']
    list_filter = ['marca_moto', 'modelo_moto', 'ano_moto']
    search_fields = ['nome_peca', 'codigo_original']
