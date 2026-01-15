# GLPI CLI - Execution Guide para LLMs

Guia prático e passo-a-passo de como um LLM deve executar e processar comandos GLPI.

---

## 🎯 Ciclo de Vida de uma Execução GLPI

```
1. RECEBER instrução do usuário
   ↓
2. ANALISAR intenção (Decision Tree)
   ↓
3. NORMALIZAR entrada (ItemType, IDs, etc)
   ↓
4. VALIDAR argumentos (tipos, ranges, etc)
   ↓
5. CONSTRUIR comando exato (Command Reference)
   ↓
6. EXECUTAR comando no shell
   ↓
7. PROCESSAR output (sucesso/erro)
   ↓
8. FORMATAR resposta ao usuário
```

---

## 📥 PASSO 1: Receber Instrução

LLM recebe instruções em linguagem natural.

### Exemplos de Entrada
```
"Get em problem do id xxxx"
"Quero detalhes do problema 12345"
"Obtém problema 12345"
"Busca problema 5000"
"Mostra problema id 5000"
```

### Análise Inicial
```
Extrair componentes:
  ├─ Ação: GET / OBTER / DETALHES
  ├─ ItemType: PROBLEM
  ├─ Identificador: 12345 / 5000 / xxxx
  └─ Formato: (não especificado = tabela)
```

---

## 🧠 PASSO 2: Analisar Intenção

Usar Decision Tree (01-DECISION-TREE.md) para determinar comando.

### Matriz de Análise
```
ENTRADA          │ AÇÃO        │ COMANDO INFERIDO
─────────────────┼─────────────┼──────────────────────────────────
"lista X"        │ LISTAR      │ glpi list <itemtype>
"get X id Y"     │ OBTER       │ glpi get <itemtype> <id>
"busca X Y"      │ BUSCAR      │ glpi search <itemtype> --field ? --value Y
"fingerprint X Y"│ ESPECIAL    │ glpi fingerprint <itemtype> <id>
"info"           │ INFO        │ glpi info
"X em JSON"      │ (qualquer)  │ [comando anterior] --json
```

### Pseudocódigo
```python
def analisar_intencao(entrada: str) -> str:
    """Retorna comando GLPI a ser executado"""
    entrada_lower = entrada.lower()

    # Detectar padrões
    if "list" in entrada_lower or "lista" in entrada_lower:
        return "LISTAR"
    elif "get" in entrada_lower or "detalhes" in entrada_lower:
        return "OBTER"
    elif "busca" in entrada_lower or "encontra" in entrada_lower:
        return "BUSCAR"
    elif "fingerprint" in entrada_lower:
        return "FINGERPRINT"
    else:
        return "DESCONHECIDA"
```

---

## 🔧 PASSO 3: Normalizar Entrada

Converter entrada de usuário para formato esperado.

### 3.1 Normalizar ItemType

```python
def normalizar_itemtype(entrada: str) -> str:
    """
    Converte entrada para PascalCase
    Exemplo: "ticket" → "Ticket"
             "computer" → "Computer"
             "PROBLEM" → "Problem"
    """
    ITEMTYPE_MAP = {
        "ticket": "Ticket",
        "problem": "Problem",
        "computer": "Computer",
        "user": "User",
        "monitor": "Monitor",
        "printer": "Printer",
        "networkequipment": "NetworkEquipment",
        # ... 30+ mais
    }

    entrada_lower = entrada.lower().replace(" ", "")
    return ITEMTYPE_MAP.get(entrada_lower, None)

# Uso
itemtype = normalizar_itemtype("TICKET")  # → "Ticket"
```

### 3.2 Validar ID

```python
def validar_id(id_str: str) -> bool:
    """ID deve ser número inteiro positivo"""
    try:
        id_num = int(id_str)
        return id_num > 0
    except ValueError:
        return False

# Uso
valido = validar_id("12345")  # → True
valido = validar_id("abc")    # → False
```

### 3.3 Validar Field ID

```python
def validar_field_id(field_id: str) -> bool:
    """Field ID deve ser número"""
    try:
        field_num = int(field_id)
        return field_num >= 1
    except ValueError:
        return False

# Uso
valido = validar_field_id("1")    # → True
valido = validar_field_id("abc")  # → False
```

### 3.4 Escapar Aspas em Valores

```python
def preparar_valor(valor: str) -> str:
    """Adiciona aspas se contém espaços"""
    if " " in valor or '"' in valor:
        valor = valor.replace('"', '\\"')
        return f'"{valor}"'
    return valor

# Uso
valor = preparar_valor("Bug Report")  # → "Bug Report"
valor = preparar_valor("test")        # → test
```

---

## ✅ PASSO 4: Validar Argumentos

Antes de executar, validar todos os parâmetros.

### Checklist de Validação

```python
def validar_comando(comando_tipo: str, itemtype: str, **kwargs) -> tuple[bool, str]:
    """
    Valida se comando pode ser executado
    Retorna: (válido: bool, mensagem_erro: str)
    """

    # 1. ItemType válido?
    itemtype_normalizado = normalizar_itemtype(itemtype)
    if not itemtype_normalizado:
        return False, f"ItemType '{itemtype}' inválido"

    # 2. Comando LIST
    if comando_tipo == "LIST":
        # Validar limit
        limit = kwargs.get("limit", 50)
        if not (1 <= int(limit) <= 1000):
            return False, "Limit deve estar entre 1 e 1000"

        # Validar start
        start = kwargs.get("start", 0)
        if not (int(start) >= 0):
            return False, "Start não pode ser negativo"

        return True, ""

    # 3. Comando GET
    elif comando_tipo == "GET":
        id_item = kwargs.get("id")
        if not validar_id(id_item):
            return False, f"ID '{id_item}' deve ser número positivo"

        return True, ""

    # 4. Comando SEARCH
    elif comando_tipo == "SEARCH":
        field_id = kwargs.get("field", "1")
        if not validar_field_id(field_id):
            return False, f"Field ID '{field_id}' inválido"

        valor = kwargs.get("value")
        if not valor:
            return False, "Value é obrigatório para search"

        return True, ""

    # 5. Comando FINGERPRINT
    elif comando_tipo == "FINGERPRINT":
        id_item = kwargs.get("id")
        if not validar_id(id_item):
            return False, f"ID '{id_item}' deve ser número positivo"

        return True, ""

    return False, f"Tipo de comando '{comando_tipo}' desconhecido"

# Uso
valido, erro = validar_comando("GET", "ticket", id="12345")
if not valido:
    print(f"Erro de validação: {erro}")
```

---

## 🏗️ PASSO 5: Construir Comando

Usar Command Reference (02-COMMAND-REFERENCE.md) para construir comando exato.

### 5.1 Construtor de Comando

```python
def construir_comando(comando_tipo: str, itemtype: str, **kwargs) -> str:
    """
    Constrói comando GLPI exato
    """

    itemtype = normalizar_itemtype(itemtype)

    # 1. LIST
    if comando_tipo == "LIST":
        cmd = f"glpi list {itemtype}"
        if "limit" in kwargs:
            cmd += f" --limit {kwargs['limit']}"
        if "start" in kwargs:
            cmd += f" --start {kwargs['start']}"
        if kwargs.get("json"):
            cmd += " --json"
        return cmd

    # 2. GET
    elif comando_tipo == "GET":
        cmd = f"glpi get {itemtype} {kwargs['id']}"
        if kwargs.get("json"):
            cmd += " --json"
        return cmd

    # 3. SEARCH
    elif comando_tipo == "SEARCH":
        field = kwargs.get("field", "1")
        valor = preparar_valor(kwargs["value"])
        searchtype = kwargs.get("searchtype", "contains")
        cmd = f"glpi search {itemtype} --field {field} --value {valor} --searchtype {searchtype}"
        if kwargs.get("json"):
            cmd += " --json"
        return cmd

    # 4. FINGERPRINT
    elif comando_tipo == "FINGERPRINT":
        cmd = f"glpi fingerprint {itemtype} {kwargs['id']}"
        if kwargs.get("json"):
            cmd += " --json"
        return cmd

    # 5. FINGERPRINT-SEARCH
    elif comando_tipo == "FINGERPRINT_SEARCH":
        valor = preparar_valor(kwargs["value"])
        cmd = f"glpi fingerprint-search {itemtype} --value {valor}"
        if kwargs.get("json"):
            cmd += " --json"
        return cmd

    # 6. INFO
    elif comando_tipo == "INFO":
        return "glpi info"

    return ""

# Uso
cmd = construir_comando("GET", "problem", id="12345")
# → "glpi get problem 12345"

cmd = construir_comando("SEARCH", "ticket", field="1", value="Bug", searchtype="contains", json=True)
# → "glpi search ticket --field 1 --value Bug --searchtype contains --json"
```

---

## 🚀 PASSO 6: Executar Comando

Executar comando no shell e capturar output.

### 6.1 Executor de Comando Seguro

```python
import subprocess
import shlex

def executar_comando_glpi(comando: str, timeout: int = 30) -> tuple[bool, str, str]:
    """
    Executa comando GLPI com segurança
    Retorna: (sucesso: bool, stdout: str, stderr: str)
    """

    try:
        # Usar shlex para fazer parse seguro
        args = shlex.split(comando)

        # Executar com timeout
        resultado = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        stdout = resultado.stdout.strip()
        stderr = resultado.stderr.strip()

        return True, stdout, stderr

    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT: Comando levou mais de 30 segundos"

    except FileNotFoundError:
        return False, "", "ERRO: Comando 'glpi' não encontrado. Instale GLPI CLI"

    except Exception as e:
        return False, "", f"ERRO na execução: {str(e)}"

# Uso
sucesso, stdout, stderr = executar_comando_glpi("glpi get problem 12345")
```

### 6.2 Exemplo de Execução Real

```bash
$ glpi get problem 12345

# Output esperado (sucesso):
┌─────────────────────┬──────────────────────────────────────┐
│ Field               │ Value                                │
├─────────────────────┼──────────────────────────────────────┤
│ ID                  │ 12345                                │
│ Name                │ Network Connectivity Issue           │
│ Status              │ Assigned                             │
└─────────────────────┴──────────────────────────────────────┘
```

---

## 📊 PASSO 7: Processar Output

Analisar resultado e determinar sucesso/erro.

### 7.1 Detector de Erro/Sucesso

```python
def processar_output(stdout: str, stderr: str) -> tuple[bool, dict]:
    """
    Processa output do comando
    Retorna: (sucesso: bool, dados: dict)
    """

    # 1. Verificar se há erro
    if stdout.startswith("✗"):
        mensagem_erro = stdout[2:].strip()
        return False, {"erro": mensagem_erro, "tipo": "GLPI_ERROR"}

    if stderr:
        return False, {"erro": stderr, "tipo": "SHELL_ERROR"}

    # 2. Verificar se está vazio (erro?)
    if not stdout or stdout == "[]":
        return True, {"dados": [], "vazio": True}

    # 3. Processar JSON
    if stdout.startswith("[") or stdout.startswith("{"):
        try:
            import json
            dados = json.loads(stdout)
            return True, {"dados": dados, "formato": "json"}
        except json.JSONDecodeError:
            return False, {"erro": "JSON inválido", "tipo": "JSON_ERROR"}

    # 4. Processar Tabela (retornar como está)
    return True, {"dados": stdout, "formato": "tabela"}

# Uso
sucesso, resultado = processar_output(stdout, stderr)
if not sucesso:
    print(f"Erro: {resultado['erro']}")
else:
    print(f"Dados: {resultado['dados']}")
```

### 7.2 Classificar Tipo de Erro

```python
def classificar_erro(mensagem_erro: str) -> str:
    """Classifica tipo de erro para resposta apropriada"""

    if "401" in mensagem_erro or "Token" in mensagem_erro or "não autenticado" in mensagem_erro:
        return "AUTENTICAÇÃO"
    elif "403" in mensagem_erro or "permissão" in mensagem_erro:
        return "PERMISSÃO"
    elif "404" in mensagem_erro or "não encontrado" in mensagem_erro:
        return "NÃO_ENCONTRADO"
    elif "400" in mensagem_erro or "inválido" in mensagem_erro:
        return "VALIDAÇÃO"
    elif "500" in mensagem_erro or "502" in mensagem_erro or "503" in mensagem_erro:
        return "SERVIDOR"
    elif "timeout" in mensagem_erro.lower() or "connection" in mensagem_erro.lower():
        return "CONEXÃO"
    else:
        return "DESCONHECIDO"

# Uso
tipo = classificar_erro("✗ Token inválido (401)")  # → "AUTENTICAÇÃO"
```

---

## 📝 PASSO 8: Formatar Resposta

Apresentar resultado de forma compreensível ao usuário.

### 8.1 Formatador de Resposta

```python
def formatar_resposta(sucesso: bool, dados: dict) -> str:
    """Formata resposta final para usuário"""

    if not sucesso:
        tipo_erro = classificar_erro(dados.get("erro", ""))
        mensagem = dados.get("erro", "Erro desconhecido")

        # Avisos contextualizados
        aviso_contexto = {
            "AUTENTICAÇÃO": "\n💡 Dica: Verifique se GLPI_URL, GLPI_APP_TOKEN e GLPI_USER_TOKEN estão configurados.",
            "PERMISSÃO": "\n💡 Dica: Você pode não ter permissão para este ItemType. Contate o admin.",
            "NÃO_ENCONTRADO": "\n💡 Dica: Use 'glpi list <tipo>' para encontrar IDs válidos.",
            "VALIDAÇÃO": "\n💡 Dica: Verifique a sintaxe do comando.",
            "SERVIDOR": "\n💡 Dica: O servidor pode estar indisponível. Tente novamente em alguns minutos.",
            "CONEXÃO": "\n💡 Dica: Verifique sua conexão de rede e se a URL do GLPI está acessível.",
        }

        resposta = f"❌ Erro [{tipo_erro}]: {mensagem}"
        resposta += aviso_contexto.get(tipo_erro, "")
        return resposta

    # Sucesso
    if dados.get("vazio"):
        return "✓ Nenhum resultado encontrado (normal)."

    if dados.get("formato") == "json":
        return f"✓ Sucesso (JSON):\n{dados['dados']}"

    if dados.get("formato") == "tabela":
        return f"✓ Sucesso:\n{dados['dados']}"

    return "✓ Sucesso! Operação realizada."

# Uso
resposta = formatar_resposta(False, {"erro": "Token inválido (401)"})
print(resposta)
# Saída:
# ❌ Erro [AUTENTICAÇÃO]: Token inválido (401)
# 💡 Dica: Verifique se GLPI_URL, GLPI_APP_TOKEN e GLPI_USER_TOKEN estão configurados.
```

---

## 🔄 Fluxo Completo: Exemplo "Get Problem 12345"

```
ENTRADA:
  "Get em problem do id 12345"

├─ PASSO 1: Receber ✓
│   └─ Entrada armazenada

├─ PASSO 2: Analisar Intenção
│   ├─ Extrair: ação="get", itemtype="problem", id="12345"
│   └─ Comando inferido: OBTER

├─ PASSO 3: Normalizar
│   ├─ itemtype: "problem" → "Problem" ✓
│   ├─ id: "12345" (número? sim ✓)
│   └─ formato: (não especificado = tabela)

├─ PASSO 4: Validar
│   ├─ ItemType "Problem" existe? ✓
│   ├─ ID "12345" é número positivo? ✓
│   └─ Validação passou ✓

├─ PASSO 5: Construir Comando
│   └─ "glpi get problem 12345"

├─ PASSO 6: Executar
│   └─ subprocess.run(["glpi", "get", "problem", "12345"])
│      ├─ stdout: "┌─────┬──────────┐\n│ ID  │ Name     │\n├─────┼──────────┤..."
│      └─ stderr: "" (vazio)

├─ PASSO 7: Processar Output
│   ├─ Contém "✗"? não
│   ├─ stderr vazio? sim
│   ├─ Formato: tabela
│   └─ Sucesso? SIM ✓

└─ PASSO 8: Formatar Resposta
    └─ "✓ Sucesso:\n┌─────┬──────────┐\n│ ID  │ Name     │..."

SAÍDA PARA USUÁRIO:
  ✓ Sucesso:
  ┌─────┬──────────────────────────────────┐
  │ ID  │ Name                             │
  ├─────┼──────────────────────────────────┤
  │ ... │ Network Connectivity Issue       │
  └─────┴──────────────────────────────────┘
```

---

## 🎯 Pseudocódigo Completo para LLM

```python
def processar_instrucao_glpi(instrucao_usuario: str) -> str:
    """
    Processa instrução de usuário e retorna resposta
    """

    # PASSO 2: Analisar
    tipo_comando = analisar_intencao(instrucao_usuario)
    itemtype_raw = extrair_itemtype(instrucao_usuario)
    args_raw = extrair_argumentos(instrucao_usuario)

    # PASSO 3: Normalizar
    itemtype = normalizar_itemtype(itemtype_raw)

    # PASSO 4: Validar
    valido, erro = validar_comando(tipo_comando, itemtype, **args_raw)
    if not valido:
        return f"❌ Erro de validação: {erro}"

    # PASSO 5: Construir
    comando = construir_comando(tipo_comando, itemtype, **args_raw)

    # PASSO 6: Executar
    sucesso_exec, stdout, stderr = executar_comando_glpi(comando)
    if not sucesso_exec:
        return f"❌ Erro na execução: {stderr}"

    # PASSO 7: Processar
    sucesso, dados = processar_output(stdout, stderr)

    # PASSO 8: Formatar
    resposta = formatar_resposta(sucesso, dados)

    return resposta

# Uso do LLM
resposta = processar_instrucao_glpi("Get em problem do id 12345")
print(resposta)
```

---

## 🚨 Tratamento de Casos Especiais

### Caso 1: Usuário quer JSON

```
Entrada: "Get problem 12345 em JSON"

Processamento:
  ├─ Analisar: json=True detectado
  └─ Construir: "glpi get problem 12345 --json"

Output:
  {
    "id": 12345,
    "name": "Network Issue",
    ...
  }
```

### Caso 2: Paginação Grande

```
Entrada: "Listar 500 tickets"

Processamento:
  ├─ limit=500 solicitado
  ├─ limit máximo=1000, então OK
  └─ Construir: "glpi list ticket --limit 500"
```

### Caso 3: Campo Desconhecido em Search

```
Entrada: "Buscar tickets por campo desconhecido com valor X"

Processamento:
  ├─ Field desconhecido, usar field=1 (name)
  ├─ Construir: "glpi search ticket --field 1 --value X"
  └─ Se user souber field ID: sugerir "glpi search ticket --field 123 --value X"
```

---

## 📚 Referência Rápida

| Passo | Função | Saída |
|-------|--------|-------|
| 1 | `receber_instrucao()` | instrucao_raw |
| 2 | `analisar_intencao()` | tipo_comando |
| 3 | `normalizar_entrada()` | itemtype, args normalized |
| 4 | `validar_comando()` | (válido: bool, erro: str) |
| 5 | `construir_comando()` | comando_str |
| 6 | `executar_comando_glpi()` | (sucesso, stdout, stderr) |
| 7 | `processar_output()` | (sucesso, dados) |
| 8 | `formatar_resposta()` | resposta_usuario |

---

## 🔗 Documentação Relacionada

- **01-DECISION-TREE.md** - Como escolher comando
- **02-COMMAND-REFERENCE.md** - Sintaxe de cada comando
- **03-EXAMPLES-REAL-WORLD.md** - Exemplos práticos
- **04-ERROR-HANDLING.md** - Tratamento de erros

---

## ✨ Dicas Finais para LLM

1. **Sempre validar antes de executar** - Previne erros desnecessários
2. **Tratamento de erro com contexto** - Não só informar erro, mas orientar usuário
3. **Sugerir alternativas** - Se algo falhar, propor plano B
4. **Usar JSON para integração** - Facilita processamento por máquinas
5. **Manter histórico** - Se múltiplas operações, rastrear estado
6. **Timeouts** - Sempre usar timeout em execução (padrão 30s)
7. **Escaping** - Sempre escapar aspas em valores de busca

---

## 🎓 Conclusão

Este guia fornece todos os passos para um LLM **executar com segurança e precisão** qualquer comando GLPI CLI.

Seguindo os 8 passos:
1. ✅ Receber instrução
2. ✅ Analisar intenção
3. ✅ Normalizar entrada
4. ✅ Validar argumentos
5. ✅ Construir comando
6. ✅ Executar comando
7. ✅ Processar output
8. ✅ Formatar resposta

**Resultado:** LLM consegue usar GLPI CLI no dia a dia sem dificuldades!

