# Python - Magic or Dunder Methods

# Built-in classes in Python define many magic methods. Use the dir() function to see the number of magic methods inherited by a class. For example, the following code defines a simple class and uses the dir() function to list the magic methods:
print(dir(int))

num = 10
res = num.__add__(5)
print(res)
# Output: 15


# __new__() Method
# The __new__() method is called when an object is created. It is the first method to be called. The __new__() method is used to create an instance of a class. It returns


class Employee:
    def __new__(cls, *args, **kwargs):
        print("Employee object created")
        instance = object.__new__(cls)
        return instance

    def __init__(self, name, age):
        print("Employee object initialized")
        self.name = "Satya"
        self.age = "21"


emp = Employee("Satya", 21)
# Output: 1. __new__ -> 2. __init__

# __str__() Method
num = 12
val = int.__str__(num)
print(type(val))


class Employee:
    def __init__(self) -> None:
        self.name = "Swati"
        self.salary = 10000

    def __str__(self) -> str:
        return f"{self.name} earns {self.salary}"


e1 = Employee()
print(e1)
# Output: Swati earns 10000


# __add__() Method
# Override
class Distance:
    def __init__(self, x=None, y=None) -> None:
        self.ft = x
        self.inch = y

    def __add__(self, x):
        temp = Distance()
        temp.ft = self.ft + x.ft
        temp.inch = self.inch + x.inch
        if temp.inch >= 12:
            temp.ft += 1
            temp.inch -= 12
        return temp

    def __str__(self) -> str:
        return f"{self.ft} ft {self.inch} inch"


d1 = Distance(5, 10)
d2 = Distance(6, 5)
print("d1= {} d2={}".format(d1, d2))

d3 = d1 + d2
print("d3= {}".format(d3))


# __ge__() Method

# To more:
# https://www.tutorialsteacher.com/python/magic-methods-in-python
