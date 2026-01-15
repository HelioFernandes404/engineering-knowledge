# GLPI CLI - Error Handling para LLMs

Guia completo de tratamento e tradução de erros que LLMs podem encontrar.

---

## 🚨 Padrão de Detecção de Erro

Todos os erros da CLI começam com `✗`:

```
✗ [MENSAGEM DO ERRO]
```

### Padrão de Detecção
```python
def tem_erro(output: str) -> bool:
    """LLM deve verificar se há erro na saída"""
    return output.startswith("✗") or "ERROR" in output

def extrair_mensagem_erro(output: str) -> str:
    """Extrair apenas a mensagem"""
    if output.startswith("✗"):
        return output[2:].strip()  # Remove "✗ "
    return output
```

---

## 🔐 CATEGORIA 1: Erros de Autenticação

Ocorrem quando credenciais estão faltando, inválidas ou expiradas.

### Erro: "Token de aplicação inválido"
```
Saída: ✗ Erro ao iniciar sessão: Token inválido (401)
HTTP Status: 401 Unauthorized

Causas:
  ├─ GLPI_APP_TOKEN está vazio
  ├─ GLPI_APP_TOKEN está incorreto/expirado
  ├─ Variável de ambiente não foi carregada
  └─ Arquivo ~/.config/glpi/config.yml tem valor errado

Solução LLM:
  1. Verificar se variável está definida:
     echo $GLPI_APP_TOKEN
  2. Se vazia, pedir ao usuário para configurar:
     export GLPI_APP_TOKEN="seu_token_aqui"
  3. Testar novamente com: glpi info
```

### Erro: "Token de usuário inválido"
```
Saída: ✗ Erro ao iniciar sessão: User Token inválido (401)
HTTP Status: 401 Unauthorized

Causas:
  ├─ GLPI_USER_TOKEN está vazio ou incorreto
  ├─ Usuário foi desativado no GLPI
  ├─ Token expirou (tokens podem ter TTL)
  └─ Credenciais no config.yml estão erradas

Solução LLM:
  1. Verificar usuário configurado:
     grep "user_token" ~/.config/glpi/config.yml
  2. Pedir novo token ao admin GLPI
  3. Atualizar config ou variável de ambiente
  4. Testar: glpi info
```

### Erro: "Não autenticado"
```
Saída: ✗ Não autenticado (401)
HTTP Status: 401 Unauthorized

Causas:
  └─ Nenhuma credencial foi configurada

Solução LLM:
  1. Guiar usuário para configurar credenciais
  2. Opção A - Variáveis de Ambiente:
     export GLPI_URL="https://glpi.example.com/apirest.php"
     export GLPI_APP_TOKEN="seu_app_token"
     export GLPI_USER_TOKEN="seu_user_token"
  3. Opção B - Arquivo de Config:
     mkdir -p ~/.config/glpi
     cat > ~/.config/glpi/config.yml << EOF
     url: https://glpi.example.com/apirest.php
     app_token: seu_app_token
     user_token: seu_user_token
     EOF
  4. Testar com: glpi info
```

---

## 🚫 CATEGORIA 2: Erros de Permissão

Ocorrem quando o usuário não tem acesso ao recurso.

### Erro: "Sem permissão para acessar"
```
Saída: ✗ Sem permissão para acessar 'computer' (403)
HTTP Status: 403 Forbidden

Causas:
  ├─ Usuário não tem permissão para ItemType
  ├─ Perfil de usuário é restrito
  ├─ Item foi marcado como privado
  └─ Grupo de usuário não tem acesso

Solução LLM:
  1. Informar ao usuário que está bloqueado
  2. Tentar com ItemType diferente
  3. Contatar admin GLPI para elevar permissões
  4. Verificar perfil: glpi info (mostra ItemTypes acessíveis)
```

### Erro: "Direitos insuficientes"
```
Saída: ✗ Direitos insuficientes para esta operação (403)
HTTP Status: 403 Forbidden

Causas:
  └─ Operação específica requer permissão maior

Solução LLM:
  1. Verificar permissões no perfil de usuário
  2. Contatar administrador GLPI
  3. Tentar operação de leitura em vez de escrita
```

---

## 🔍 CATEGORIA 3: Erros de Recurso Não Encontrado

Ocorrem quando item ou tipo não existe.

### Erro: "ItemType não encontrado"
```
Saída: ✗ ItemType 'xyz' não é válido
Causa: Usuário digitou um ItemType que não existe

Solução LLM:
  1. Listar ItemTypes válidos
  2. Sugerir alternativas similares:
     "Você quis dizer: Computer, Ticket, Problem?"
  3. Usar: glpi info (para ver todos)

ItemTypes Válidos:
  Computer, Monitor, Printer, NetworkEquipment, Peripheral, Phone,
  Software, SoftwareLicense, SoftwareVersion, Ticket, TicketFollowup,
  TicketTask, TicketValidation, ITILCategory, Problem, Change, Solution,
  SolutionTemplate, User, Group, Entity, Profile, Location, Supplier,
  Contact, Contract, Budget, Document, DocumentType, KnowbaseItem,
  Network, NetworkPort, NetworkName, IPAddress, IPNetwork, FQDN, Vlan,
  Project, ProjectTask, Reminder, RSSFeed, Reservation, Log, Event,
  CronTask, Config, Plugin
```

### Erro: "Item com ID não encontrado"
```
Saída: ✗ Item 'ticket' com ID '99999' não encontrado (404)
HTTP Status: 404 Not Found

Causas:
  ├─ ID não existe no banco de dados
  ├─ ID foi deletado
  ├─ Usuário não tem permissão para ver este item
  └─ ID digitado incorretamente

Solução LLM:
  1. Verificar ID digitado está correto
  2. Listar items para encontrar ID correto:
     glpi list ticket --limit 20
  3. Buscar por nome se souber:
     glpi search ticket --field 1 --value "nome_do_ticket"
  4. Se foi deletado, informar ao usuário
```

---

## ❌ CATEGORIA 4: Erros de Validação de Entrada

Ocorrem quando argumentos/flags estão inválidos.

### Erro: "ID deve ser um número"
```
Saída: ✗ ID deve ser um número inteiro positivo
Causa: Usuário passou ID que não é número

Exemplo:
  glpi get ticket abc    ← ERRO: "abc" não é número
  glpi get ticket 123    ← OK

Solução LLM:
  1. Validar antes de executar se ID é número
  2. Se não for, pedir ID correto ou buscar por nome
  3. Sugerir: glpi search ticket --field 1 --value "nome"
```

### Erro: "Field ID inválido"
```
Saída: ✗ Field '999' não existe para ItemType 'ticket'
Causa: Field ID não corresponde a nenhum campo neste ItemType

Solução LLM:
  1. Tentar descobrir field ID correto
  2. Usar glpi get para ver estrutura:
     glpi get ticket 1 --json
  3. Procurar pelo nome do campo na estrutura
  4. Se ainda assim não funcionar, usar field 1 (name)
```

### Erro: "Valor inválido"
```
Saída: ✗ Valor inválido para este campo
Causa: Valor fornecido não corresponde ao tipo de campo

Solução LLM:
  1. Verificar tipo de campo (texto, número, select, etc)
  2. Reformatar valor se necessário
  3. Usar aspas se contém espaços:
     glpi search ticket --field 1 --value "Bug Report"
  4. Tentar com --searchtype contains em vez de equals
```

### Erro: "Limite inválido"
```
Saída: ✗ Limite deve estar entre 1 e 1000
Causa: Valor de --limit está fora do range

Exemplos de ERRO:
  glpi list ticket --limit 0      ← 0 é inválido
  glpi list ticket --limit 2000   ← 2000 é > 1000
  glpi list ticket --limit abc    ← não é número

Solução LLM:
  1. Sempre validar: 1 <= limit <= 1000
  2. Usar padrão (50) se não especificado
  3. Para listas grandes, usar paginação:
     glpi list ticket --start 0 --limit 500
     glpi list ticket --start 500 --limit 500
     glpi list ticket --start 1000 --limit 500
```

---

## 🌐 CATEGORIA 5: Erros de Conexão/Servidor

Ocorrem quando não consegue conectar ao servidor GLPI.

### Erro: "URL inválida ou servidor inacessível"
```
Saída: ✗ Erro de conexão: Não foi possível conectar ao servidor GLPI
HTTP Status: Connection Error

Causas:
  ├─ GLPI_URL está vazio ou inválido
  ├─ Servidor GLPI está offline
  ├─ Problema de rede/firewall
  ├─ URL tem erro de digitação
  └─ Certificado SSL inválido (HTTPS)

Solução LLM:
  1. Verificar se URL está configurada:
     echo $GLPI_URL
  2. Testar conectividade:
     curl -I https://glpi.example.com/apirest.php
  3. Verificar se servidor está UP:
     Contatar admin GLPI ou provider
  4. Se firewall, desbloquear em:
     https://glpi.example.com:443 (HTTPS)
```

### Erro: "Timeout na conexão"
```
Saída: ✗ Timeout: Servidor não respondeu em tempo hábil
HTTP Status: Timeout

Causas:
  ├─ Servidor GLPI está lento
  ├─ Rede congestionada
  ├─ Query muito pesada (muitos items)
  └─ Servidor offline/crash

Solução LLM:
  1. Tentar novamente (pode ser falha temporária)
  2. Reduzir scope da busca:
     glpi list ticket --limit 10  (menos items)
     glpi search ticket --field 1 --value "algo" (mais específico)
  3. Se persistir, contatar admin GLPI
  4. Verificar com: curl -I https://glpi.example.com/apirest.php
```

### Erro: "SSL Certificate Error"
```
Saída: ✗ Erro SSL: Certificado inválido ou self-signed
HTTP Status: SSL Error

Causas:
  ├─ Certificado GLPI expirou
  ├─ Certificado self-signed (não confiável)
  ├─ Problema de data/hora do sistema
  └─ Certificado intermediário faltando

Solução LLM:
  1. Se GLPI tem certificado self-signed, avisar usuário
  2. Não ignorar SSL em produção (inseguro)
  3. Contatar admin GLPI para corrigir certificado
  4. Verificar data/hora do sistema:
     date  (deve estar sincronizado com servidor)
```

---

## 📋 CATEGORIA 6: Erros de API GLPI

Erros retornados pela API do GLPI (status 4xx/5xx).

### Erro: "Requisição malformada"
```
Saída: ✗ Requisição inválida: Parâmetros malformados (400)
HTTP Status: 400 Bad Request

Causas:
  ├─ JSON malformado (se POST/PUT)
  ├─ Parâmetro obrigatório faltando
  ├─ Tipo de parâmetro incorreto
  └─ URL mal formatada

Solução LLM:
  1. Verificar sintaxe do comando
  2. Verificar se todos argumentos obrigatórios estão
  3. Usar exemplos da referência: 02-COMMAND-REFERENCE.md
  4. Debug com: --json flag para ver resposta completa
```

### Erro: "Erro interno do servidor"
```
Saída: ✗ Erro interno do servidor GLPI (500)
HTTP Status: 500 Internal Server Error

Causas:
  ├─ Bug no GLPI
  ├─ Problema no banco de dados
  ├─ Plugin com erro
  └─ Sobrecarga do servidor

Solução LLM:
  1. Tentar novamente (pode ser falha temporária)
  2. Verificar logs do GLPI (contatar admin)
  3. Reduzir carga se muitas requisições
  4. Contatar suporte GLPI se persistir
```

### Erro: "Gateway indisponível"
```
Saída: ✗ Gateway indisponível (502/503)
HTTP Status: 502 Bad Gateway ou 503 Service Unavailable

Causas:
  ├─ Servidor GLPI está reiniciando
  ├─ Load balancer tem problema
  ├─ Manutenção programada
  └─ Servidor sobrecarregado

Solução LLM:
  1. Esperar alguns minutos
  2. Tentar novamente
  3. Verificar status.glpi.com ou status page
  4. Contatar admin para informação
```

---

## 🔄 MATRIZ DE DECISÃO: Como LLM Deve Responder

```
Erro? ──┬─ NÃO ──→ Processar resultado com sucesso
        │
        └─ SIM ──┬─ Começa com "✗" ?
                 │
                 ├─ "autenticação" / "401" / "Token"
                 │  └─ → Avisar sobre credenciais
                 │       Sugerir reconfiguração
                 │
                 ├─ "permissão" / "403" / "direitos"
                 │  └─ → Avisar que acesso está bloqueado
                 │       Contatar admin
                 │
                 ├─ "não encontrado" / "404"
                 │  └─ → Verificar ID/valor
                 │       Sugerir busca por nome
                 │       Listar items válidos
                 │
                 ├─ "inválido" / "400"
                 │  └─ → Mostrar sintaxe correta
                 │       Validar argumentos
                 │       Sugerir exemplo
                 │
                 ├─ "conexão" / "timeout" / "ssl"
                 │  └─ → Testar conectividade
                 │       Informar servidor pode estar down
                 │       Contatar admin
                 │
                 └─ "500" / "502" / "503"
                    └─ → Informar erro no servidor
                         Sugerir tentar mais tarde
                         Contatar support
```

---

## 🎯 Template de Tratamento de Erro para LLM

```python
def executar_comando_glpi(comando: str) -> tuple[bool, str]:
    """
    Executa comando GLPI e retorna (sucesso, mensagem)
    """
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = resultado.stdout.strip()
        stderr = resultado.stderr.strip()

        # Verificar se há erro
        if stdout.startswith("✗"):
            mensagem_erro = stdout[2:].strip()

            # Classificar tipo de erro
            if "401" in mensagem_erro or "Token" in mensagem_erro:
                tipo = "AUTENTICAÇÃO"
            elif "403" in mensagem_erro or "permissão" in mensagem_erro:
                tipo = "PERMISSÃO"
            elif "404" in mensagem_erro or "não encontrado" in mensagem_erro:
                tipo = "NÃO_ENCONTRADO"
            elif "400" in mensagem_erro or "inválido" in mensagem_erro:
                tipo = "VALIDAÇÃO"
            elif "500" in mensagem_erro or "502" in mensagem_erro:
                tipo = "SERVIDOR"
            else:
                tipo = "DESCONHECIDO"

            return False, f"[{tipo}] {mensagem_erro}"

        # Sem erro, retornar resultado
        return True, stdout

    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT] Comando levou muito tempo"

    except Exception as e:
        return False, f"[ERRO_EXECUÇÃO] {str(e)}"

# Uso
sucesso, resultado = executar_comando_glpi("glpi get problem 12345")
if sucesso:
    print("Sucesso:", resultado)
else:
    print("Erro:", resultado)
```

---

## ✅ Checklist de Debugging para LLM

Quando encontrar erro, seguir essa ordem:

```
[ ] 1. Erro começa com "✗"? (padrão de erro)
[ ] 2. Qual categoria de erro? (auth, permission, not found, etc)
[ ] 3. Verificar comando foi digitado correto?
[ ] 4. Argumentos obrigatórios estão presentes?
[ ] 5. Tipos de dados estão corretos? (ID = número, etc)
[ ] 6. ItemType é válido? (usar: glpi info)
[ ] 7. Credenciais estão configuradas? (echo $GLPI_URL)
[ ] 8. Servidor está acessível? (curl GLPI_URL)
[ ] 9. Usuário tem permissão? (tentar outro ItemType)
[ ] 10. Se ainda não funciona, informar ao usuário:
    - Comando que foi executado
    - Mensagem de erro completa
    - Passos de ação recomendados
```

---

## 🔗 Próximo Passo

Ver: **05-EXECUTION-GUIDE.md** para guia completo de execução
