# CLAUDE.md

Este arquivo orienta Claude Code ao trabalhar neste repositório.

## O QUÊ (Tecnologia e Estrutura)

**Stack**: Python 3.x CLI tool
**Dependências principais**:
- `questionary` - Interface interativa do CLI
- `webbrowser` - Abertura automática de URLs

**Estrutura do projeto** (`linkedin_helper/`):
- `cli.py` - Interface do usuário (menus, prompts, orquestração dos fluxos)
- `url_builder.py` - Lógica de construção de URLs do LinkedIn
- `constants.py` - Mapeamentos de parâmetros da API do LinkedIn

## POR QUE (Propósito)

LinkedIn Query Helper gera URLs de busca do LinkedIn com filtros avançados. Usuários selecionam opções em um menu interativo e o tool constrói URLs otimizadas para:
- Busca de vagas (job search) com filtros de workplace type, experiência, Easy Apply, etc.
- Busca de conteúdo/posts (content search) com enriquecimento automático de termos

## COMO (Desenvolvimento)

### Setup
```bash
# Criar e ativar ambiente virtual
python -m venv .venvkeep
source .venvkeep/bin/activate  # Linux/macOS

# Instalar em modo editável
pip install -e .
```

### Executar
```bash
linkedin-helper              # CLI interativo
python -m linkedin_helper.cli  # Ou direto
```

### Verificar mudanças
```bash
# Testar fluxo completo
linkedin-helper

# Verificar imports e sintaxe
python -m py_compile linkedin_helper/*.py
```

## Contexto Adicional

Para detalhes específicos sobre:
- **Parâmetros da API do LinkedIn**: Veja `linkedin_helper/constants.py` (mapeamentos autoritativos)
- **Lógica de construção de URLs**: Veja funções em `linkedin_helper/url_builder.py`

**Importante**: Os mapeamentos em `constants.py` são a fonte autoritativa. Não duplique valores - sempre referencie o arquivo original.

## Convenções do Projeto

- **Estilo**: Código existente segue convenções Python padrão (PEP 8)
- **Estrutura de funções**: Funções `collect_*_data()` em `cli.py` retornam dicionários de parâmetros
- **Construção de URLs**: Funções `build_*_url()` em `url_builder.py` recebem dicionários e retornam URLs formatadas
