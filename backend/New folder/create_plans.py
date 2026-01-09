import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from clientes.models import Plan

# Criar plano gratuito
free_plan, created = Plan.objects.get_or_create(
    name='free',
    defaults={
        'price': 0.00,
        'max_clientes': 100,
        'max_motos': 100,
        'max_agendamentos': 100,
        'has_app_mobile': False,
        'has_whatsapp': False,
        'has_lembretes': False,
        'has_fornecedores': False,
        'has_chat_suporte': False,
        'has_backup_nuvem': False,
        'has_ia_diagnostico': False,
        'has_plano_fidelidade': False,
        'has_agendamentos_prioritarios': False,
    }
)

if created:
    print("✓ Plano Gratuito criado com sucesso!")
else:
    print("✓ Plano Gratuito já existe")

# Criar plano PRO
pro_plan, created = Plan.objects.get_or_create(
    name='pro',
    defaults={
        'price': 99.90,
        'max_clientes': 999999,  # Ilimitado
        'max_motos': 999999,
        'max_agendamentos': 999999,
        'has_app_mobile': True,
        'has_whatsapp': True,
        'has_lembretes': True,
        'has_fornecedores': True,
        'has_chat_suporte': True,
        'has_backup_nuvem': True,
        'has_ia_diagnostico': True,
        'has_plano_fidelidade': True,
        'has_agendamentos_prioritarios': True,
    }
)

if created:
    print("✓ Plano PRO criado com sucesso!")
else:
    print("✓ Plano PRO já existe")

print("\n=== Planos Cadastrados ===")
for plan in Plan.objects.all():
    print(f"{plan.name}: R$ {plan.price} - Limites: {plan.max_clientes} clientes")
