# 1. O que é funçoes?
def nome_da_funcao(parametro):
    return parametro


# 3. Tipos de funçoes em Python

# a) Funçoes integradas (built-in functions)

print("a) Funçoes integradas (built-in functions)")
len("Python")
print(len("Python"))

# print
# len
# type
# int, float, str, list, dict, tuple, set
# range
# sum
# max, min

# 2. Lambda functions

soma = lambda x, y: x + y  # noqa: E731
print(soma(2, 3))

numeros = [1, 2, 3, 4, 5]
quadrados = list(map(lambda x: x**2, numeros))
print(quadrados)

# Higher-order functions
# map
# filter
# reduce
# sorted


# Map exemplo
def dobrar(x):
    return x * 2


numeros = [1, 2, 3, 4, 5]
dobrados = list(map(dobrar, numeros))
print(dobrados)
# Usando lambda
dobrados = list(map(lambda x: x * 2, numeros))


# Exemplo de filter
def eh_par(x):
    return x % 2 == 0


numeros = [1, 2, 3, 4, 5]
pares = list(filter(eh_par, numeros))
print(pares)  # Output: [2, 4]

# Usando lambda
pares = list(filter(lambda x: x % 2 == 0, numeros))

# Exemplo de reduce
from functools import reduce

numeros = [1, 2, 3, 4, 5]
total = reduce(soma, numeros)
print(total)  # Output: 15

# Usando lambda
total = reduce(lambda x, y: x + y, numeros)
print(total)  # Output: 15


# Funçoes que retornam funçoes
def criar_multiplicador(x):
    def multiplicar(y):
        return x * y

    return multiplicar


dobrar = criar_multiplicador(2)
triplicar = criar_multiplicador(3)

print(dobrar(5))  # Output: 10
print(triplicar(5))  # Output: 15


# Exemplo pratico
numeros_dobrados = list(map(dobrar, numeros))
print(numeros_dobrados)

numeros_pares = list(filter(eh_par, numeros))
print(numeros_pares)

soma_total = reduce(soma, numeros)
print(soma_total)

resultado = reduce(soma, filter(eh_par, map(dobrar, numeros)))
print("Soma dos numeros pares e dobrados: ", resultado)
