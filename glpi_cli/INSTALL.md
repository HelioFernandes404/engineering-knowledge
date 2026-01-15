# Guia de Instalação - GLPI CLI

Documentação completa para instalar o GLPI CLI em diferentes ambientes.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação via pipx (Recomendado)](#instalação-via-pipx-recomendado)
- [Instalação via pip](#instalação-via-pip)
- [Instalação para Desenvolvimento](#instalação-para-desenvolvimento)
- [Configuração](#configuração)
- [Verificação da Instalação](#verificação-da-instalação)
- [Atualização](#atualização)
- [Desinstalação](#desinstalação)
- [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

- **Python 3.8 ou superior**
- **pip** ou **pipx** instalado
- **Git** (para instalação do GitHub)
- Acesso a uma instância GLPI com API REST habilitada
- Tokens de autenticação (App Token e User Token)

### Verificar versão do Python

```bash
python3 --version
# Deve mostrar: Python 3.8.x ou superior
```

### Instalar pipx (se ainda não tiver)

**Linux/Mac:**
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

**Arch Linux:**
```bash
sudo pacman -S python-pipx
```

**Ubuntu/Debian:**
```bash
sudo apt install pipx
pipx ensurepath
```

**macOS (Homebrew):**
```bash
brew install pipx
pipx ensurepath
```

Depois de instalar, **feche e abra o terminal novamente**.

---

## Instalação via pipx (Recomendado)

pipx instala o CLI em um ambiente isolado e o disponibiliza globalmente.

### 1. Instalar a última versão estável

```bash
pipx install git+https://github.com/HelioFernandes404/glpi_cli.git@v1.0.0
```

### 2. Instalar a versão em desenvolvimento (main branch)

```bash
pipx install git+https://github.com/HelioFernandes404/glpi_cli.git
```

### 3. Verificar instalação

```bash
glpi --version
# Deve mostrar: glpi, version 1.0.0
```

---

## Instalação via pip

### Método 1: Diretamente do GitHub

```bash
pip install git+https://github.com/HelioFernandes404/glpi_cli.git@v1.0.0
```

### Método 2: Clonar e instalar localmente

```bash
# Clone o repositório
git clone https://github.com/HelioFernandes404/glpi_cli.git
cd glpi_cli

# Instale
pip install .
```

### Método 3: Em um ambiente virtual (recomendado com pip)

```bash
# Crie ambiente virtual
python3 -m venv glpi-env

# Ative o ambiente
source glpi-env/bin/activate  # Linux/Mac
# ou
glpi-env\Scripts\activate  # Windows

# Instale o GLPI CLI
pip install git+https://github.com/HelioFernandes404/glpi_cli.git@v1.0.0

# Use o comando
glpi --version
```

---

## Instalação para Desenvolvimento

Para contribuir ou modificar o código:

### 1. Clone o repositório

```bash
git clone https://github.com/HelioFernandes404/glpi_cli.git
cd glpi_cli
```

### 2. Crie ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale em modo editable com dependências de desenvolvimento

```bash
pip install -e ".[dev]"
```

Agora qualquer mudança no código será refletida imediatamente no comando `glpi`.

### 4. Execute testes (quando disponíveis)

```bash
pytest
pytest --cov=glpi_cli  # Com cobertura
```

---

## Configuração

Após instalar, você precisa configurar as credenciais do GLPI.

### Opção 1: Variáveis de Ambiente (Recomendado)

**Linux/Mac:**

```bash
# Adicione ao seu ~/.bashrc ou ~/.zshrc
export GLPI_URL="https://seu-glpi.com.br/apirest.php"
export GLPI_APP_TOKEN="seu_app_token_aqui"
export GLPI_USER_TOKEN="seu_user_token_aqui"

# Recarregue o shell
source ~/.bashrc  # ou source ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# Adicione ao seu perfil do PowerShell
$env:GLPI_URL="https://seu-glpi.com.br/apirest.php"
$env:GLPI_APP_TOKEN="seu_app_token_aqui"
$env:GLPI_USER_TOKEN="seu_user_token_aqui"
```

### Opção 2: Arquivo de Configuração

Crie o arquivo `~/.config/glpi/config.yml`:

```bash
# Linux/Mac
mkdir -p ~/.config/glpi
nano ~/.config/glpi/config.yml
```

Adicione o conteúdo:

```yaml
url: https://seu-glpi.com.br/apirest.php
app_token: seu_app_token_aqui
user_token: seu_user_token_aqui
```

### Opção 3: Arquivo .env (Temporário)

Crie um arquivo `.env` no diretório onde você vai executar o comando:

```bash
cp .env.example .env
nano .env
```

Edite com suas credenciais:

```env
GLPI_URL=https://seu-glpi.com.br/apirest.php
GLPI_APP_TOKEN=seu_app_token_aqui
GLPI_USER_TOKEN=seu_user_token_aqui
```

### Como obter os tokens no GLPI

1. **App Token:**
   - Acesse GLPI como administrador
   - Vá em: **Configurar > Geral > API**
   - Na aba **Clientes API**, adicione um novo cliente
   - Copie o **App Token** gerado

2. **User Token:**
   - Acesse GLPI com seu usuário
   - Vá em: **Meu Perfil > Configurações Remotas**
   - Clique em **Gerar** ou copie o token existente

---

## Verificação da Instalação

### 1. Verificar versão

```bash
glpi --version
```

### 2. Verificar configuração

```bash
glpi info
```

Deve mostrar:

```
ℹ Configuração GLPI CLI

URL: https://seu-glpi.com.br/apirest.php
App Token: ✓ configurado
User Token: ✓ configurado

✔ Configuração válida!

==================================================
ItemTypes comuns disponíveis:
==================================================
   1. Budget
   2. Change
   3. Computer
   ...
```

### 3. Testar comando básico

```bash
glpi list entity --limit 5
```

Se tudo estiver correto, você verá uma tabela com as entidades do GLPI.

---

## Atualização

### Com pipx

```bash
# Atualizar para última versão
pipx upgrade glpi-cli

# Ou reinstalar versão específica
pipx uninstall glpi-cli
pipx install git+https://github.com/HelioFernandes404/glpi_cli.git@v1.0.0
```

### Com pip

```bash
pip install --upgrade git+https://github.com/HelioFernandes404/glpi_cli.git
```

### Em ambiente de desenvolvimento

```bash
cd glpi_cli
git pull origin main
pip install -e ".[dev]"
```

---

## Desinstalação

### Com pipx

```bash
pipx uninstall glpi-cli
```

### Com pip

```bash
pip uninstall glpi-cli
```

### Remover configurações

```bash
# Linux/Mac
rm -rf ~/.config/glpi
rm -f .env

# Remover do bashrc/zshrc as variáveis GLPI_*
```

---

## Troubleshooting

### Erro: `command not found: glpi`

**Causa:** O PATH não está configurado corretamente.

**Solução:**
```bash
# Verifique se pipx está no PATH
echo $PATH

# Execute novamente
pipx ensurepath

# Feche e abra o terminal
```

### Erro: `Configuração inválida: GLPI_URL não configurado`

**Causa:** Variáveis de ambiente não configuradas.

**Solução:**
```bash
# Verifique as variáveis
echo $GLPI_URL
echo $GLPI_APP_TOKEN
echo $GLPI_USER_TOKEN

# Configure conforme a seção "Configuração"
```

### Erro: `ERROR_GLPI_LOGIN_USER_TOKEN`

**Causa:** User Token inválido ou sem permissões.

**Solução:**
- Verifique se o token está correto
- Regenere o token no GLPI (Meu Perfil > Configurações Remotas)
- Verifique se a API está habilitada para seu usuário

### Erro: `ERROR_WRONG_APP_TOKEN_PARAMETER`

**Causa:** App Token e User Token trocados.

**Solução:**
- **GLPI_APP_TOKEN** deve ser o token do "Cliente API"
- **GLPI_USER_TOKEN** deve ser o token do "Usuário"
- Verifique se não inverteu os tokens

### Erro: `ERROR_ITEM_NOT_FOUND`

**Causa:** Item não existe ou sem permissão.

**Solução:**
- Verifique se o ID existe: `glpi list <itemtype>`
- Verifique suas permissões no GLPI

### Python 3.7 ou inferior

**Causa:** GLPI CLI requer Python 3.8+

**Solução:**
```bash
# Atualize o Python
sudo apt update && sudo apt install python3.11  # Ubuntu/Debian
```

### Problemas de encoding (caracteres estranhos)

**Causa:** Encoding do terminal não UTF-8.

**Solução:**
```bash
# Linux/Mac
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8

# Adicione ao ~/.bashrc para permanente
```

---

## Suporte

- **Issues:** https://github.com/HelioFernandes404/glpi_cli/issues
- **Documentação:** https://github.com/HelioFernandes404/glpi_cli#readme
- **Releases:** https://github.com/HelioFernandes404/glpi_cli/releases

---

## Próximos Passos

Agora que você instalou o GLPI CLI com sucesso, confira:

- [README.md](README.md) - Documentação completa de uso
- [Exemplos de comandos](README.md#exemplos)
- [Lista de ItemTypes suportados](README.md#itemtypes-suportados)
