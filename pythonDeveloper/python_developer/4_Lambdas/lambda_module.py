# Syntax labmda
# lambda arguments : expression

# Exemple: add 10 to arg a
x = lambda a: a + 10
print(x(10))

# Multiply
x = lambda a, b: a * b
print(x(5, 6))

# more args
x = lambda a, b, c: a + b + c
print(x(5, 6, 2))


# func the func lambda
def myfunc(n):
    return lambda a: a * n


mydoubler = myfunc(2)

print(mydoubler(11))

mytripler = myfunc(3)

print(mytripler(11))


# How to Use Python Lambda Functions


# Lambda Calculus
# History
# First Example
def identity(x):
    return x


# Anonymous Functions
# Python Lambda and Regular Functions
# Functions
# Traceback
# Syntax
# Arguments
# Decorators
# Closure
# Evaluation Time
# Testing Lambdas
# Lambda Expression Abuses
# Raising an Exception
# Cryptic Style
# Python Classes
# Appropriate Uses of Lambda Expressions
# Classic Functional Constructs
# Key Functions
# UI Frameworks
# Python Interpreter
# timeit
# Monkey Patching
# Alternatives to Lambdas
# Map
# Filter
# Reduce
# Are Lambdas Pythonic or Not?
# Conclusion
