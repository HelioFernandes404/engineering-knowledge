# GLPI CLI - Quick Start para LLMs

**Guia rápido: como um LLM começa a usar GLPI CLI em minutos.**

---

## ⚡ 5 Minutos: O Essencial

### 1. Verificar Instalação
```bash
glpi --version
# Output esperado: GLPI CLI version 1.0.0
```

### 2. Configurar Credenciais
```bash
export GLPI_URL="https://glpi.example.com/apirest.php"
export GLPI_APP_TOKEN="seu_app_token_aqui"
export GLPI_USER_TOKEN="seu_user_token_aqui"
```

### 3. Testar Conexão
```bash
glpi info
# Output esperado: Mostra config e ItemTypes disponíveis
```

### 4. Seu Primeiro Comando
```bash
# Listar 5 primeiros tickets
glpi list ticket --limit 5

# Output esperado:
# ┌────┬──────────────────┬────────┐
# │ ID │ Name             │ Status │
# ├────┼──────────────────┼────────┤
# │ 1  │ Email not work   │ New    │
# │ 2  │ Printer issue    │ Open   │
# └────┴──────────────────┴────────┘
```

### 5. Seu Primeiro Get
```bash
# Obter detalhes de um item específico
glpi get problem 12345

# Output esperado: Tabela com todos os campos do problema 12345
```

---

## 🎯 3 Padrões Mais Comuns

### Padrão 1: Listar Items
```bash
glpi list <tipo> [--limit N] [--json]

# Exemplos:
glpi list ticket           # Primeiros 50 tickets (padrão)
glpi list problem --limit 100  # Primeiros 100 problemas
glpi list computer --json  # Todos os computadores em JSON
```

### Padrão 2: Obter Detalhes
```bash
glpi get <tipo> <id> [--json]

# Exemplos:
glpi get ticket 5          # Detalhes do ticket 5
glpi get problem 12345     # Detalhes do problema 12345
glpi get computer 99 --json    # Computador 99 em JSON
```

### Padrão 3: Buscar por Critério
```bash
glpi search <tipo> --field 1 --value "seu_valor" [--json]

# Exemplos:
glpi search ticket --field 1 --value "bug"       # Tickets com "bug" no nome
glpi search problem --field 4 --value "Critical" # Problemas críticos
glpi search user --field 1 --value "John"        # Usuários com "John"
```

---

## 🔍 Exemplo Completo: Pesquisar e Detalhar

**Cenário:** Encontrar problema chamado "Network Down" e ver detalhes

### Passo 1: Buscar
```bash
glpi search problem --field 1 --value "Network Down"

# Output:
# ┌────┬──────────────────┬──────────┐
# │ ID │ Name             │ Status   │
# ├────┼──────────────────┼──────────┤
# │ 42 │ Network Down     │ Assigned │
# └────┴──────────────────┴──────────┘

# ID encontrado: 42
```

### Passo 2: Detalhar
```bash
glpi get problem 42

# Output:
# ┌──────────────────┬──────────────────────────────┐
# │ Field            │ Value                        │
# ├──────────────────┼──────────────────────────────┤
# │ ID               │ 42                           │
# │ Name             │ Network Down                 │
# │ Status           │ Assigned                     │
# │ Priority         │ Critical                     │
# │ Description      │ Main switch is down...       │
# │ Assigned To      │ Network Team                 │
# └──────────────────┴──────────────────────────────┘
```

---

## 📋 Referência: 7 Comandos Disponíveis

| Comando | Sintaxe | Propósito |
|---------|---------|----------|
| **list** | `glpi list <tipo>` | Listar vários items |
| **get** | `glpi get <tipo> <id>` | Detalhes de um item |
| **search** | `glpi search <tipo> --field N --value V` | Buscar com critério |
| **fingerprint** | `glpi fingerprint <tipo> <id>` | Dados especiais de 1 item |
| **fingerprints** | `glpi fingerprints <tipo>` | Listar dados especiais |
| **fingerprint-search** | `glpi fingerprint-search <tipo> --value V` | Buscar por dado especial |
| **info** | `glpi info` | Configuração do sistema |

---

## 🚗 Fluxo: Como LLM Deve Processar Instrução

```
ENTRADA: "Get em problem do id 12345"

├─ Extrair componentes:
│  ├─ Comando: GET
│  ├─ ItemType: PROBLEM
│  └─ ID: 12345
│
├─ Validar:
│  ├─ ItemType "PROBLEM" existe? SIM ✓
│  └─ ID "12345" é número? SIM ✓
│
├─ Construir comando:
│  └─ "glpi get problem 12345"
│
├─ Executar:
│  └─ $ glpi get problem 12345
│
└─ Responder ao usuário com resultado
```

---

## ⚠️ Erros Comuns

### Erro: "ItemType inválido"
```
PROBLEMA: glpi list xyz
OUTPUT: ✗ ItemType 'xyz' não é válido

SOLUÇÃO: Use ItemTypes válidos: ticket, problem, computer, user, etc.
         Ou execute: glpi info (para ver todos)
```

### Erro: "ID não é número"
```
PROBLEMA: glpi get ticket abc
OUTPUT: ✗ ID deve ser um número inteiro positivo

SOLUÇÃO: Use ID numérico: glpi get ticket 123
         Ou busque por nome: glpi search ticket --field 1 --value "abc"
```

### Erro: "Não autenticado"
```
PROBLEMA: glpi list ticket
OUTPUT: ✗ Não autenticado (401)

SOLUÇÃO: Configure credenciais:
  export GLPI_URL="https://glpi.example.com/apirest.php"
  export GLPI_APP_TOKEN="seu_token"
  export GLPI_USER_TOKEN="seu_token"
```

### Erro: "Não encontrado"
```
PROBLEMA: glpi get problem 99999
OUTPUT: ✗ Item 'problem' com ID '99999' não encontrado

SOLUÇÃO: ID não existe. Listar válidos:
  glpi list problem --limit 20
  Ou buscar por nome:
  glpi search problem --field 1 --value "seu_nome"
```

---

## 🔧 Dicas para LLM

### 1. Sempre Validar Entrada
```
Antes de executar, verificar:
  ✓ ItemType é válido?
  ✓ ID é número?
  ✓ Credenciais estão configuradas?
```

### 2. Use JSON para Integração
```bash
# Se máquina/script precisa processar:
glpi list ticket --json
# Retorna: JSON puro (mais fácil de parsear)

# Se humano precisa ler:
glpi list ticket
# Retorna: Tabela formatada (mais legível)
```

### 3. Paginação Para Listas Grandes
```bash
# Se precisa de muitos items:
glpi list ticket --limit 500       # Primeiros 500
glpi list ticket --start 500 --limit 500  # Próximos 500
glpi list ticket --start 1000 --limit 500 # Próximos 500
```

### 4. Tratamento de Erro
```bash
# Se erro contém "✗":
EXTRAIR mensagem
CLASSIFICAR tipo de erro
RESPONDER com solução

# Exemplo:
# ✗ Token inválido (401)
# → Erro de AUTENTICAÇÃO
# → Solução: Verificar GLPI_APP_TOKEN
```

### 5. Timeout é Crítico
```bash
# Sempre executar com timeout
subprocess.run(..., timeout=30)
# Se > 30s sem resposta: servidor pode estar offline
```

---

## 🏗️ Estrutura de Decisão Rápida

```
O que o usuário quer?

├─ "Listar X"
│  └─ glpi list <tipo>

├─ "Detalhes do X com id Y"
│  └─ glpi get <tipo> <id>

├─ "Encontra X que contém Y"
│  └─ glpi search <tipo> --field 1 --value "Y"

├─ "Busca X por status Y"
│  └─ glpi search <tipo> --field 4 --value "Y"

├─ "Fingerprint do X id Y"
│  └─ glpi fingerprint <tipo> <id>

├─ "X em JSON"
│  └─ Adicione "--json" ao comando anterior

└─ "Quantos X existem"
   └─ glpi list <tipo> --limit 1 --json
      (verá total no metadata)
```

---

## ✅ Checklist: LLM Pronto?

- [ ] Entendo os 7 comandos disponíveis?
- [ ] Sei como normalizar ItemType?
- [ ] Sei como validar ID?
- [ ] Sei como construir busca com --field --value?
- [ ] Sei como processar JSON vs tabela?
- [ ] Sei como lidar com paginação?
- [ ] Sei como detectar e classificar erros?
- [ ] Tenho timeout configurado?
- [ ] Sei como responder ao usuário?

---

## 📚 Próximos Passos

Depois de entender Quick Start:

1. **Decision Tree** (01-DECISION-TREE.md)
   → Entender fluxograma completo

2. **Command Reference** (02-COMMAND-REFERENCE.md)
   → Conhecer cada comando em detalhe

3. **Real World Examples** (03-EXAMPLES-REAL-WORLD.md)
   → Ver exemplos práticos complexos

4. **Error Handling** (04-ERROR-HANDLING.md)
   → Dominar tratamento de erros

5. **Execution Guide** (05-EXECUTION-GUIDE.md)
   → Implementar execução em código

---

## 🎓 Resumo de 30 Segundos

```
GLPI CLI é ferramenta para:
  → Listar items (tickets, problemas, computadores, etc)
  → Obter detalhes de um item
  → Buscar items por critério

Uso:
  glpi list <tipo>                              # Listar
  glpi get <tipo> <id>                          # Detalhar
  glpi search <tipo> --field N --value V        # Buscar

Erros:
  → Se "✗", há erro
  → Checar: autenticação, permissão, item existe, ID é número

LLM Deve:
  ✓ Validar entrada
  ✓ Construir comando correto
  ✓ Executar com timeout
  ✓ Processar resultado
  ✓ Responder apropriadamente
```

---

## 🚀 Pronto Para Começar!

Um LLM que leu este documento consegue:

✅ Receber instrução em linguagem natural
✅ Entender qual comando executar
✅ Construir comando preciso
✅ Executar com segurança
✅ Processar resposta
✅ Orientar usuário se erro

**Bem-vindo ao GLPI CLI! 🎉**

---

**Versão:** 1.0
**Data:** 2025-10-30
**Tempo de Leitura:** ~5 minutos
