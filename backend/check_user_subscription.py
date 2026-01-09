import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Subscription, Plan

print("\n=== VERIFICANDO SUBSCRIÇÕES ===\n")

for user in User.objects.all():
    try:
        subscription = user.subscription
        print(f"👤 Usuário: {user.username}")
        print(f"   📋 Plano: {subscription.plan.name}")
        print(f"   💰 Preço: R$ {subscription.plan.price}")
        print(f"   ✅ Status: {subscription.status}")
        print(f"   🔥 Ativo: {subscription.is_active()}")
        print()
    except Subscription.DoesNotExist:
        print(f"👤 Usuário: {user.username}")
        print(f"   ❌ SEM SUBSCRIÇÃO\n")

print("\n=== PLANOS DISPONÍVEIS ===\n")
for plan in Plan.objects.all():
    print(f"📦 {plan.name}: R$ {plan.price}")
    print(f"   Limites: {plan.max_clientes} clientes, {plan.max_motos} motos")
    print()
