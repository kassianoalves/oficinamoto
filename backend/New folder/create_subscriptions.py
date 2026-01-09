import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Plan, Subscription

# Obter o plano gratuito
free_plan = Plan.objects.get(name='free')

# Criar subscrições para usuários sem subscrição
users_without_subscription = User.objects.filter(subscription__isnull=True)

count = 0
for user in users_without_subscription:
    Subscription.objects.create(
        user=user,
        plan=free_plan,
        status='ativa'
    )
    count += 1
    print(f"✓ Subscrição criada para: {user.username}")

print(f"\n✓ Total de {count} subscrições criadas!")
print(f"✓ Total de usuários no sistema: {User.objects.count()}")
print(f"✓ Total de subscrições: {Subscription.objects.count()}")
