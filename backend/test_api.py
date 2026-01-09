import requests

token = '3daa247348f6fa062933fecae87308f66cd76302'
url = 'http://127.0.0.1:8000/api/clientes/'

print(f'Testing GET {url}')
print(f'Token: {token}')

r = requests.get(url, headers={'Authorization': f'Token {token}'})
print(f'Status: {r.status_code}')
print(f'Response: {r.text[:500]}')
