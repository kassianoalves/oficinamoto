from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'telefone', 'cidade', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'cidade', 'data_criacao']
    search_fields = ['nome', 'cpf', 'email']
    readonly_fields = ['data_criacao']
