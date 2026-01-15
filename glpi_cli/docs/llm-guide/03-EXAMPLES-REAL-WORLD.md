# GLPI CLI - Exemplos Práticos do Dia a Dia

Exemplos reais de como LLMs devem usar a CLI em cenários comuns.

---

## 📌 EXEMPLO 1: "Quero obter dados do problema com ID 12345"

**Entrada do Usuário:** "Get em problem do id 12345"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ Usuário quer OBTER detalhes de UM item específico

Passo 2: ItemType
  └─ "problem" → normalizar para "Problem"

Passo 3: Identificador
  └─ ID = 12345 (é número, válido ✓)

Passo 4: Comando a Executar
  └─ glpi get problem 12345

Passo 5: Formato de Saída
  └─ Usuário quer ver, portanto tabela (padrão)
```

### 🎬 Comando Executado
```bash
$ glpi get problem 12345
```

### 📊 Saída Esperada - Formato Tabela
```
┌────────────────────┬──────────────────────────────────────────┐
│ Field              │ Value                                    │
├────────────────────┼──────────────────────────────────────────┤
│ ID                 │ 12345                                    │
│ Name               │ Network Connectivity Issue in Wing A     │
│ Status             │ Assigned                                 │
│ Priority           │ High                                     │
│ Description        │ Users unable to access network...        │
│ Created On         │ 2025-01-10 09:30:00                     │
│ Last Modified      │ 2025-01-15 14:20:00                     │
│ Assigned To        │ John Tech Support                        │
│ Impact             │ Multiple Departments                     │
└────────────────────┴──────────────────────────────────────────┘
```

### 🔄 Variante: Mesmo Comando em JSON
```bash
$ glpi get problem 12345 --json
```

### 📋 Saída em JSON
```json
{
  "id": 12345,
  "name": "Network Connectivity Issue in Wing A",
  "status": "Assigned",
  "priority": "High",
  "description": "Users unable to access network...",
  "created_on": "2025-01-10T09:30:00Z",
  "last_modified": "2025-01-15T14:20:00Z",
  "assigned_to": "John Tech Support",
  "impact": "Multiple Departments"
}
```

### 🎯 Como LLM Deve Processar
```python
# Pseudocódigo
resultado = executar("glpi get problem 12345")

if resultado.contains("✗"):
    # Erro ocorreu
    extrair_mensagem_erro()
elif resultado.is_json():
    # JSON retornado
    dados = parse_json(resultado)
    retornar_para_usuario(dados)
else:
    # Tabela retornada
    retornar_para_usuario(resultado)
```

---

## 📌 EXEMPLO 2: "Quero listar todos os tickets"

**Entrada do Usuário:** "Lista de tickets"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ LISTAR múltiplos items do mesmo tipo

Passo 2: ItemType
  └─ "tickets" → normalizar para "Ticket"

Passo 3: Parâmetros
  └─ Sem limite especificado → usar padrão (50)

Passo 4: Comando
  └─ glpi list ticket
```

### 🎬 Comando Executado
```bash
$ glpi list ticket
```

### 📊 Saída Esperada
```
┌────┬──────────────────────────┬──────────────┬──────────────────┐
│ ID │ Name                     │ Status       │ Last Modified    │
├────┼──────────────────────────┼──────────────┼──────────────────┤
│ 1  │ Email not working        │ New          │ 2025-01-20       │
│ 2  │ Printer driver issue     │ In Progress  │ 2025-01-19       │
│ 3  │ Password reset request   │ Resolved     │ 2025-01-18       │
│ 4  │ Access denied to folder  │ New          │ 2025-01-17       │
│ 5  │ Software installation    │ In Progress  │ 2025-01-16       │
│ ... (45 mais)                                                     │
└────┴──────────────────────────┴──────────────┴──────────────────┘
```

### 🔄 Variante: Limitar Resultado
```bash
$ glpi list ticket --limit 5
```

### 📊 Saída (Primeiros 5)
```
┌────┬──────────────────────────┬──────────────┬──────────────────┐
│ ID │ Name                     │ Status       │ Last Modified    │
├────┼──────────────────────────┼──────────────┼──────────────────┤
│ 1  │ Email not working        │ New          │ 2025-01-20       │
│ 2  │ Printer driver issue     │ In Progress  │ 2025-01-19       │
│ 3  │ Password reset request   │ Resolved     │ 2025-01-18       │
│ 4  │ Access denied to folder  │ New          │ 2025-01-17       │
│ 5  │ Software installation    │ In Progress  │ 2025-01-16       │
└────┴──────────────────────────┴──────────────┴──────────────────┘
```

### 🔄 Variante: Paginação (proximos 5, começando do 6º)
```bash
$ glpi list ticket --start 5 --limit 5
```

### 🔄 Variante: Resultado em JSON
```bash
$ glpi list ticket --limit 3 --json
```

### 📋 Saída em JSON
```json
[
  {
    "id": 1,
    "name": "Email not working",
    "status": "New",
    "last_modified": "2025-01-20"
  },
  {
    "id": 2,
    "name": "Printer driver issue",
    "status": "In Progress",
    "last_modified": "2025-01-19"
  },
  {
    "id": 3,
    "name": "Password reset request",
    "status": "Resolved",
    "last_modified": "2025-01-18"
  }
]
```

---

## 📌 EXEMPLO 3: "Buscar todos os computadores com status 'Active'"

**Entrada do Usuário:** "Procura computadores ativos"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ BUSCAR items com um critério específico

Passo 2: ItemType
  └─ "computadores" → normalizar para "Computer"

Passo 3: Critério
  └─ Campo: status (padrão field 4 para Computer)
  └─ Valor: "Active"
  └─ Tipo: equals (procura exata)

Passo 4: Comando
  └─ glpi search computer --field 4 --value "Active" --searchtype equals
```

### 🎬 Comando Executado
```bash
$ glpi search computer --field 4 --value "Active" --searchtype equals
```

### 📊 Saída Esperada
```
┌────┬──────────────────────────┬────────┬──────────────────┐
│ ID │ Name                     │ Status │ Last Modified    │
├────┼──────────────────────────┼────────┼──────────────────┤
│ 1  │ DESKTOP-JOHN-001         │ Active │ 2025-01-15       │
│ 3  │ LAPTOP-MARIA-002         │ Active │ 2025-01-20       │
│ 5  │ WORKSTATION-ENG-001      │ Active │ 2025-01-18       │
│ 7  │ SERVER-BACKUP-001        │ Active │ 2025-01-16       │
└────┴──────────────────────────┴────────┴──────────────────┘
```

---

## 📌 EXEMPLO 4: "Buscar tickets que contenham 'bug' no nome"

**Entrada do Usuário:** "Encontra tickets com 'bug'"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ BUSCAR items onde nome contém um valor

Passo 2: ItemType
  └─ "tickets" → normalizar para "Ticket"

Passo 3: Critério
  └─ Campo: name (field 1)
  └─ Valor: "bug"
  └─ Tipo: contains (substring, padrão)

Passo 4: Comando
  └─ glpi search ticket --field 1 --value "bug"
```

### 🎬 Comando Executado
```bash
$ glpi search ticket --field 1 --value "bug"
```

### 📊 Saída Esperada
```
┌────┬──────────────────────────────────┬────────┐
│ ID │ Name                             │ Status │
├────┼──────────────────────────────────┼────────┤
│ 15 │ Bug in login form                │ New    │
│ 27 │ Critical bug report - UI crash   │ Open   │
│ 42 │ Minor bug in search feature      │ Closed │
│ 88 │ bug fix needed for export        │ Open   │
└────┴──────────────────────────────────┴────────┘
```

---

## 📌 EXEMPLO 5: "Obter fingerprint do computador ID 5"

**Entrada do Usuário:** "Fingerprint do computador 5"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ OBTER dados especiais (Plugin Field)

Passo 2: ItemType
  └─ "computador" → normalizar para "Computer"

Passo 3: ID
  └─ 5 (válido ✓)

Passo 4: Comando
  └─ glpi fingerprint computer 5
```

### 🎬 Comando Executado
```bash
$ glpi fingerprint computer 5
```

### 📊 Saída Esperada
```
┌───────────────┬──────────────────────────────────────────────┐
│ Field         │ Value                                        │
├───────────────┼──────────────────────────────────────────────┤
│ id            │ 5                                            │
│ fingerprint   │ a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6          │
│ modified      │ 2025-01-15T10:30:00Z                        │
└───────────────┴──────────────────────────────────────────────┘
```

---

## 📌 EXEMPLO 6: "Buscar computador por fingerprint ABC123"

**Entrada do Usuário:** "Qual computador tem fingerprint ABC123?"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ BUSCAR item pelo valor de Plugin Field

Passo 2: ItemType
  └─ "computador" → normalizar para "Computer"

Passo 3: Valor
  └─ fingerprint = "ABC123"

Passo 4: Comando
  └─ glpi fingerprint-search computer --value "ABC123"
```

### 🎬 Comando Executado
```bash
$ glpi fingerprint-search computer --value "ABC123"
```

### 📊 Saída Esperada
```
┌────┬───────────────────────┬──────────────────┐
│ ID │ Name                  │ Fingerprint      │
├────┼───────────────────────┼──────────────────┤
│ 15 │ WORKSTATION-JOHN-001  │ ABC123           │
└────┴───────────────────────┴──────────────────┘
```

---

## 📌 EXEMPLO 7: Fluxo Completo - "Pesquisa um problema e mostra detalhes"

**Entrada do Usuário:** "Encontra o problema chamado 'Network Down' e mostra detalhes"

### 🧠 Análise LLM - Passo a Passo

#### PASSO 1: Buscar o Problema
```bash
$ glpi search problem --field 1 --value "Network Down"
```

Resultado:
```
┌────┬──────────────────┬──────────────┐
│ ID │ Name             │ Status       │
├────┼──────────────────┼──────────────┤
│ 42 │ Network Down     │ Assigned     │
└────┴──────────────────┴──────────────┘
```

#### PASSO 2: Extrair ID e Obter Detalhes
```bash
$ glpi get problem 42
```

Resultado:
```
┌────────────────────┬──────────────────────────────────────────┐
│ Field              │ Value                                    │
├────────────────────┼──────────────────────────────────────────┤
│ ID                 │ 42                                       │
│ Name               │ Network Down                             │
│ Status             │ Assigned                                 │
│ Priority           │ Critical                                 │
│ Description        │ Main network switch is down...           │
│ Created On         │ 2025-01-20 08:15:00                     │
│ Assigned To        │ Network Team                             │
│ Impact             │ All Departments                          │
└────────────────────┴──────────────────────────────────────────┘
```

#### PASSO 3: Retornar ao Usuário
```
Encontrado! Problema #42:
- Nome: Network Down
- Status: Assigned
- Prioridade: Critical
- Descrição: Main network switch is down...
- Atribuído a: Network Team
```

---

## 📌 EXEMPLO 8: Tratamento de Erro - ItemType Inválido

**Entrada do Usuário:** "Lista de xyz"

### 🧠 Análise LLM
```
Passo 1: ItemType recebido = "xyz"

Passo 2: Validar se é ItemType conhecido
  └─ "xyz" não está na lista de ItemTypes válidos ✗

Passo 3: Tentar normalizar
  └─ "xyz" não corresponde a nenhum ItemType conhecido

Passo 4: Executar mesmo assim (para ver erro da API)
  └─ glpi list xyz
```

### 🎬 Comando Executado
```bash
$ glpi list xyz
```

### 📊 Saída de Erro
```
✗ ItemType 'xyz' não é válido

ItemTypes válidos:
Computer, Monitor, Printer, NetworkEquipment, Peripheral, Phone,
Software, SoftwareLicense, SoftwareVersion, Ticket, TicketFollowup,
TicketTask, TicketValidation, ITILCategory, Problem, Change, Solution,
SolutionTemplate, User, Group, Entity, Profile, Location, Supplier,
Contact, Contract, Budget, Document, DocumentType, KnowbaseItem,
Network, NetworkPort, NetworkName, IPAddress, IPNetwork, FQDN, Vlan,
Project, ProjectTask, Reminder, RSSFeed, Reservation, Log, Event,
CronTask, Config, Plugin
```

### 🤖 Resposta LLM ao Usuário
```
Erro: ItemType 'xyz' não é válido.

Você quis dizer um desses?
- Computer (computador)
- User (usuário)
- Ticket (ticket)
- Problem (problema)

Ou use: glpi info
para ver todos os ItemTypes disponíveis
```

---

## 📌 EXEMPLO 9: Tratamento de Erro - Item Não Encontrado

**Entrada do Usuário:** "Get problem 99999"

### 🧠 Análise LLM
```
Passo 1: Intenção = OBTER item específico

Passo 2: ItemType = "problem" ✓

Passo 3: ID = 99999 (número válido ✓)

Passo 4: Executar
  └─ glpi get problem 99999
```

### 🎬 Comando Executado
```bash
$ glpi get problem 99999
```

### 📊 Saída de Erro
```
✗ Item 'problem' com ID '99999' não encontrado
```

### 🤖 Resposta LLM ao Usuário
```
Problema não encontrado. O ID 99999 não existe no sistema.

Você pode:
1. Verificar o ID correto com: glpi list problem --limit 20
2. Buscar por nome: glpi search problem --field 1 --value "seu_nome"
3. Ver: glpi info
```

---

## 📌 EXEMPLO 10: Processamento de JSON para Integração

**Entrada do Usuário (Sistema Externo):** "Preciso de todos os tickets ativos em JSON"

### 🧠 Análise LLM
```
Passo 1: Intenção
  └─ LISTAR items em formato MÁQUINA (JSON)

Passo 2: ItemType
  └─ "ticket" → "Ticket"

Passo 3: Critério
  └─ Status = "Active" (ou similar)
  └─ Comando 1: buscar quais são "active"
  └─ Comando 2: retornar em JSON

Passo 4: Executar
  └─ glpi search ticket --field 4 --value "Active" --json
```

### 🎬 Comando Executado
```bash
$ glpi search ticket --field 4 --value "Active" --json
```

### 📋 Saída em JSON (Puro, sem formatação)
```json
[
  {
    "id": 1,
    "name": "Email not working",
    "status": "Active",
    "priority": "Medium",
    "created_on": "2025-01-10T09:00:00Z",
    "assigned_to": "Support Team"
  },
  {
    "id": 4,
    "name": "Access denied to folder",
    "status": "Active",
    "priority": "High",
    "created_on": "2025-01-12T14:30:00Z",
    "assigned_to": "IT Team"
  },
  {
    "id": 5,
    "name": "Software installation",
    "status": "Active",
    "priority": "Low",
    "created_on": "2025-01-15T11:00:00Z",
    "assigned_to": "Admin"
  }
]
```

### 🤖 LLM Processa JSON
```python
import json
import subprocess

# Executar comando
resultado = subprocess.run(
    ["glpi", "search", "ticket", "--field", "4",
     "--value", "Active", "--json"],
    capture_output=True,
    text=True
)

# Parsear JSON
tickets = json.loads(resultado.stdout)

# Processar dados
for ticket in tickets:
    print(f"Ticket #{ticket['id']}: {ticket['name']}")
    # Enviar para sistema externo, BD, etc.
```

---

## 🔗 Próximo Passo

Ver: **04-ERROR-HANDLING.md** para tratamento detalhado de erros
