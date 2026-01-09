import requests

# Tokens de teste
admin_token = '3daa247348f6fa062933fecae87308f66cd76302'
func_token = '190b662aa8b52dfa9caad804f3f9f2b95c493782'

print("=== TESTANDO ENDPOINTS DE MANUTENÇÃO ===\n")

# Teste 1: GET agendamentos com admin
print("1. GET /api/agendamentos/ (admin)")
r = requests.get('http://127.0.0.1:8000/api/agendamentos/', 
                 headers={'Authorization': f'Token {admin_token}'})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'   Agendamentos: {data.get("count", len(data))}')
else:
    print(f'   Erro: {r.text[:200]}')

# Teste 2: GET agendamentos com funcionário
print("\n2. GET /api/agendamentos/ (funcionário)")
r = requests.get('http://127.0.0.1:8000/api/agendamentos/', 
                 headers={'Authorization': f'Token {func_token}'})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'   Agendamentos: {data.get("count", len(data))}')
else:
    print(f'   Erro: {r.text[:200]}')

# Teste 3: GET motos (para verificar se há motos para fazer agendamento)
print("\n3. GET /api/motos/ (admin)")
r = requests.get('http://127.0.0.1:8000/api/motos/', 
                 headers={'Authorization': f'Token {admin_token}'})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    motos = data.get('results', data) if isinstance(data, dict) else data
    print(f'   Motos disponíveis: {len(motos)}')
    if motos:
        print(f'   Primeira moto: ID={motos[0].get("id")}, {motos[0].get("marca")} {motos[0].get("modelo")}')
else:
    print(f'   Erro: {r.text[:200]}')

# Teste 4: POST agendamento com funcionário (deve funcionar - funcionário pode criar agendamentos)
print("\n4. POST /api/agendamentos/ (funcionário - deve funcionar)")
r = requests.post('http://127.0.0.1:8000/api/agendamentos/',
                  json={
                      'moto': 1,  # ID da primeira moto
                      'tipo_servico': 'manutencao',
                      'data_agendada': '2026-01-15T10:00:00',
                      'observacoes': 'Teste de agendamento',
                      'status': 'pendente'
                  },
                  headers={'Authorization': f'Token {func_token}'})
print(f'   Status: {r.status_code}')
print(f'   Response: {r.text[:300]}')

# Teste 5: GET manutencoes
print("\n5. GET /api/manutencoes/ (admin)")
r = requests.get('http://127.0.0.1:8000/api/manutencoes/', 
                 headers={'Authorization': f'Token {admin_token}'})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'   Manutenções: {data.get("count", len(data))}')
else:
    print(f'   Erro: {r.text[:200]}')
