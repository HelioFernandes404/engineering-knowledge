# How to Use Python Lambda Functions


# Lambda Calculus
# History
# First Example
def identity(x):
    return x


## In contrast, the lambda equivalent is:
identity = lambda x: x
# Output: x

# slightly more elaborate example
lambda x: x + 1
(lambda x: x + 1)(2)
# Output: 3

# Reduction
(lambda x: x + 1)(2)  # Evaluates to 3
# Step-by-step reduction:
# (lambda x: x + 1)(2)
# = (2 + 1)
# = 3

# Rename lambda
add_one = lambda x: x + 1
add_one(2)  # Output: 3


# Multiple Arguments
full_name = lambda first, last: f"Full name: {first.title()} {last.title()}"
print(full_name("guido", "van rossum"))  # Output: Full name: Guido Van Rossum

# Anonymous Functions
# Output: 3

# iffy in Python
(lambda x, y: x + y)(2, 3)  # Output: 5

# Higher-Order Functions lambda
high_ord_func = lambda x, func: x + func(x)
high_ord_func(2, lambda x: x * x)  # Output: 6
high_ord_func(2, lambda x: x + 3)  # Output: 7

# Python Lambda and Regular Functions
# https://realpython.com/python-lambda/#python-lambda-and-regular-functions TODO: continue from here
lambda x: x + 1

# Functions
import dis

add = lambda x, y: x + y
type(add)  # Output: <class 'function'>

dis.dis(add)

add  # <function <lambda> at 0x7f30c6ce9ea0>

# Traceback
div_zero = lambda x: x / 0
div_zero(2)
# ZeroDivisionError: division by zero

# Syntax

# função lambda não aceita intruçoes como
# return, pass, assert, or raise
# SyntaxError: invalid syntax

## Expresão unica
(lambda x: x % 2 and "odd" or "even")(3)  # Output: 'odd'

## Anotações de tipo

# função lambda equivalente é gerada em tempo de execução:

## IIFE

# geralmente preferido para casos simples ou temporários

# Arguments

# Argumentos posicionais
# Argumentos nomeados (às vezes chamados de argumentos de palavra-chave)
# Lista variável de argumentos (frequentemente chamada de varargs )
# Lista variável de argumentos de palavras-chave
# Argumentos somente de palavras-chave

(lambda x, y, z: x + y + z)(1, 2, 3)  # Output: 6
(lambda x, y, z=3: x + y + z)(1, 2)  # Output: 6
(lambda x, y, z=3: x + y + z)(1, y=2)  # Output: 6
(lambda *args: sum(args))(1, 2, 3)  # Output: 6
(lambda **kwargs: sum(kwargs.values()))(one=1, two=2, three=3)  # Output: 6
(lambda x, *, y=0, z=0: x + y + z)(1, y=2, z=3)  # Output: 6


# Decorators
def some_decorator(f):
    def wraps(*args, **kwargs):
        print("Calling function")
        return f(*args, **kwargs)

    return wraps


@some_decorator
def decorated_function(x):
    return x + 1


# Closure
def outer_func(x):
    def inner_func(y):
        return x + y

    return inner_func


for i in range(3):
    closure = outer_func(i)
    print(closure(i + 1))  # Output: 1, 3, 5


# Evaluation Time
def wrap(x):
    print("wrap()")
    return x


numbers = ["one", "two", "three"]

funcs = []

for n in numbers:
    funcs.append(lambda: wrap(n))

for f in funcs:
    print(f())
# Output: three, three, three


# Testing Lambdas


# Lambda Expression Abuses
# Raising an Exception
# Cryptic Style
# Python Classes
# Appropriate Uses of Lambda Expressions
# Classic Functional Constructs
list(map(lambda x: x.upper(), ["cat", "dog", "cow"]))  #

list(filter(lambda x: "o" in x, ["cat", "dog", "cow"]))  # Output: ['dog', 'cow']

from functools import reduce

# reduce in cat dog cow
reduce(
    lambda acc, x: f"{acc} | {x}", ["cat", "dog", "cow"]
)  # Output: 'cat | dog | cow'


# Key Functions
ids = ["id1", "id2", "id30", "id3", "id22", "id100"]

print(sorted(ids))  # Output: ['id1', 'id100', 'id2', 'id22', 'id3', 'id30']


# UI Frameworks
# Python Interpreter
from timeit import timeit

timeit("lambda x: x + 1", number=10)
# Output: 0.000001

# timeit
# Monkey Patching
from contextlib import contextmanager
import secrets


def gen_token():
    """Generate a random token."""
    return f"TOKEN_{secrets.token_hex(8)}"


@contextmanager
def mock_token():
    """Context manager to monkey patch the secrets.token_hex
    function during testing.
    """
    default_token_hex = secrets.token_hex
    secrets.token_hex = lambda _: "feedfacecafebeef"
    yield
    secrets.token_hex = default_token_hex


def test_gen_token():
    """Test the random token."""
    with mock_token():
        assert gen_token() == f"TOKEN_{'feedfacecafebeef'}"


test_gen_token()

# Alternatives to Lambdas


# Map
# Filter
# Reduce
# Are Lambdas Pythonic or Not?
# Conclusion
