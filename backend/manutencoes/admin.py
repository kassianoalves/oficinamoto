from django.contrib import admin
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade, Peca, FotoPeca, ItemCarrinho

class FotoPecaInline(admin.TabularInline):
    model = FotoPeca
    extra = 1
    fields = ['imagem']

@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'quantidade', 'preco_unitario', 'categoria', 'ativa']
    list_filter = ['categoria', 'ativa', 'data_criacao']
    search_fields = ['nome', 'codigo', 'sku']
    inlines = [FotoPecaInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo', 'sku', 'descricao')
        }),
        ('Preço e Estoque', {
            'fields': ('preco_unitario', 'quantidade')
        }),
        ('Categorização', {
            'fields': ('categoria', 'fornecedor')
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
    )

@admin.register(FotoPeca)
class FotoPecaAdmin(admin.ModelAdmin):
    list_display = ['peca', 'imagem', 'data_criacao']
    list_filter = ['data_criacao']
    search_fields = ['peca__nome']
    readonly_fields = ['data_criacao']

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['moto', 'tipo_servico', 'data_manutencao', 'custo', 'concluida']
    list_filter = ['tipo_servico', 'concluida', 'data_manutencao']
    search_fields = ['moto__placa', 'moto__cliente__nome']

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['moto', 'tipo_servico', 'data_agendada', 'prioritario', 'status']
    list_filter = ['status', 'prioritario', 'tipo_servico', 'data_agendada']
    search_fields = ['moto__placa', 'moto__cliente__nome']
    list_editable = ['prioritario']

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ['agendamento', 'tipo', 'destinatario', 'data_envio_programada', 'enviado']
    list_filter = ['tipo', 'enviado', 'data_envio_programada']
    search_fields = ['destinatario', 'agendamento__moto__cliente__nome']
    readonly_fields = ['data_envio_real']

@admin.register(PontosFidelidade)
class PontosFidelidadeAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'pontos', 'total_gasto', 'data_atualizacao']
    search_fields = ['cliente__nome']


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['get_usuario_display', 'peca', 'quantidade', 'preco_unitario', 'subtotal', 'data_adicao']
    list_filter = ['data_adicao', 'data_atualizacao']
    search_fields = ['usuario__username', 'peca__nome', 'sessao_id']
    readonly_fields = ['data_adicao', 'data_atualizacao', 'preco_unitario', 'subtotal']

    def get_usuario_display(self, obj):
        if obj.usuario:
            return obj.usuario.username
        return f'Anônimo ({obj.sessao_id[:8]}...)'
    get_usuario_display.short_description = 'Usuário'

    readonly_fields = ['data_atualizacao']
