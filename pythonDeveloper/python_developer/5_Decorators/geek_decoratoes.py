# Decorators in Python
# https://www.geeksforgeeks.org/decorators-in-python/


def decorator(func):

    def wrapper():
        print("Before function execution")
        func()
        print("After function execution")

    return wrapper


@decorator
def greet():
    print("Hello")


greet()
# output:
# Before function execution
# Hello
# After function execution


# Higher Order Function
def fun(f, x):
    return f(x)


def square(x):
    return x * x


res = fun(square, 5)
print(res)
# Output: 25


# Assigning function to a variable
def greet(n):
    return f"Hello, {n}"


say_hi = greet
print(say_hi("John"))
# Output: Hello, John


def apply(f, val):
    return f(val)


res = apply(say_hi, "John")
print(res)  # Output: Hello, John


# Returning function from function
def make_mult(factor):
    def mult(n):
        return n * factor

    return mult


dbl = make_mult(2)
print(dbl(10))  # Output: 20

# Type of Decorators


## 1. Function Decorators
def simple_decorator(func):
    def wrapper():
        print("Before function execution")
        func()
        print("After function execution")

    return wrapper


@simple_decorator
def greet():
    print("Hello")


## 2. Method Decorators
print("## Method Decorators")


def method_decorator(func):
    def wrapper(self, *args, **kwargs):
        print("Before function execution")
        res = func(self, *args, **kwargs)
        print("After function execution")
        return res

    return wrapper


class MyClass:
    @method_decorator
    def greet(self):
        print("Hello")


obj = MyClass()
obj.greet()
# Output: Hello


## 3. Class Decorators
print("## Class Decorators")


def fun(cls):
    cls.class_name = cls.__name__
    return cls


@fun
class Person:
    pass


print(Person.class_name)
# Output: Person


## Common bulit-in decorators
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y


res = MathOperations.add(4, 5)
print(res)  # Output: 9

# @Classmethod


class Employee:
    raise_amt = 1.05

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount


Employee.set_raise_amt(1.10)
print(Employee.raise_amt)  # Output: 1.1


## property
class Circle:
    def __init__(self, redius):
        self._radius = redius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius should be non-negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * (self._radius**2)


c = Circle(5)
print(c.radius)  # Output: 5
print(c.area)  # Output: 78.53975
c.radius = 10
print(c.area)  # Output: 314.159


# Chaining Decorators
def decor1(func):
    def inner():
        x = func()
        return x * x

    return inner


def decor(func):
    def inner():
        x = func()
        return 2 * x

    return inner


@decor1
@decor
def num():
    return 10


print(num())  # Output: 400


@decor
@decor1
def num():
    return 10


# Output: 200
