from __future__ import print_function

# Basic Syntax
print("Hello World")

## Reserved Words

# and as assert break class continue def del elif else except exec finally for from global if import in is lambda not or pass print raise

# Variables and Data Types
name = "John"
age = 25

type(name)  # <class 'str'>
type(age)  # <class 'int'>

# Coditionals
if "foo" in ["bar", "baz", "qux"]:
    print("Expression was true")
    print("Executing statement in suite")
    print("...")
    print("Done.")
print("After conditional")

# Does line execute?                        Yes    No
#                                           ---    --
if "foo" in ["foo", "bar", "baz"]:  #  x
    print("Outer condition is true")  #  x

    if 10 > 20:  #  x
        print("Inner condition 1")  #        x

    print("Between inner conditions")  #  x

    if 10 < 20:  #  x
        print("Inner condition 2")  #  x

    print("End of outer condition")  #  x
print("After outer condition")  #  x

# Loops
count = 0
while count < 5:
    count = count + 1
    print("Hello World")

# While loop with else
count = 0
while count < 5:
    count = count + 1
    print("Hello World")
else:
    print("In else Black")

# For loop
n = 4
for i in range(0, n):
    print(i)

# For loop with Dictionary
d = dict({"foo": 1, "bar": 2, "baz": 3})
for i in d:
    print("key: %s, value: %d" % (i, d[i]))

# Dictionary output
# key: foo, value: 1
# key: bar, value: 2
# key: baz, value: 3

# Index of Sequences
list = [1, 2, 3, 4, 5]
for index in range(len(list)):
    print(list[index])

# For loop with else
list = [1, 2, 3, 4, 5]
for index in range(len(list)):
    print(list[index])
else:
    print("In else block")

## Index of Sequences
list = ["apple", "banana", "cherry"]
for index in range(len(list)):
    print(list[index])
# Output: apple banana cherry

## Nested loops
for i in range(1, 5):
    for j in range(i):
        print(i, end=" ")
    print()
# 1
# 2 2
# 3 3 3
# 4 4 4 4

## Loop control statements
### Continue statement
for letter in "python":
    if letter == "h":
        continue
    print("Current Letter: ", letter)
### Break statement
for letter in "python":
    if letter == "h":
        break
    print("Current Letter: ", letter)
    # Output : Current Letter:  h
### Pass statement
for letter in "python":
    if letter == "h":
        pass
        print("Last letter: ", letter)
    print("Current Letter: ", letter)
### How for loops internally in Python
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)
fruit = ["apple", "banana", "cherry"]
iter_obj = iter(fruit)
while True:
    try:
        print(next(iter_obj))
    except StopIteration:
        break
# output: apple banana cherry

# Type Casting

## Two types of type casting (Implicit and Explicit)

# Integer to float
integer_number = 123
float_number = 1.23

new_number = integer_number + float_number

# Display the new number and result data type
print("Value ", new_number)
print("Data type", type(new_number))

## Addition of string and integer using explict conversion
num_string = "12"
num_integer = 23

print("Data type of num_string before Type Casting: ", type(num_string))
# explicit type conversion
num_string = int(num_string)

print("Data type of num_string after Type Casting: ", type(num_string))

num_sum = num_string + num_integer

print("sum: ", num_sum)
print("Data type of sum: ", type(num_sum))


# Exceptions

## Python Exceptions

### Python Built-in Exceptions
print(dir(locals()["__builtins__"]))

### Python Error and Exception
# Python try...except Block
try:
    # block of code
    pass
except Exception as e:
    # block
    pass

# Exception handling using try... except
try:
    numerator = 10
    denominator = 0

    result = numerator / denominator

    print("Result: ", result)
except:
    print("Error: Division by zero")

# Catchinh specific exception in Python
try:
    even_numbers = [2, 4, 6, 8, 10]
    print(even_numbers[5])

except ZeroDivisionError:
    print("Error: Division by zero")
except IndexError:
    print("Error: Index out of range")

# Python try with else clause
try:
    num = int(input("Enter a number: "))
    assert num % 2 == 0
except:
    print("Error: Only even numbers are allowed")
else:
    reciprocal = 1 / num
    print("Reciprocal of ", num, " is ", reciprocal)

# Python try with finally clause
try:
    numerator = 10
    denominator = 0

    result = numerator / denominator

    print("Result: ", result)
except:
    print("Error: Division by zero")
finally:
    print("This is finally block")


# Python Custom Exceptions
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Python User-Defined Exception
class InvalidAgeExeption(Exception):
    "Raised whe in input value is less than 18"
    pass


# you need to guess this number
number = 18
try:
    i_num = int(input("Enter a number: "))
    if i_num < number:
        raise InvalidAgeExeption
    else:
        print("Congratulations! You guessed it correctly.")

except InvalidAgeExeption:
    print("This value is too small, try again!")


# Customizing Exception Classes
class SalaryNotInRange(Exception):
    def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
        self.salary = salary
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.salary} -> {self.message}"


salary = int(input("Enter salary: "))
if not 5000 < salary < 15000:
    raise SalaryNotInRange(salary)

# Functions, builtin functions


## Creating a fuction
def my_function():
    print("Hello from my function")


# Calling a function
my_function()


# Arguments
def my_function_with_args(username, greeting):
    print("Hello, %s, From My Function!, I wish you %s" % (username, greeting))


my_function_with_args("John Doe", "a great year!")

# Parameters or Arguments?


## Number of Arguments
def num_args(fname, lname):
    print("Hello", fname, lname)


num_args("John", "Doe")  # this fuction expetcs 2 arguments, and get 2 arguments


# Arbitrary Arguments, *args
def greet_kids(*kids):
    print("The youngest child is " + kids[2])


greet_kids("Emil", "Tobias", "Linus")  # output: The youngest child is Linus


# Keyword Arguments
def greet_kids(child3, child2, child1):
    print("The youngest child is " + child3)


greet_kids(
    child1="Emil", child2="Tobias", child3="Linus"
)  # output: The youngest child is Linus


# Arbitrary Keyword Arguments, **kwargs
def greet_kids(**kids):
    print("The youngest child is " + kids["child3"])


greet_kids(fname="Tobias", lname="Linus")  # output: The youngest


# Default Parameter Value
def default_value(country="Norway"):
    print("I am from " + country)


default_value("Sweden")  # output: I am from Sweden
default_value()  # output: I am from Norway
default_value("India")  # output: I am from India


# Passing a List as an Argument
def print_food(food):
    for x in food:
        print(x)


fruits = ["apple", "banana", "cherry"]

print_food(fruits)  # output: apple banana cherry


# Return Values
def my_function(x):
    return 5 * x


print(my_function(3))  # output: 15


# The pass Statement
def my_function_pass():
    pass


# having an empty function definition like this, would raise an error without the pass statement


# Positional-Only arguments
def positional_only(arg, /):
    print(arg)


positional_only(10)  # output: 10


# Keyword-Only arguments


def keyword_only(*, arg):
    print(arg)


print(arg=10)  # output: 10


# Combine positional-only and keyword-only arguments
def combined_example(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)


combined_example(5, 6, c=7, d=8)


# Recursion
def tri_recursion(k):
    if k > 0:
        result = k + tri_recursion(k - 1)
        print(result)
    else:
        result = 0
    return result


print("\n\nRecursion Example Results")
tri_recursion(6)

# List, Tuple, Set,

## List dynamic array
["apple", "banana", "cherry"]
# 1. Quando voce precisa mutar sua lista
# 2. Quando voce preicsa remover e adicionar elementos

## Tuple immutable list
("apple", "banana", "cherry")
# 1. Se seus dados devem ou não ser alterados
# 2. Tuplas são mais rapida que listas. Devemos usar tupla em vez de lista se estivermos deifindo conjuntos constente de valores de tudo o que vamos fazer e iterar sobre eles
# 3. Se precisarmos de um arry de eleemntos para serem usa como chaves de dicionario, podemos usar tuplas, como lista são mutaveis, elas não podem ser usadas como chaves de dicionario


## Set unordered collection of unique items
{"apple", "banana", "cherry"}


# Dictionaries
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

print(thisdict)


# Dict items
print(thisdict["brand"])

# Ordered or Unordered?

# Changeable

# Dirct items - Datar types

thisdict = {
    "brand": "Ford",
    "electric": False,
    "year": 1964,
    "colors": ["red", "white", "blue"],
}  # Output: {'brand': 'Ford', 'electric': False, 'year': 1964, 'colors': ['red', 'white', 'blue']}


# The dic() Constructor
thisdict = dict(brand="Ford", model="Mustang", year=1964)

# https://www.python.org/
