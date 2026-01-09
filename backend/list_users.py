import os
import django
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oficinamoto_api.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

print('=== USUÁRIOS ===')
for u in User.objects.all():
    groups = list(u.groups.values_list('name', flat=True))
    print(f'{u.username} (id={u.id}, admin={u.is_staff}, groups={groups})')

print('\n=== TOKENS ===')
for t in Token.objects.all():
    print(f'{t.user.username}: {t.key}')
