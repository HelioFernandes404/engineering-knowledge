# Minibudget 💰

Um sistema de orçamento pessoal focado em simplicidade, alta densidade de informação e experiência de uso desktop-first. Construído com Python e Flask, seguindo uma filosofia de **Server-Side Rendering (SSR)** e design minimalista inspirado em `shadcn/ui`.

## 🚀 Tecnologias

- **Backend:** Python 3.12+ com Flask
- **Banco de Dados:** SQLite (SQL puro)
- **Frontend:** Jinja2 (Componentizado), CSS Moderno (Variáveis, Grid, Flexbox), JS Mínimo
- **Gerenciamento de Pacotes:** [uv](https://github.com/astral-sh/uv)
- **Testes:** Pytest

## ✨ Funcionalidades Atuais

### 1. Dashboard Inteligente
- **Navegação Temporal:** Seletor de meses para análise de histórico e planejamento futuro.
- **Hero Stats:** Visualização clara de saldo restante, total gasto e progresso do orçamento.
- **Breakdown por Categoria:** Gráfico de barras simplificado mostrando a distribuição dos gastos.
- **Transações Recentes:** Acesso rápido aos últimos 5 lançamentos do mês selecionado.

### 2. Gestão de Despesas (CRUD Completo)
- **Lançamento Rápido:** Formulário otimizado para entrada de dados via teclado.
- **Edição Inline:** Corrija erros de lançamento sem precisar deletar e recriar.
- **Histórico Denso:** Tabela compacta com paginação visual natural e ações rápidas.
- **Localização PT-BR:** Formatação automática de moeda (R$) e datas (dd/mm/aaaa).

### 3. Preferências e Ajustes
- **Orçamento Dinâmico:** Defina sua meta mensal e o sistema recalcula todos os dashboards instantaneamente.
- **Persistência:** Configurações armazenadas de forma segura no SQLite.

## 🏗️ Estrutura do Projeto

```text
Minibudget/
├── app.py              # Rotas, lógica de negócio e filtros Jinja
├── db.py               # Gerenciamento de conexão e helpers SQL
├── schema.sql          # Definição das tabelas do banco
├── static/
│   ├── css/style.css   # Design System (CSS Variables + Component styles)
│   └── js/script.js    # Micro-interações
├── templates/
│   ├── layouts/        # Base HTML e estrutura comum
│   ├── components/     # Macros Jinja (Inputs, Cards, Icons)
│   ├── dashboard.html  # Página principal
│   └── expenses.html   # Gestão de lançamentos
└── tests/              # Suite de testes automatizados
```

## 🛠️ Comandos Úteis

### Iniciar o servidor
```bash
uv run python app.py
```

### Rodar testes
```bash
uv run pytest
```

### Formatar código
```bash
uv run ruff format .
```

## 🎯 Filosofia de Design
- **Desktop-First:** Interface otimizada para produtividade em telas grandes.
- **Informação Densa:** Menos espaço em branco inútil, mais dados visíveis.
- **Sem Frameworks JS:** UI rica usando apenas CSS moderno e transições nativas.
- **Pragmatismo:** SQL direto para máxima performance e simplicidade arquitetural.
