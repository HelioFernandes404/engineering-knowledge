# Python Modules


def add(a, b):
    result = a + b
    return result


# Import modules in python
import math

print("The value of pi is", math.pi)
# Python import with Renaming
import math as m

print(m.pi)

# Python from... import statemnet
from math import pi

print(pi)

# Import all names from the standard module math
from math import *

print("The value of pi is", pi)

# Builtin

## The dir() built-in function
print(dir(exemple))

[
    "__builtins__",
    "__cached__",
    "__doc__",
    "__file__",
    "__initializing__",
    "__loader__",
    "__name__",
    "__package__",
    "add",
]

import exemple

exemple.__name__

# Output: 'example'
a = 1
b = "Hello"

import math

print(dir())
["__builtins__", "__doc__", "__name__", "a", "b", "math", "pyscripter"]
