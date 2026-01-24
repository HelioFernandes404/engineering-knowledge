# %%
import numpy as np

print(f"NumPy version: {np.__version__}")

# %%
m = np.array([[10, 20, 30], 
              [40, 50, 60]])

# fatia = m[1:].copy()  # linha
# print(fatia)
# %%

linha_0 = m[1]
linha_1 = m[0:1]
print(linha_0)
print(linha_1)
# %%
