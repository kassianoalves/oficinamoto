from django.contrib import admin
from .models import Manutencao, Agendamento, Lembrete, PontosFidelidade

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
    readonly_fields = ['data_atualizacao']
