# Or Modules
# import modules_programiz  # <-- find

# Doc oficial python
import fibo

fibo.fib(1000)
# output: 0, 1, 1....

fibo.fib2(100)
# outpout: [1,2...]

fibo.__name__
# output: Fibo

# intend to use a function often you can assign it to a local name:

fib = fibo.fib
fib(500)

# More on modules
from fibo import fib, fib2

fib(500)

# Rename func
from fibo import fib as fibonacci

fibonacci(1000)

# Executing modules as scripts
if __name__ == "__main__":
    import sys

    fib(int(sys.argv[1]))
# $ python fibo.py 50


# Standard Modules
import sys

sys.ps1

sys.ps2

sys.ps1 = "C> "

#  PYTHONPATH

# Custom
