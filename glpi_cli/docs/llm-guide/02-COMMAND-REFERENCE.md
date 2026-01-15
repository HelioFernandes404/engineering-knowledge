# GLPI CLI - Command Reference para LLMs

Documentação completa da sintaxe de cada comando para execução por LLMs.

## 🎬 Sintaxe Geral

```
glpi [COMANDO] [ARGUMENTOS] [FLAGS]
```

### Convenções
- `<>` = argumento obrigatório
- `[]` = argumento opcional
- `--flag` = flag (booleano ou com valor)

---

## 📋 COMANDO: list

Lista todos os items de um tipo específico.

### Sintaxe
```bash
glpi list <itemtype> [--limit N] [--start N] [--json]
```

### Argumentos Obrigatórios
```
<itemtype>
  Tipo de item a listar (Computer, Ticket, Problem, etc)
  Exemplo: ticket, computer, problem
  Nota: case-insensitive, será normalizado
```

### Flags Opcionais
```
--limit N
  Número máximo de items a retornar
  Padrão: 50
  Máximo recomendado: 1000
  Exemplo: --limit 100

--start N
  Índice inicial para paginação
  Padrão: 0
  Uso: Para pegar próximos N items, use --start N --limit M
  Exemplo: --start 50 --limit 50 (items 51-100)

--json
  Retorna resultado em JSON em vez de tabela formatada
  Padrão: FALSE (retorna tabela)
  Uso: Quando LLM precisa processar dados
  Exemplo: glpi list ticket --json
```

### Exemplos de Uso
```bash
# Listar 50 primeiros tickets (padrão)
glpi list ticket

# Listar 100 computadores
glpi list computer --limit 100

# Listar problemas em formato JSON
glpi list problem --json

# Paginação: próximos 50 items (51-100)
glpi list ticket --start 50 --limit 50

# Todos os argumentos
glpi list user --limit 200 --start 100 --json
```

### Saída Esperada
```
Sucesso (formato tabela):
┌────┬──────────────────┬─────────────────┬──────────┐
│ ID │ Name             │ Status          │ Modified │
├────┼──────────────────┼─────────────────┼──────────┤
│ 1  │ My Ticket        │ New             │ 2025-01  │
│ 2  │ Another Ticket   │ In Progress     │ 2025-01  │
└────┴──────────────────┴─────────────────┴──────────┘

Sucesso (formato JSON):
[
  {"id": 1, "name": "My Ticket", "status": "New"},
  {"id": 2, "name": "Another Ticket", "status": "In Progress"}
]

Erro (ItemType inválido):
✗ ItemType 'invalid' não é válido
```

### Detecção de Erros
```
Se output contém "✗" ou começa com "ERROR" → operação falhou
Se output é lista vazia [] → nenhum item encontrado (normal)
Se timeout → adicionar --json para debug
```

---

## 🔍 COMANDO: get

Obtém um item específico pelo ID.

### Sintaxe
```bash
glpi get <itemtype> <id> [--json]
```

### Argumentos Obrigatórios
```
<itemtype>
  Tipo de item (Computer, Ticket, Problem, etc)
  Exemplo: ticket, problem, computer

<id>
  ID numérico do item
  Deve ser um número inteiro positivo
  Exemplo: 12345
```

### Flags Opcionais
```
--json
  Retorna resultado em JSON em vez de tabela
  Padrão: FALSE
  Uso: Quando LLM precisa processar resultado
```

### Exemplos de Uso
```bash
# Obter ticket com ID 5
glpi get ticket 5

# Obter problema com ID 12345
glpi get problem 12345

# Obter computador com ID 999 em JSON
glpi get computer 999 --json

# Obter usuário com ID 1
glpi get user 1
```

### Saída Esperada
```
Sucesso (tabela):
┌─────────────────┬──────────────────────────────────┐
│ Field           │ Value                            │
├─────────────────┼──────────────────────────────────┤
│ ID              │ 12345                            │
│ Name            │ My Ticket                        │
│ Status          │ New                              │
│ Description     │ This is a test ticket            │
└─────────────────┴──────────────────────────────────┘

Sucesso (JSON):
{
  "id": 12345,
  "name": "My Ticket",
  "status": "New",
  "description": "This is a test ticket"
}

Erro (não encontrado):
✗ Item 'problem' com ID '99999' não encontrado
```

### Detecção de Erros
```
"não encontrado" → Item não existe (404)
"sem permissão" → Usuário não tem acesso (403)
"não é um ItemType" → Type inválido (400)
```

---

## 🔎 COMANDO: search

Busca items com critérios específicos.

### Sintaxe
```bash
glpi search <itemtype> --field <id> --value <valor> [--searchtype tipo] [--json]
```

### Argumentos Obrigatórios
```
<itemtype>
  Tipo de item a buscar (Ticket, Computer, Problem, etc)

--field <id>
  ID do campo onde buscar
  Padrão: 1 (name)
  Exemplos:
    1 = name (padrão)
    4 = status
    12 = priority
  Nota: IDs variam por ItemType. Se desconhecido, usar --json em get

--value <valor>
  Valor a buscar
  Se contém espaços, use aspas: "My Value"
```

### Flags Opcionais
```
--searchtype tipo
  Como fazer a busca
  Valores: contains (padrão), equals, under
  Padrão: contains (busca substring)
  Exemplo: --searchtype equals (apenas igualdade exata)

--json
  Retorna resultado em JSON em vez de tabela
  Padrão: FALSE
```

### Exemplos de Uso
```bash
# Buscar tickets com "bug" no nome
glpi search ticket --field 1 --value "bug"

# Buscar tickets com status exato = "New"
glpi search ticket --field 4 --value "New" --searchtype equals

# Buscar computadores com status "In Use"
glpi search computer --field 4 --value "In Use"

# Mesmo resultado em JSON
glpi search ticket --field 1 --value "bug" --json

# Buscar com espaços
glpi search ticket --field 1 --value "Bug Report" --searchtype contains
```

### Saída Esperada
```
Sucesso (1+ resultados):
┌────┬──────────────────┬─────────┐
│ ID │ Name             │ Status  │
├────┼──────────────────┼─────────┤
│ 5  │ Bug Report 1     │ New     │
│ 12 │ Bug Fix Request  │ Closed  │
└────┴──────────────────┴─────────┘

Sucesso (nenhum resultado):
[] (lista vazia)

Sucesso (JSON):
[
  {"id": 5, "name": "Bug Report 1", "status": "New"},
  {"id": 12, "name": "Bug Fix Request", "status": "Closed"}
]
```

### Detecção de Erros
```
"field não existe" → Field ID inválido para este ItemType
"valor inválido" → Formato de valor não aceito
[] (vazio) → Nenhum resultado encontrado (normal, não é erro)
```

---

## 👆 COMANDO: fingerprint

Obtém fingerprint (Plugin Fields) de um item específico.

### Sintaxe
```bash
glpi fingerprint <itemtype> <id> [--json]
```

### Argumentos Obrigatórios
```
<itemtype>
  Tipo de item que tem Plugin Fields (Computer, NetworkEquipment, etc)

<id>
  ID numérico do item
```

### Flags Opcionais
```
--json
  Retorna resultado em JSON
  Padrão: FALSE
```

### Exemplos de Uso
```bash
# Obter fingerprint do computador 5
glpi fingerprint computer 5

# Obter fingerprint em JSON
glpi fingerprint computer 5 --json

# Obter fingerprint de equipment de rede
glpi fingerprint networkequipment 123
```

### Saída Esperada
```
Sucesso (tabela):
┌──────────┬──────────────────────┐
│ Field    │ Value                │
├──────────┼──────────────────────┤
│ id       │ 5                    │
│ value    │ ABC123XYZ            │
│ modified │ 2025-01-15T10:30:00Z │
└──────────┴──────────────────────┘

Sucesso (JSON):
{
  "id": 5,
  "value": "ABC123XYZ",
  "modified": "2025-01-15T10:30:00Z"
}

Erro (sem Plugin Fields):
✗ Plugin Field não disponível para este ItemType
```

---

## 📚 COMANDO: fingerprints

Lista todos os fingerprints de um ItemType.

### Sintaxe
```bash
glpi fingerprints <itemtype> [--limit N] [--start N] [--json]
```

### Argumentos e Flags
Mesmo que `list` (veja acima).

### Exemplos de Uso
```bash
# Listar todos os fingerprints de computadores
glpi fingerprints computer

# Primeiros 100
glpi fingerprints computer --limit 100

# Paginação + JSON
glpi fingerprints computer --start 50 --limit 50 --json
```

---

## 🔍 COMANDO: fingerprint-search

Busca items por valor de fingerprint.

### Sintaxe
```bash
glpi fingerprint-search <itemtype> --value <valor> [--json]
```

### Argumentos Obrigatórios
```
<itemtype>
  Tipo de item (Computer, NetworkEquipment, etc)

--value <valor>
  Valor de fingerprint a buscar
  Exemplo: "ABC123" ou "CPU-HASH-VALUE"
```

### Exemplos de Uso
```bash
# Buscar computador por fingerprint
glpi fingerprint-search computer --value "ABC123XYZ"

# Resultado em JSON
glpi fingerprint-search computer --value "ABC123XYZ" --json
```

### Saída Esperada
```
Sucesso (encontrado):
┌────┬──────────────────┬──────────────┐
│ ID │ Name             │ Fingerprint  │
├────┼──────────────────┼──────────────┤
│ 5  │ My Computer      │ ABC123XYZ    │
└────┴──────────────────┴──────────────┘

Sucesso (não encontrado):
[] (lista vazia)
```

---

## ℹ️ COMANDO: info

Exibe informações do sistema e configuração.

### Sintaxe
```bash
glpi info
```

### Sem argumentos ou flags

### Exemplos de Uso
```bash
# Mostrar configuração
glpi info
```

### Saída Esperada
```
╔════════════════════════════════════════╗
║         GLPI CLI Configuration         ║
╠════════════════════════════════════════╣
│ URL: https://glpi.example.com/...     │
│ Versão CLI: 1.0.0                     │
├────────────────────────────────────────┤
║      Available ItemTypes (40+)         ║
├────────────────────────────────────────┤
│ Computer, Monitor, Printer, ...        │
│ Ticket, Problem, Change, ...           │
│ User, Group, Entity, ...               │
└────────────────────────────────────────┘
```

---

## 🚀 Padrões para LLMs

### Padrão 1: Construção Progressiva
```
1. User input → parse intenção
2. Determinar ItemType → normalizar
3. Extrair parâmetros → --field, --value, --limit
4. Construir comando → glpi [cmd] [args] [flags]
5. Executar e processar resultado
```

### Padrão 2: Validação de Entrada
```
Antes de executar, validar:
  ✓ ItemType válido ou normalizável?
  ✓ ID é número (se necessário)?
  ✓ Field ID é número (se especificado)?
  ✓ Espaços em valor? (adicionar aspas)
  ✓ Limit em range [1, 1000]?
```

### Padrão 3: Processamento de Saída
```
Após execução:
  ✓ Verificar se contém "✗" ou "ERROR"
  ✓ Se erro, parsear mensagem
  ✓ Se sucesso, parsear conforme --json ou --table
  ✓ Retornar dados estruturados ao user
```

---

## 📊 Tabela Rápida de Referência

| Comando | Sintaxe | Quando Usar |
|---------|---------|------------|
| **list** | `glpi list <type>` | Listar todos items |
| **get** | `glpi get <type> <id>` | Um item específico |
| **search** | `glpi search <type> --field <id> --value <v>` | Buscar com critério |
| **fingerprint** | `glpi fingerprint <type> <id>` | Plugin Field de 1 item |
| **fingerprints** | `glpi fingerprints <type>` | Listar Plugin Fields |
| **fingerprint-search** | `glpi fingerprint-search <type> --value <v>` | Buscar por Plugin Field |
| **info** | `glpi info` | Configuração do sistema |

---

## 🔗 Próximo Passo

Ver: **03-EXAMPLES-REAL-WORLD.md** para exemplos práticos completos
