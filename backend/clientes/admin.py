from django.contrib import admin
from .models import Cliente, UserProfile, Plan, Subscription, Fornecedor, ProdutoLoja
from .site_models import SiteSettings

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


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_clientes', 'max_motos', 'max_agendamentos']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'price')
        }),
        ('Limites', {
            'fields': ('max_clientes', 'max_motos', 'max_agendamentos')
        }),
        ('Recursos Básicos', {
            'fields': ('has_app_mobile', 'has_whatsapp', 'has_lembretes')
        }),
        ('Recursos Avançados (PRO)', {
            'fields': ('has_fornecedores', 'has_chat_suporte', 'has_backup_nuvem', 
                      'has_ia_diagnostico', 'has_plano_fidelidade', 'has_agendamentos_prioritarios')
        }),
        ('Recursos Enterprise', {
            'fields': ('has_loja',)
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'data_inicio', 'data_renovacao']
    list_filter = ['status', 'plan', 'data_inicio']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['data_inicio']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especialidade', 'cidade', 'telefone', 'data_criacao']
    list_filter = ['especialidade', 'cidade', 'data_criacao']
    search_fields = ['nome', 'email', 'telefone', 'cnpj']
    readonly_fields = ['data_criacao']


@admin.register(ProdutoLoja)
class ProdutoLojaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'user', 'preco', 'estoque', 'categoria', 'ativo', 'data_criacao']
    list_filter = ['categoria', 'ativo', 'data_criacao']
    search_fields = ['nome', 'sku', 'user__username']
    readonly_fields = ['data_criacao']
    list_editable = ['estoque', 'ativo']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'logo', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Permitir apenas 1 instância (singleton)
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar a configuração
        return False
