# GLPI CLI - Decision Tree para LLMs

Esta seção ajuda LLMs a determinar qual comando usar baseado na intenção do usuário.

## 📊 Decision Tree - Qual comando usar?

```
┌─ Quero FAZER algo com dados GLPI?
│
├─► Visualizar/Obter dados?
│   ├─► Listar vários items do mesmo tipo?
│   │   └─► USAR: glpi list <itemtype>
│   │       Exemplo: glpi list ticket
│   │       Retorna: Lista formatada ou JSON de todos os items
│   │
│   ├─► Obter UM item específico pelo ID?
│   │   └─► USAR: glpi get <itemtype> <id>
│   │       Exemplo: glpi get problem 12345
│   │       Retorna: Detalhes completos do item específico
│   │
│   └─► Buscar items com critérios?
│       └─► USAR: glpi search <itemtype> --field <id> --value <valor>
│           Exemplo: glpi search ticket --field 1 --value "Bug"
│           Retorna: Items que correspondem ao critério
│
├─► Acessar dados especiais (Fingerprints)?
│   ├─► Obter fingerprint de UM item?
│   │   └─► USAR: glpi fingerprint <itemtype> <id>
│   │       Exemplo: glpi fingerprint computer 5678
│   │
│   ├─► Listar todos os fingerprints?
│   │   └─► USAR: glpi fingerprints <itemtype>
│   │       Exemplo: glpi fingerprints computer
│   │
│   └─► Buscar por valor de fingerprint?
│       └─► USAR: glpi fingerprint-search <itemtype> --value <valor>
│           Exemplo: glpi fingerprint-search computer --value "ABC123"
│
└─► Obter informações do sistema?
    └─► USAR: glpi info
        Retorna: Configuração atual, ItemTypes disponíveis
```

## 🎯 Mapeamento de Intenções → Comandos

### Intenção: "Quero listar todos os tickets"
```
Análise:
  - Ação: LISTAR (múltiplos items)
  - Recurso: TICKET
  - Comando: glpi list ticket
  - Alternativas: --limit 100 (mais itens), --json (formato máquina)
```

### Intenção: "Quero obter detalhes do problema com ID 5000"
```
Análise:
  - Ação: OBTER (um item específico)
  - Recurso: PROBLEM
  - Identificador: 5000
  - Comando: glpi get problem 5000
  - Alternativas: --json (formato máquina)
```

### Intenção: "Quero encontrar todos os computadores com fingerprint ABC123"
```
Análise:
  - Ação: BUSCAR (por valor especial)
  - Recurso: COMPUTER (com Plugin Fields)
  - Campo: fingerprint
  - Valor: ABC123
  - Comando: glpi fingerprint-search computer --value "ABC123"
```

### Intenção: "Quero buscar tickets com status 'Aberto'"
```
Análise:
  - Ação: BUSCAR (com critério)
  - Recurso: TICKET
  - Campo: status (ou ID do campo)
  - Valor: "Aberto"
  - Comando: glpi search ticket --field 12 --value "Aberto"
  - Nota: Field ID pode variar, usar --json para verificar estrutura
```

## 📋 ItemTypes Disponíveis

LLM deve normalizar entrada do usuário para esses ItemTypes (case-insensitive, converte para PascalCase):

### Infraestrutura & Assets (9)
```
Computer, Monitor, Printer, NetworkEquipment, Peripheral,
Phone, Software, SoftwareLicense, SoftwareVersion
```

### Helpdesk & Tickets (8)
```
Ticket, TicketFollowup, TicketTask, TicketValidation,
ITILCategory, Problem, Change, Solution, SolutionTemplate
```

### Gerenciamento (11)
```
User, Group, Entity, Profile, Location, Supplier, Contact,
Contract, Budget, Document, DocumentType, KnowbaseItem
```

### Rede (7)
```
Network, NetworkPort, NetworkName, IPAddress, IPNetwork, FQDN, Vlan
```

### Outros (5)
```
Project, ProjectTask, Reminder, RSSFeed, Reservation
```

### Administrativo (5)
```
Log, Event, CronTask, Config, Plugin
```

## 🔄 Fluxo de Decisão Detalhado

```
PASSO 1: Entender a Intenção
   └─ Extrair: O que o usuário quer fazer?
      ├─ LISTAR todos?
      ├─ OBTER um específico?
      ├─ BUSCAR com critério?
      └─ ACESSAR dados especiais?

PASSO 2: Identificar o Recurso (ItemType)
   └─ Qual tipo de dado?
      ├─ Ticket, Problem, Computer, User, etc.
      └─ Normalizar para PascalCase

PASSO 3: Extrair Parâmetros
   └─ Se precisa de:
      ├─ ID do item → incluir <id>
      ├─ Valor de busca → incluir --value
      ├─ Campo específico → incluir --field
      └─ Limite/paginação → incluir --limit/--start

PASSO 4: Escolher Formato de Saída
   └─ Como o resultado será usado?
      ├─ Humano lê → formato TABLE (padrão)
      └─ Máquina processa → formato JSON (--json)

PASSO 5: Construir Comando
   └─ glpi [comando] [args] [flags]
```

## ⚡ Atalhos para LLMs

Se o usuário diz... | LLM deve executar...
---|---
"lista de X" | `glpi list <itemtype>`
"detalhes do X com id Y" | `glpi get <itemtype> <id>`
"encontra todos X com Y = Z" | `glpi search <itemtype> --field <field_id> --value "Z"`
"fingerprint do X id Y" | `glpi fingerprint <itemtype> <id>`
"busca fingerprint com valor Z" | `glpi fingerprint-search <itemtype> --value "Z"`
"quantos X existem" | `glpi list <itemtype> --limit 1` (apenas conta)
"X em formato JSON" | Adicione `--json` ao comando

## 📊 Ordem de Prioridade de Busca

Quando o usuário menciona um campo para busca, LLM deve tentar nessa ordem:

1. **Nome/Descrição** → field 1 (padrão)
2. **Status** → field 12 (comum em tickets)
3. **Estado** → field 4 (comum em assets)
4. **Valor customizado** → informar ao usuário que precisa do field ID exato

Se field ID é desconhecido, executar com `--json` para inspecionar estrutura.

## ✅ Validações Antes de Executar

LLM deve verificar:

- [ ] ItemType é válido? (caso não, tentar normalizar)
- [ ] ID fornecido é número? (se necessário)
- [ ] Field ID é número? (se especificado)
- [ ] Valor de busca tem espaços? (adicionar aspas se sim)
- [ ] Limite está entre 1 e 1000? (padrão 50)

Exemplo de validação:
```python
# Entrada: "get ticket abc"
ItemType: ticket → válido ✓
ID: abc → NÃO é número ✗
Ação: Perguntar ao usuário ou usar como busca
```

## 🔍 Exemplo: "Quero obter dados do problema 12345"

```
Entrada: "get problema 12345"

Análise LLM:
  1. Intenção → OBTER um item específico
  2. ItemType → "problema" → normalizar para "Problem"
  3. ID → "12345" → válido (é número)
  4. Comando → glpi get problem 12345
  5. Executar → Sistema retorna detalhes do problema

Esperado:
  ├─ Status: 200 OK
  ├─ Saída: Detalhes do problema em formato tabela/JSON
  └─ Erro possível: Problema não encontrado (404)
```

## 🔗 Próximo Passo

Ver: **02-COMMAND-REFERENCE.md** para sintaxe exata de cada comando
