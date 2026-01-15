def squares(n):
    for i in range(n):
        yield i ** 2


for square in squares(5):
    print(square)

# Output: 0 1 4 9 16


# Expressao geradora que retorna numeros quadrados de um inteiros de 0 a 4
squares = (i ** 2 for i in range(5))


# Expressões geradoras vs compreensões de lista

# https://www.pythontutorial.net/advanced-python/python-generator-expressions/
