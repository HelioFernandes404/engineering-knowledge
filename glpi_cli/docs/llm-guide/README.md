# GLPI CLI - LLM Guide Completo

Documentação estruturada para ensinar **LLMs (Large Language Models)** a usar a CLI GLPI de forma autônoma e precisa.

---

## 📚 Índice de Documentação

### 1. **01-DECISION-TREE.md** 🌳
**Aprenda como escolher o comando certo**

- Fluxograma de decisão visual
- Mapeamento de intenções → comandos
- ItemTypes disponíveis
- Ordem de prioridade de busca
- Exemplos de análise

**Quando usar:** Primeira coisa que um LLM deve ler para entender qual comando escolher.

---

### 2. **02-COMMAND-REFERENCE.md** 📖
**Referência completa de sintaxe de cada comando**

- Sintaxe exata de cada comando
- Argumentos obrigatórios vs opcionais
- Descrição detalhada de cada flag
- Exemplos de uso
- Saídas esperadas (sucesso e erro)

**Quando usar:** Ao construir o comando exato. Consulte para sintaxe precisa.

---

### 3. **03-EXAMPLES-REAL-WORLD.md** 💡
**Exemplos práticos do dia a dia**

- 10 exemplos reais completos
- Passo-a-passo de análise LLM
- Comandos executados
- Saídas esperadas
- Fluxos com múltiplas operações
- Tratamento de erros com contexto

**Quando usar:** Para entender padrões reais e ver fluxos completos.

---

### 4. **04-ERROR-HANDLING.md** ⚠️
**Guia de tratamento e tradução de erros**

- 6 categorias de erros
- Cada erro tem: causa, solução, exemplo
- Matriz de decisão para responder ao usuário
- Template de tratamento de erro para LLM
- Checklist de debugging

**Quando usar:** Quando erro ocorre, para entender o que fazer.

---

### 5. **05-EXECUTION-GUIDE.md** 🚀
**Guia prático step-by-step de execução**

- 8 passos do ciclo de vida de execução
- Pseudocódigo implementável
- Funções prontas para adaptar
- Fluxo completo com exemplo real
- Casos especiais

**Quando usar:** Implementar execução real em código do LLM.

---

## 🎯 Fluxo Recomendado para LLM

```
NOVO LLM LENDO DOCUMENTAÇÃO?
  ├─ Ler: 01-DECISION-TREE.md
  │  └─ Entender "qual comando" para cada intenção
  │
  ├─ Ler: 02-COMMAND-REFERENCE.md
  │  └─ Entender sintaxe exata de cada comando
  │
  └─ Ler: 03-EXAMPLES-REAL-WORLD.md
     └─ Ver exemplos práticos

DURANTE EXECUÇÃO?
  ├─ Usar: 05-EXECUTION-GUIDE.md
  │  └─ Seguir 8 passos para executar com segurança
  │
  └─ Se erro: 04-ERROR-HANDLING.md
     └─ Entender erro e responder apropriadamente
```

---

## 📊 Matriz Rápida: Intenção → Comando

| Intenção | Comando | Exemplo |
|----------|---------|---------|
| Listar todos os items | `glpi list <tipo>` | `glpi list ticket` |
| Obter um item por ID | `glpi get <tipo> <id>` | `glpi get problem 12345` |
| Buscar por critério | `glpi search <tipo> --field N --value V` | `glpi search ticket --field 1 --value "bug"` |
| Obter fingerprint | `glpi fingerprint <tipo> <id>` | `glpi fingerprint computer 5` |
| Listar fingerprints | `glpi fingerprints <tipo>` | `glpi fingerprints computer` |
| Buscar por fingerprint | `glpi fingerprint-search <tipo> --value V` | `glpi fingerprint-search computer --value "ABC123"` |
| Info do sistema | `glpi info` | `glpi info` |

---

## 🔑 Conceitos-Chave que LLM Deve Entender

### 1. ItemType (Tipo de Recurso)
```
Computer, Ticket, Problem, User, Monitor, Network, etc.
Sempre normalizar para PascalCase: "ticket" → "Ticket"
```

### 2. Operações CRUD Básicas
```
C: Não suportado (CLI é read-only)
R: list, get, search ← Principais
U: Não suportado
D: Não suportado
```

### 3. Paginação
```
--limit N    : Quantidade máxima de items (padrão: 50, máx: 1000)
--start N    : Índice inicial (padrão: 0)

Exemplo:
  Items 1-50:    glpi list ticket --limit 50 --start 0
  Items 51-100:  glpi list ticket --limit 50 --start 50
  Items 101-150: glpi list ticket --limit 50 --start 100
```

### 4. Formato de Saída
```
--json     : Retorna JSON (máquina lê)
(padrão)   : Retorna tabela formatada (humano lê)
```

### 5. Search com Critérios
```
--field N      : ID do campo (padrão: 1 = name)
--value V      : Valor a buscar
--searchtype T : Tipo de busca (padrão: contains)
               Opções: contains, equals, under
```

---

## 🛠️ Implementação Recomendada para LLM

Se você é um LLM ou IA implementando isso, aqui está a estrutura sugerida:

```python
class GLPICLIExecutor:
    """Executor de comandos GLPI CLI para LLM"""

    def __init__(self):
        self.itemtypes = self.load_itemtypes()
        self.session = None

    def processar_instrucao(self, instrucao: str) -> str:
        """
        Processa instrução em linguagem natural e retorna resultado
        """
        try:
            # Passo 1-2: Analisar
            tipo_cmd = self.decision_tree(instrucao)

            # Passo 3-4: Validar
            if not self.validar(tipo_cmd):
                return f"❌ Erro de validação"

            # Passo 5: Construir
            cmd = self.construir_comando(tipo_cmd)

            # Passo 6: Executar
            resultado = self.executar(cmd)

            # Passo 7-8: Processar e Formatar
            return self.formatar_resposta(resultado)

        except Exception as e:
            return self.tratador_de_erros(e)

    def decision_tree(self, instrucao: str) -> dict:
        """Implementar: 01-DECISION-TREE.md"""
        pass

    def validar(self, comando: dict) -> bool:
        """Implementar: 05-EXECUTION-GUIDE.md Passo 4"""
        pass

    def construir_comando(self, comando: dict) -> str:
        """Implementar: 02-COMMAND-REFERENCE.md"""
        pass

    def executar(self, comando: str) -> tuple[bool, str]:
        """Implementar: 05-EXECUTION-GUIDE.md Passo 6"""
        pass

    def tratador_de_erros(self, erro) -> str:
        """Implementar: 04-ERROR-HANDLING.md"""
        pass
```

---

## ✅ Checklist: O que um LLM Precisa Saber

- [ ] Qual é o propósito da CLI? (Debug/query da API GLPI)
- [ ] Quais são os 7 comandos disponíveis? (list, get, search, fingerprint, fingerprints, fingerprint-search, info)
- [ ] Como normalizar ItemType? (to PascalCase)
- [ ] Como validar ID? (deve ser número positivo)
- [ ] Como construir comando search? (--field --value)
- [ ] Qual é o máximo de items em uma query? (1000)
- [ ] Como processar JSON vs tabela? (--json flag)
- [ ] Qual é o padrão de erro? (começa com "✗")
- [ ] Quais são as 6 categorias de erro? (auth, permission, not_found, validation, connection, server)
- [ ] Como fazer paginação? (--limit N --start M)

---

## 🚀 Exemplo Prático: "Get em problem do id xxxx"

Seguindo essa documentação, aqui está como LLM processaria:

```
ENTRADA: "Get em problem do id xxxx"

PASSO 1-2 (Decision Tree):
  Intenção = GET
  ItemType = problem
  ID = xxxx (após normalizar para "xxxx" ou número)

PASSO 3 (Normalizar):
  ItemType: "problem" → "Problem" ✓
  ID: "xxxx" → (se número: válido ✓, se texto: erro)

PASSO 4 (Validar):
  - ItemType "Problem" existe? ✓
  - ID é número? Depende do input
  - OK para executar? Sim (se ID for número)

PASSO 5 (Construir):
  Comando = "glpi get problem xxxx"
  (assumindo xxxx é número válido)

PASSO 6 (Executar):
  $ glpi get problem xxxx
  [tabela com detalhes do problema]

PASSO 7 (Processar):
  Sucesso? ✓
  Formato? Tabela
  Dados? [detalhes do problema]

PASSO 8 (Formatar):
  ✓ Sucesso:
  [exibir tabela ao usuário]
```

---

## 🔗 Arquivos Relacionados

```
/docs/llm-guide/
├── README.md (este arquivo)
├── 01-DECISION-TREE.md
├── 02-COMMAND-REFERENCE.md
├── 03-EXAMPLES-REAL-WORLD.md
├── 04-ERROR-HANDLING.md
└── 05-EXECUTION-GUIDE.md
```

---

## 📝 Notas Importantes

1. **Sempre validar antes de executar** - Segurança primeiro
2. **Timeouts são críticos** - Não execute indefinidamente
3. **Tratar erros com contexto** - Não só informar, mas orientar
4. **Manter compatibilidade** - Alguns campos variam por ItemType
5. **JSON para integração** - Máquinas entendem melhor JSON
6. **Tabela para humanos** - Formatação visual é importante

---

## 🎓 Conclusão

Esta documentação fornece tudo que um **LLM ou IA** precisa para:

✅ Entender a intenção do usuário
✅ Escolher o comando certo
✅ Construir comando com precisão
✅ Executar com segurança
✅ Processar resultado corretamente
✅ Responder apropriadamente
✅ Tratar erros e orientar usuário

**Resultado:** LLM consegue usar GLPI CLI **de forma autônoma e confiável** no dia a dia!

---

## 📞 Suporte

Se encontrar algo não documentado:
1. Verificar `glpi --help`
2. Verificar `glpi <comando> --help`
3. Consultar 04-ERROR-HANDLING.md para tratamento de erro
4. Contatar admin GLPI para dúvidas sobre ItemTypes/Fields

---

**Versão:** 1.0
**Data:** 2025-10-30
**CLI Versão Alvo:** 1.0.0
**Último Atualizado:** 2025-10-30

