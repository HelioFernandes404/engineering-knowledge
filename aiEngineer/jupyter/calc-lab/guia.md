Beleza — abaixo vai um “mini-demo” completo (projeto hipotético) com **nomes diferentes** e comandos na ordem certa, do zero até rodar no Jupyter e no Cursor usando `.venv` por projeto. [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)

## Demo: `calc-lab`
### Criar projeto e venv (uv)
```bash
mkdir calc-lab
cd calc-lab

uv init
# (opcional) ver o esqueleto criado
ls
```
O `uv init` cria o `pyproject.toml` e um esqueleto de app (incluindo `main.py`). [docs.astral](https://docs.astral.sh/uv/guides/projects/)

Agora rode algo para o uv criar/usar a `.venv` do projeto:
```bash
uv run main.py
```
A lógica do “rodar via uv” é o fluxo padrão de projetos, e é isso que materializa o ambiente por projeto quando necessário. [docs.astral](https://docs.astral.sh/uv/guides/projects/)

### Criar uma “calculadora” com células (arquivo .py)
Crie um arquivo `calculator.py` (ou renomeie como quiser) com este conteúdo:

```python
# %% [markdown]
# # Calc Lab
# Mini demo: funções + execução por células

# %%
def add(a: float, b: float) -> float:
    return a + b

def sub(a: float, b: float) -> float:
    return a - b

def mul(a: float, b: float) -> float:
    return a * b

def div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b não pode ser 0")
    return a / b

# %%
add(2, 3), sub(10, 4), mul(6, 7), div(20, 5)
```

Esse formato com `# %%` permite trabalhar “célula por célula” em arquivo `.py` usando a extensão Jupyter (mesma experiência do notebook, só que mais amigável para Git e refactor). [kirill-markin](https://kirill-markin.com/articles/jupyter-notebooks-cursor-ide-llm-ai-tutorial/)

Rode pelo terminal:
```bash
uv run calculator.py
```
Rodar scripts com `uv run` é o fluxo de projetos recomendado pelo uv. [docs.astral](https://docs.astral.sh/uv/guides/projects/)

## Jupyter (kernel do projeto)
### Adicionar ipykernel ao `.venv` do projeto
```bash
uv add --dev ipykernel
```
O próprio guia do uv recomenda `ipykernel` como dev dependency para criar um kernel dedicado do projeto. [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)

### Registrar o kernel apontando para a `.venv` local
```bash
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=calc-lab
```
Esse comando instala um kernelspec que “amarra” o notebook ao ambiente do projeto (sua `.venv`). [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)

### Subir o JupyterLab (como tool isolada)
```bash
uv run --with jupyter jupyter lab
```
O uv descreve esse modo como uma forma de rodar o Jupyter em um ambiente isolado, mas com notebooks executando no kernel do projeto. [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)

No browser/JupyterLab:
- Crie um notebook Python.
- Selecione o kernel **calc-lab**.
- Teste:
  ```python
  import sys
  sys.executable
  ```
  e confirme que aponta para `.../calc-lab/.venv/bin/python...` (como você já validou no seu caso). [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)

## Cursor (usando a `.venv` local)
- Instale a extensão Jupyter (`ms-toolsai.jupyter`) no Cursor para habilitar `.ipynb` e execução por células em `.py`. [docs.cursor](https://docs.cursor.com/en/guides/advanced/datascience)
- Abra a pasta `calc-lab` no Cursor e:
  - Se estiver no `.ipynb`, selecione o kernel `calc-lab`. [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)
  - Se estiver no `calculator.py` com `# %%`, execute célula por célula com os botões/ações do Jupyter na IDE. [kirill-markin](https://kirill-markin.com/articles/jupyter-notebooks-cursor-ide-llm-ai-tutorial/)

Se quiser, dá para adaptar essa demo para um projeto “real” com dependências (ex.: `uv add numpy pandas`) e um notebook com pequenos testes/benchmarks, mantendo exatamente o mesmo padrão de kernel por projeto. [docs.astral](https://docs.astral.sh/uv/guides/projects/)
