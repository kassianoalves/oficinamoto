from django.contrib import admin
from .models import Manutencao, Agendamento

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['moto', 'tipo_servico', 'data_manutencao', 'custo', 'concluida']
    list_filter = ['tipo_servico', 'concluida', 'data_manutencao']
    search_fields = ['moto__placa', 'moto__cliente__nome']

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['moto', 'tipo_servico', 'data_agendada', 'status']
    list_filter = ['status', 'tipo_servico', 'data_agendada']
    search_fields = ['moto__placa', 'moto__cliente__nome']
