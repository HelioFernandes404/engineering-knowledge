# GLPI CLI

Command-line interface para debug e interação com a API REST do GLPI.

## Características

- Interface de linha de comando simples e intuitiva
- Suporte para GET em todos os ItemTypes do GLPI
- Suporte para campos customizados via Plugin Fields (fingerprint)
- Saída formatada em tabela ou JSON
- Gerenciamento automático de sessões
- Tradução de erros para PT-BR
- Conversão automática de ItemTypes (case-insensitive)

## Instalação

### Via pipx (recomendado)

Instalar direto do GitHub:

```bash
# Última versão (main branch)
pipx install git+https://github.com/HelioFernandes404/glpi_cli.git

# Versão específica (tag/release)
pipx install git+https://github.com/HelioFernandes404/glpi_cli.git@1.0.0
```

### Via pip

```bash
# Do GitHub
pip install git+https://github.com/HelioFernandes404/glpi_cli.git

# Local
pip install .
```

### Modo desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/HelioFernandes404/glpi_cli.git
cd glpi_cli

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale em modo editable
pip install -e ".[dev]"
```

## Configuração

### Opção 1: Variáveis de ambiente (prioridade)

```bash
export GLPI_URL="https://itsm.systemframe.com.br/apirest.php"
export GLPI_APP_TOKEN="seu_app_token"
export GLPI_USER_TOKEN="seu_user_token"
```

Ou crie um arquivo `.env`:

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### Opção 2: Arquivo de configuração

Crie `~/.config/glpi/config.yml`:

```yaml
url: https://itsm.systemframe.com.br/apirest.php
app_token: seu_app_token
user_token: seu_user_token
```

**Nota:** Variáveis de ambiente têm prioridade sobre o arquivo de configuração.

## Uso

### Comandos disponíveis

```bash
glpi --help              # Ajuda geral
glpi info                # Mostra configuração e ItemTypes disponíveis
glpi list <itemtype>     # Lista items
glpi get <itemtype> <id> # Obtém item específico
glpi search <itemtype>   # Busca items com critérios
```

### Exemplos

#### Listar tickets

```bash
# Formato tabela (padrão)
glpi list ticket

# Formato JSON
glpi list ticket --json

# Com paginação
glpi list ticket --limit 100 --start 0
```

#### Obter item específico

```bash
# Formato tabela
glpi get ticket 123

# Formato JSON completo
glpi get computer 42 --json

# Qualquer ItemType
glpi get entity 5
```

#### Buscar items

```bash
# Busca por nome (field 1)
glpi search ticket --value "servidor"

# Busca em campo específico
glpi search computer --field 1 --value "srv-web"

# Resultado em JSON
glpi search entity --value "TI" --json
```

#### Obter fingerprint de um item (Plugin Fields)

```bash
# Obter fingerprint de um Problem específico
glpi fingerprint problem 123

# Formato JSON
glpi fingerprint ticket 42 --json
```

#### Listar todos os fingerprints de um tipo de item

```bash
# Listar todos os fingerprints de Problems
glpi fingerprints problem

# Com paginação
glpi fingerprints ticket --limit 100 --start 0

# Formato JSON
glpi fingerprints problem --json
```

#### Buscar items por valor de fingerprint

```bash
# Buscar por valor de fingerprint
glpi fingerprint-search problem --value "abc123xyz"

# Formato JSON
glpi fingerprint-search ticket --value "hash-value" --json
```

#### Ver informações

```bash
glpi info
```

### ItemTypes suportados

O CLI converte automaticamente para o formato correto (PascalCase):

```bash
# Todas essas formas funcionam:
glpi list ticket
glpi list TICKET
glpi list Ticket
```

ItemTypes comuns:
- **Assets:** Computer, Monitor, Printer, NetworkEquipment, Software
- **Helpdesk:** Ticket, Problem, Change, ITILCategory
- **Management:** User, Group, Entity, Location, Supplier, Contract
- **Network:** NetworkPort, IPAddress, VLAN

Execute `glpi info` para ver lista completa.

## Estrutura do Projeto

```
glpi_cli/
├── glpi_cli/
│   ├── __init__.py
│   ├── cli.py           # Entry point e comandos
│   ├── config.py        # Gerenciamento de configuração
│   ├── client.py        # Cliente HTTP da API GLPI
│   ├── errors.py        # Tratamento e tradução de erros
│   ├── formatters.py    # Formatadores de saída (table/json)
│   └── utils.py         # Utilitários (normalização de ItemType)
├── tests/               # Testes
├── pyproject.toml       # Configuração do projeto
├── README.md
└── .env.example
```

## Desenvolvimento

### Instalar dependências de desenvolvimento

```bash
pip install -e ".[dev]"
```

### Executar testes

```bash
pytest
pytest --cov=glpi_cli
```

### Formatação de código

```bash
black glpi_cli/
```

### Linting

```bash
flake8 glpi_cli/
mypy glpi_cli/
```

## Troubleshooting

### Erro: "Configuração inválida"

Verifique se as variáveis de ambiente ou arquivo de configuração estão corretos:

```bash
glpi info
```

### Erro: "ERROR_GLPI_LOGIN_USER_TOKEN"

Seu user_token está inválido ou sem permissões. Verifique em:
GLPI > Configurar > API > Usuários

### Erro: "ERROR_ITEM_NOT_FOUND"

O item com o ID especificado não existe ou você não tem permissão para acessá-lo.

### Erro: "ERROR_ITEMTYPE_NOT_FOUND"

O ItemType especificado não existe. Execute `glpi info` para ver os tipos disponíveis.

## Licença

MIT
