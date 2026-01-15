# Adicionando Elementos em uma Lista
lista: list = [1, 2, 3]

# Adicionando no final
lista.append(6)

# Adicionando em uma posição específica
lista.insert(2, 'Novo valor')

# Adicionando Pares Chave-Valor em um Dicionário
dicionario: dict[str, str] = {'Chave': "Valor"} # iniciado a varaivel
dicionario.update({
    "endereco": "Rua Fictícia, 123",
    "idade": 30
})

# Adicionando Elementos em um Conjunto
conjunto: set = {1, 2, 3, 4, 5}
conjunto.add(6)

# Adicionando Elementos a uma Tupla
tupla: tuple = (1, 2, 3)
tupla = tupla + (6,)  # Saída: (6,)
tupla = tupla + (6)  # Saída: <class 'int'>

# 4. Operações de Remoção de Dados
# Remove o primeiro item com valor 3
lista.remove(3)

# Remove e retorna o último item
ultimo = lista.pop()

# Remove um item em um índice específico
del list[2]

# Removendo Pares Chave-Valor de um Dicionário
# o método pop() permite remover um item com base na chave.
dicionario.pop("idade")

# Removendo Elementos de um Conjunto
conjunto.remove(3)
# ou
conjunto.discard(3)

# Tentando Remover Elementos de uma Tupla
# Como as tuplas são imutáveis, não é possível remover diretamente seus elementos. Se você precisar "remover" um item, terá que criar uma nova tupla.
tupla = tupla[:2] + tupla[3:]

# Operações de Alteração de Dados
# Alterando Elementos em uma Lista
lista[0] = "Novo valor"

# Alterando Valores em um Dicionário
dicionario["nome"] = "Maria"

# 6. Operações de Busca de Dados
# Buscando Elementos em uma Lista
if 3 in lista: print("O Valor 3 está na lista!")

# Buscando Valores em um Dicionário
nome = dicionario.get("nome")

# Buscando Elementos em um Conjunto
if 3 in conjunto: print("O valor 3 está no conjunto")

# 7. Operações de Ordenação de Dados
# Ordenando Listas
lista.sort()  # Ordena em ordem crescente

# Ordenando Dicionários
sorted(dicionario.items())  # Ordena por chave

# Ordenando Conjuntos
sorted(conjunto)

# Ordenando tupla
tupla = (5, 3, 8, 1, 2)

# Passo 1: Converter a tupla em lista
lista = lista(tupla)

# Passo 2: Ordenar a lista
lista.sort()

# Passo 3: Converter a lista de volta para tupla
tupla_ordenada = sorted(tupla)

# Exibindo o resultado
print("Tupla ordenada:", tupla_ordenada)
# Tupla ordenada: (1, 2, 3, 5, 8)