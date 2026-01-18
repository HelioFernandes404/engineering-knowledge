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
