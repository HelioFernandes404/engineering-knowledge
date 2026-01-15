# LinkedIn Query Helper - CLI

Interactive command-line tool for building LinkedIn search URLs with advanced filters.

## Features

- 🔍 Search LinkedIn jobs and content
- 🎯 Filter by technology, seniority, workplace type
- 📅 Filter by date posted
- ⚡ Easy Apply filter
- 🚫 Exclude keywords from search
- 🌐 Automatically opens search in browser
- 💻 Pure Python - no Node.js required

## Setup

### Prerequisites
- Python 3.8+

### Installation

```bash
# Create virtual environment (using venvkeep)
python -m venv .venvkeep
source .venvkeep/bin/activate  # Linux/macOS
# or
.venvkeep\Scripts\activate  # Windows

# Install in editable mode
pip install -e .
```

## Usage

Simply run the command:

```bash
linkedin-helper
```

The interactive menu will guide you through:
1. Choose search type (Jobs or Content)
2. Enter technology/keywords
3. Optionally exclude keywords
4. For jobs: select filters (workplace type, seniority, date, Easy Apply)
5. Enter page number
6. URL opens automatically in your browser

### Example Flow

```
==================================================
🔎  LinkedIn Query Helper
==================================================

? Buscar em: Vagas

🔎 LinkedIn Query Helper - Busca de Vagas

? Tecnologia/palavra-chave: React
? Excluir palavras-chave: estágio, júnior
? Modalidade de trabalho: Remoto
? Senioridade: Senior
? Publicada há: Última semana
? Apenas Easy Apply? Yes
? Página de pesquisa: 1

==================================================
✅ URL gerada com sucesso!
==================================================

https://www.linkedin.com/jobs/search/?keywords=React&f_AL=true&f_WT=2&f_TPR=r604800

🌐 Abrindo no navegador...
```

## Project Structure

```
linkedin-query-helper/
├── linkedin_helper/
│   ├── __init__.py
│   ├── cli.py           # Interactive menu (main entry point)
│   ├── url_builder.py   # LinkedIn URL construction logic
│   └── constants.py     # LinkedIn parameter mappings
├── requirements.txt
├── setup.py
└── README.md
```

## Architecture

- **Pure Python**: No JavaScript/Node.js dependencies
- **Interactive CLI**: Uses `questionary` for beautiful TUI
- **URL Building**: Recreates all React app logic in Python
- **Browser Integration**: Uses stdlib `webbrowser` module
