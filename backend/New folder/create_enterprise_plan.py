import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from clientes.models import Plan

# Verificar e atualizar plano PRO para incluir novos campos
pro_plan = Plan.objects.filter(name='pro').first()
if pro_plan:
    pro_plan.has_plano_fidelidade = True
    pro_plan.has_agendamentos_prioritarios = True
    pro_plan.save()
    print("✅ Plano PRO atualizado com novos campos!")

# Criar plano Enterprise
enterprise_plan, created = Plan.objects.get_or_create(
    name='enterprise',
    defaults={
        'price': 499.90,
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
        'has_loja': True,
        'has_imagem_3d': True,
        'has_manuais': True,
    }
)

if created:
    print("✅ Plano Enterprise criado com sucesso!")
else:
    print("✅ Plano Enterprise já existe")

print("\n=== Planos Cadastrados ===")
for plan in Plan.objects.all().order_by('price'):
    resources = []
    if plan.has_loja:
        resources.append("🛍️ Loja")
    if plan.has_imagem_3d:
        resources.append("🎨 3D")
    if plan.has_manuais:
        resources.append("📚 Manuais")
    
    resources_text = f" + {', '.join(resources)}" if resources else ""
    print(f"\n{plan.name.upper()}: R$ {plan.price}")
    print(f"  Limites: {plan.max_clientes} clientes{resources_text}")
