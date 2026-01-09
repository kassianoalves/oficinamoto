import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Pegar o token do usuário funcionario
try:
    user = User.objects.get(username='funcionario')
    token, created = Token.objects.get_or_create(user=user)
    
    print(f"✅ Token do usuário 'funcionario':")
    print(f"   {token.key}\n")
    print(f"🔗 Teste manual no navegador ou Postman:")
    print(f"   URL: http://127.0.0.1:8000/api/subscription/subscription/")
    print(f"   Header: Authorization: Token {token.key}\n")
    
    # Verificar subscrição
    subscription = user.subscription
    print(f"📋 Dados da subscrição:")
    print(f"   Plano: {subscription.plan.name}")
    print(f"   Status: {subscription.status}")
    print(f"   Ativo: {subscription.is_active()}")
    print(f"   Data renovação: {subscription.data_renovacao}")
    
except User.DoesNotExist:
    print("❌ Usuário não encontrado")
