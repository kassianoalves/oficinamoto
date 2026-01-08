# VALIDAÇÃO & TESTES - ETAPA 1

## ✅ Checklist de Validação

### Backend Django

- [ ] Pasta `backend/venv` criada (após `python -m venv venv`)
- [ ] Arquivo `db.sqlite3` criado (após `python manage.py migrate`)
- [ ] `manage.py` executa: `python manage.py runserver`
- [ ] Admin acessível: http://127.0.0.1:8000/admin
- [ ] API endpoints retornam JSON: http://127.0.0.1:8000/api/clientes/

### Frontend Vue

- [ ] Pasta `frontend/node_modules` criada (após `npm install`)
- [ ] Servidor Vue inicia: `npm run dev`
- [ ] Interface acessível: http://127.0.0.1:5173
- [ ] Navbar visível com logo e navegação
- [ ] Dashboard mostra estatísticas (podem ser 0)

### Integração

- [ ] Frontend consegue se conectar ao Backend (sem CORS error)
- [ ] Página de Clientes carrega lista (mesmo que vazia)
- [ ] Formulário de Cliente consegue enviar POST
- [ ] Novo cliente apareça na lista

## 🧪 Testes Funcionais

### Teste 1: Criar Cliente

```
1. Ir em http://127.0.0.1:5173
2. Clicar em "Novo Cliente"
3. Preencher:
   - Nome: João Silva
   - CPF: 12345678900
   - Email: joao@email.com
   - Telefone: (11) 98765-4321
   - Endereço: Rua A, 123
   - Cidade: São Paulo
4. Clicar em "Salvar"
5. ✓ Cliente aparece na lista
```

### Teste 2: Criar Moto

```
1. Clicar em "Motos" (navbar)
2. Clicar em "Registrar Moto"
3. Selecionar cliente (João Silva)
4. Preencher:
   - Marca: Honda
   - Modelo: CB 500
   - Ano: 2020
   - Cor: Vermelha
   - Placa: ABC1234
   - Série: XYZ123456789
5. Clicar em "Salvar"
6. ✓ Moto aparece na lista com cliente correto
```

### Teste 3: Agendar Manutenção

```
1. Clicar em "Manutenções" (navbar)
2. Clicar em "Novo Agendamento"
3. Selecionar moto (Honda CB 500)
4. Escolher tipo: Troca de Óleo
5. Data: amanhã às 14:00
6. Status: Pendente
7. Observações: Trocar óleo 10W40
8. Clicar em "Salvar"
9. ✓ Agendamento aparece com status "pendente"
```

### Teste 4: Editar Cliente

```
1. Na página de Clientes
2. Clicar em "Editar" em um cliente
3. Mudar nome para "João da Silva"
4. Clicar em "Atualizar"
5. ✓ Nome atualizado na lista
```

### Teste 5: Deletar Cliente

```
1. Na página de Clientes
2. Clicar em "Deletar" em um cliente
3. Confirmar exclusão
4. ✓ Cliente desaparece da lista
5. NOTA: Se tem motos vinculadas, o backend pode impedir
```

### Teste 6: Dashboard

```
1. Ir em Home (logo ou /home)
2. Verificar se mostra:
   - Total de clientes
   - Total de motos
   - Agendamentos próximos
3. ✓ Números aumentam conforme você adiciona dados
```

## 🔍 Verificação de Dados

### Backend - Admin Django

```
1. Ir em http://127.0.0.1:8000/admin
2. Fazer login com credenciais do superusuário
3. Verificar tabelas:
   - Clientes → deve listar tudo que criou
   - Motos → deve vincular com cliente
   - Agendamentos → deve vincular com moto
4. Criar/editar/deletar diretamente no admin
5. ✓ Dados aparecem no frontend
```

### Frontend - Rede (DevTools)

```
1. Abrir http://127.0.0.1:5173
2. F12 → Abrir DevTools
3. Ir em "Network"
4. Fazer ação (criar cliente, etc)
5. Verificar requisição:
   - POST /api/clientes/ → Status 201 (criado)
   - Response em JSON
6. ✓ Sem erros CORS ou 500
```

### Frontend - Console (DevTools)

```
1. F12 → Aba "Console"
2. Fazer ação
3. Não deve haver erros vermelhos
4. Apenas warnings normais do Vite
```

## 📊 Teste de Performance

- [ ] Página carrega em < 2s
- [ ] Botões respondem imediatamente
- [ ] Formulário valida em tempo real
- [ ] Nenhum delay noticível

## 📱 Teste em Tablet

- [ ] Interface responsiva em 768px (tablet)
- [ ] Botões com tamanho adequado (> 44px)
- [ ] Sem necessidade de zoom
- [ ] Grid se adapta corretamente

## 🌐 Teste de Conectividade

```
1. Parar o Backend
2. Tentar criar cliente no Frontend
3. ✓ Deve mostrar erro clara ("Erro ao salvar cliente")
4. Reiniciar Backend
5. ✓ Volta a funcionar
```

## 🐛 Logs para Debug

### Se houver erro na criação de cliente:

```bash
# Backend - Terminal 1
python manage.py runserver
# Procure por traceback ou error 500

# Frontend - DevTools
F12 → Network → POST request → Response
# Verifique mensagem de erro JSON
```

### Se houver CORS error:

```
Erro: Access to XMLHttpRequest blocked by CORS

Solução:
1. Verificar settings.py:
   CORS_ALLOWED_ORIGINS = [
       "http://127.0.0.1:5173",
       "http://127.0.0.1:5173",
   ]
2. Reiniciar Django
3. Tentar novamente
```

## 📝 Dados de Teste Sugeridos

Para popular rápido o sistema:

**Clientes:**
- João Silva (12345678900)
- Maria Santos (98765432100)
- Pedro Oliveira (11122233300)

**Motos:**
- Honda CB 500 2020 (ABC-1234)
- Yamaha YZF-R3 2021 (XYZ-5678)
- Kawasaki Ninja 400 2019 (DEF-9012)

**Agendamentos:**
- Troca de óleo (próxima semana)
- Reparo corrente (daqui 3 dias)
- Vistoria geral (próximo mês)

## ✨ Indicadores de Sucesso

✅ Sistema funcionando = quando:
1. Backend rodando sem erros
2. Frontend carregando sem console errors
3. CRUD completo funcionando (Create, Read, Update, Delete)
4. Dashboard mostrando números corretos
5. Dados persistindo no banco (recarregar página mantém dados)
6. Interface responsiva em diferentes tamanhos

## 🎯 Se Algo Não Funcionar

1. **Verificar terminals**
   - Backend rodando na porta 8000?
   - Frontend rodando na porta 5173?
   
2. **Limpar cache**
   - Frontend: Ctrl+Shift+Del → Clear cache
   - F5 para recarregar

3. **Reiniciar tudo**
   ```bash
   # Fechar terminals (Ctrl+C)
   # Abrir novos e reiniciar
   ```

4. **Verificar logs**
   ```bash
   # Backend
   python manage.py runserver (mostra erros)
   
   # Frontend
   F12 → Console (mostra erros)
   ```

5. **Verificar conexão**
   - Abra: http://127.0.0.1:8000/api/clientes/
   - Deve retornar JSON

## 🚀 Após Validação

Se tudo passou:
1. Sistema pronto para desenvolvimento
2. Pode começar Etapa 2
3. Dados podem ser resetados deletando `db.sqlite3`
4. Rodar `python manage.py migrate` novamente

---

**Próximo:** Siga para Etapa 2 (Histórico de Manutenções)
