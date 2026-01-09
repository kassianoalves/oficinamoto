import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Subscription

# Tornar funcionario PRO ativo
try:
    user = User.objects.get(username='funcionario')
    subscription = user.subscription
    
    # Renovar por 365 dias (1 ano)
    subscription.renew(days=365)
    
    print(f"✅ Usuário '{user.username}' agora é PRO ATIVO!")
    print(f"📋 Plano: {subscription.plan.name}")
    print(f"✅ Status: {subscription.status}")
    print(f"📅 Renovação: {subscription.data_renovacao}")
    print(f"🔥 is_active(): {subscription.is_active()}")
except User.DoesNotExist:
    print("❌ Usuário 'funcionario' não encontrado")
