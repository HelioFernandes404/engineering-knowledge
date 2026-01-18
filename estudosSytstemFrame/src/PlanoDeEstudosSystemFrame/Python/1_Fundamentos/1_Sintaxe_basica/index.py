# Revisar a sintaxe básica do Python: variáveis, operadores aritméticos e lógicos.


# 1. Variáveis em Python
x: int = 5  # Inteiro
pi: float = 3.14  # Ponto flutuante
nome: str = "João"  # String
is_valid: bool = True  # Booleano
convidados: list[str] = ["Helio", "Fernandes"]  # Lista
tupla: tuple[int, int] = (1, 2)  # Tupla (imutável)
dicionario_vazio: dict[str, int] = {"João": 1, "Ronaldo": 2}  # Dicionário (mutável)
variavel: None = None  # None

# 2. Operadores Aritméticos
a = 10
b = 3

soma = a + b  # 13
subtracao = a - b  # 7
multiplicacao = a * b  # 30
divisao = a / b  # 3.333....
divisao_inteiro = a // b  # 3
resto = a % b  # 1
potencia = a ** b  # 1000

# 3. Operadores Lógicos
x = 5
y = 10

# and
resultado_and = (x > 2 and y < 15)  # True

# or
resultado_or = (x > 10 and y > 15)  # False

# not
resultado_not = not (x > 10)  # True

# 4. Estruturas Condicionais
idade = 18

if idade < 18:
    print("Menor de idade")
elif idade == 18:
    print("Recém maior de idade")
else:
    print("Maior de idade")


# 5. Funções em Python
def saudacao(nome: str) -> str:
    """
    Retorna uma saudação personalizada para o nome fornecido.

    :param nome: O nome da pessoa.
    :return: Uma string com a saudação.
    """
    return f"Olá, {nome}!"


print(saudacao("João"))

# 6. Loop (Estruturas de Repetição)
# Exemplo de loop `for`
for convidado in convidados:
    print(f"Olá ,{convidado}")

# Exemplo de Loop
contador = 0
while contador < 10:
    print(f"{contador}")
    contador += 1 # Incrementando o contador

# 7. Tratamento de Exceções
try:
    # Tentando acessar uma chave inexistente
    print(dicionario_vazio["João"])
except KeyError as e:
    print(f"Erro: A chave {e} não existe no dicionário.")
