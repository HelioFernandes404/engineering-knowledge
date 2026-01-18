Segue uma demo mais “real” (projeto com pacote em `src/`, testes, lint e notebook/`#%%`) usando **uv + .venv por projeto + kernel Jupyter**, pronta para abrir no Cursor. [docs.astral](https://docs.astral.sh/uv/guides/projects/)

## Estrutura do projeto
A proposta é ter código reaproveitável em `src/`, testes em `tests/` e exploração em `notebooks/` (ou arquivo `.py` com `# %%`), para não “virar só notebook”.  
O uv cobre o ciclo de projeto (dependências, lock e sincronização do ambiente) via `uv add`, `uv lock`, `uv sync` e `uv run`. [docs.astral](https://docs.astral.sh/uv/concepts/projects/sync/)

## Criar projeto e dependências
Crie o projeto hipotético `sales-forecast` (pode trocar o nome): [docs.astral](https://docs.astral.sh/uv/guides/projects/)
```bash
mkdir sales-forecast
cd sales-forecast
uv init
```

Adicione dependências “de projeto” e “de dev” (isso atualiza `pyproject.toml`/lock e mantém a `.venv` do projeto em dia). [docs.astral](https://docs.astral.sh/uv/guides/projects/)
```bash
uv add pandas numpy scikit-learn matplotlib
uv add --dev ipykernel pytest ruff
```

Dica prática: quando quiser garantir que o editor está 100% alinhado com o lockfile, rode `uv sync` (ele faz sync “exato” por padrão, removendo pacotes fora do lock). [docs.astral](https://docs.astral.sh/uv/concepts/projects/sync/)

## Código + testes (pacote real)
Crie as pastas e um módulo simples:  
```bash
mkdir -p src/sales_forecast tests notebooks
touch src/sales_forecast/__init__.py
```

Crie `src/sales_forecast/features.py`:
```python
import pandas as pd

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_x_ads"] = df["price"] * df["ads_spend"]
    return df
```

Crie `tests/test_features.py`:
```python
import pandas as pd
from sales_forecast.features import make_features

def test_make_features_adds_column():
    df = pd.DataFrame({"price": [10.0], "ads_spend": [2.0]})
    out = make_features(df)
    assert out["price_x_ads"].iloc[0] == 20.0
```

Rode lint e testes pelo uv (mantém tudo no ambiente do projeto e evita “python errado”). [docs.astral](https://docs.astral.sh/uv/guides/projects/)
```bash
uv run ruff check .
uv run pytest -q
```

## Kernel + JupyterLab (no .venv do projeto)
Registre um kernel do projeto apontando para a `.venv` local (mude o `--name` se quiser): [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)
```bash
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=sales-forecast
```

Suba o JupyterLab sem “poluir” o venv do projeto, usando o modo `--with jupyter` (o kernel é que garante a execução no seu `.venv`). [docs.astral](https://docs.astral.sh/uv/guides/integration/jupyter/)
```bash
uv run --with jupyter jupyter lab
```

## Mini demo no notebook (EDA + modelo)
Crie um notebook em `notebooks/01_baseline.ipynb` (ou um `notebooks/01_baseline.py` com `# %%`) e selecione o kernel `sales-forecast`. [docs.cursor](https://docs.cursor.com/en/guides/advanced/datascience)
No notebook, rode algo assim (dataset sintético, mas fluxo real: features → split → treino → métrica):

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from sales_forecast.features import make_features

rng = np.random.default_rng(7)

n = 500
df = pd.DataFrame({
    "price": rng.uniform(10, 100, size=n),
    "ads_spend": rng.uniform(0, 50, size=n),
})

# target com ruído: vendas aumentam com ads e caem com preço
df["sales"] = 200 - 1.5*df["price"] + 3.2*df["ads_spend"] + rng.normal(0, 10, size=n)

X = make_features(df)[["price", "ads_spend", "price_x_ads"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
mae
```

No Cursor, instale a extensão Jupyter (`ms-toolsai.jupyter`) para ter suporte completo a `.ipynb` e também execução por células em `.py` com `# %%` no mesmo estilo. [docs.cursor](https://docs.cursor.com/en/guides/advanced/datascience)
