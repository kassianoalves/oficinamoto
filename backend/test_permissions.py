import requests

print("=== TESTE 1: GET com admin (deve funcionar) ===")
r = requests.get('http://127.0.0.1:8000/api/clientes/', 
                 headers={'Authorization': 'Token 3daa247348f6fa062933fecae87308f66cd76302'})
print(f'GET clientes: {r.status_code} {r.json().get("count") or r.text[:100]}')

print("\n=== TESTE 2: GET com funcionário (deve funcionar - apenas leitura) ===")
r = requests.get('http://127.0.0.1:8000/api/clientes/', 
                 headers={'Authorization': 'Token 190b662aa8b52dfa9caad804f3f9f2b95c493782'})
print(f'GET clientes: {r.status_code} {r.json().get("count") or r.text[:100]}')

print("\n=== TESTE 3: POST com admin (deve funcionar) ===")
r = requests.post('http://127.0.0.1:8000/api/clientes/',
                  json={'nome': 'Teste', 'cpf': '12345678901', 'email': 'teste@test.com', 
                        'telefone': '1234567890', 'endereco': 'teste', 'cidade': 'teste'},
                  headers={'Authorization': 'Token 3daa247348f6fa062933fecae87308f66cd76302'})
print(f'POST clientes: {r.status_code} {r.text[:100]}')

print("\n=== TESTE 4: POST com funcionário (deve falhar - sem permissão) ===")
r = requests.post('http://127.0.0.1:8000/api/clientes/',
                  json={'nome': 'Teste', 'cpf': '12345678902', 'email': 'teste2@test.com', 
                        'telefone': '1234567890', 'endereco': 'teste', 'cidade': 'teste'},
                  headers={'Authorization': 'Token 190b662aa8b52dfa9caad804f3f9f2b95c493782'})
print(f'POST clientes: {r.status_code} {r.text[:100]}')
