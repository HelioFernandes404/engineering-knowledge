
# %%
import numpy as np
print(f"NumPy version: {np.__version__}")

# %%
temperatura = [10, 20, 30, 40 ,50]

celsius = np.array(temperatura)

fahrenheit = np.array(( celsius * 9/5 + 32))

print(fahrenheit)

# %%
