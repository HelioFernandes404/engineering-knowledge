# GitHub Repository Batch Clone Tool

Script bash para clonar todos os repositórios de uma organização ou usuário do GitHub de forma paralela e eficiente.

## Requisitos

- [GitHub CLI (gh)](https://cli.github.com/) instalado e autenticado
- `git` instalado
- `jq` para processamento JSON

### Instalação dos Requisitos

```bash
# GitHub CLI
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Arch Linux
sudo pacman -S github-cli

# Autenticar
gh auth login

# jq (processador JSON)
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq

# Arch Linux
sudo pacman -S jq
```

## Uso

### Sintaxe Básica

```bash
./clone_repos.sh [OPÇÕES] <org-ou-usuário>
```

### Exemplos

```bash
# Clonar todos os repos de uma organização
./clone_repos.sh systemframe

# Clonar com 4 jobs paralelos e limite de 500 repos
./clone_repos.sh -p 4 -l 500 myorg

# Clonar para diretório específico usando HTTPS
./clone_repos.sh -d ~/projetos/minhaorg -m https minhaorg

# Clonar apenas repos públicos, excluindo forks
./clone_repos.sh --public-only --no-forks meuusuario

# Filtrar repos por padrão no nome
./clone_repos.sh -f "backend" myorg

# Clonar repos privados para um diretório específico
./clone_repos.sh --private-only -d ~/work/private-repos myorg
```

## Opções Disponíveis

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `-l, --limit <número>` | Número máximo de repos a buscar | 1000 |
| `-p, --parallel <número>` | Número de clones paralelos | 8 |
| `-d, --directory <caminho>` | Diretório destino para clonagem | Diretório atual |
| `-m, --method <ssh\|https>` | Método de clone: ssh ou https | ssh |
| `-f, --filter <padrão>` | Filtrar repos por nome (padrão grep) | - |
| `--public-only` | Clonar apenas repositórios públicos | - |
| `--private-only` | Clonar apenas repositórios privados | - |
| `--archived` | Incluir repositórios arquivados | - |
| `--no-forks` | Excluir repositórios que são forks | - |
| `-h, --help` | Mostrar mensagem de ajuda | - |

## Funcionalidades

✅ **Clone em paralelo** - Acelera o processo usando múltiplos workers
✅ **Suporte SSH e HTTPS** - Escolha o método de autenticação
✅ **Filtros avançados** - Por visibilidade, forks, arquivados e nome
✅ **Skip inteligente** - Pula repositórios já clonados
✅ **Output colorido** - Interface visual clara
✅ **Validação de requisitos** - Verifica gh CLI e autenticação
✅ **Gestão de erros** - Continua mesmo se um clone falhar

## Como Funciona

1. Verifica se o GitHub CLI está instalado e autenticado
2. Busca a lista de repositórios usando a API do GitHub
3. Aplica os filtros especificados (visibilidade, forks, nome, etc.)
4. Clona os repositórios em paralelo usando `xargs`
5. Pula repositórios que já existem no diretório destino
6. Exibe um resumo ao final

## Casos de Uso

### Backup de Organização

```bash
# Fazer backup completo de todos os repos da org
./clone_repos.sh -d ~/backups/myorg myorg
```

### Desenvolvimento Local

```bash
# Clonar apenas repos ativos (não arquivados) para desenvolvimento
./clone_repos.sh -d ~/dev/projects --no-forks myorg
```

### Auditoria de Código

```bash
# Clonar apenas repos públicos para auditoria
./clone_repos.sh --public-only -d ~/audit/public-repos organization
```

### Migração

```bash
# Clonar todos os repos incluindo arquivados para migração
./clone_repos.sh --archived -d ~/migration/all-repos oldorg
```

## Troubleshooting

### Erro: "gh: command not found"

Instale o GitHub CLI seguindo as instruções em https://cli.github.com/

### Erro: "not authenticated"

Execute `gh auth login` para autenticar o GitHub CLI

### Erro: "jq: command not found"

Instale o jq usando seu gerenciador de pacotes (apt, brew, pacman, etc.)

### Clone muito lento

Reduza o número de jobs paralelos: `./clone_repos.sh -p 2 myorg`

### Problemas com SSH

Use HTTPS como método de clone: `./clone_repos.sh -m https myorg`

## Scripts Adicionais

Este repositório também contém outros scripts úteis:

- `install__k9s.sh` - Instalador do K9s (Kubernetes CLI)
- `tunnel__k9s.sh` - Script para configurar túnel e abrir K9s

## Contribuindo

Sinta-se livre para abrir issues ou pull requests com melhorias!

## Licença

MIT
