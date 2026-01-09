from django.contrib import admin
from .models import Cliente, UserProfile

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'telefone', 'cidade', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'cidade', 'data_criacao']
    search_fields = ['nome', 'cpf', 'email']
    readonly_fields = ['data_criacao']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'idade', 'telefone', 'data_criacao']
    list_filter = ['data_criacao']
    search_fields = ['user__username', 'user__email', 'telefone']
    readonly_fields = ['data_criacao', 'data_atualizacao']
