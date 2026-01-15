# class is a blueprint for creating objects
# Instantieate a class to create an object
# Use attributes and methods to define the object's properties and behaviors
# Use inheritance to create a new class based on an existing class
# Reference a method on a parent lcass using super()
# Check if an object is an instance of a particular class using isinstance()


class Dog:
    pass


# Class and Instance Attributes
class Dog:

    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age


# Instancer in class
miles = Dog("Miles", 4)
buddy = Dog("Buddy", 9)


# Instence methods
class Dog:
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"

    def speak(self, sound):
        return f"{self.name} says {sound}"


miles = Dog("Miles", 4)

miles.description()


miles.speak("Woof Woof")


miles.speak("Bow Wow")

print(miles)  # Miles is 4 years old (from __str__ method)


class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __str__(self):
        return f"The {self.color} car has {self.mileage} miles"


car1 = Car("blue", 20000)
car2 = Car("red", 30000)

print(car1)  # The blue car has 20000 miles
print(car2)  # The red car has 30000 miles

# Inherti from another class in python


class Parent:
    hair_color = "black"


class Child(Parent):
    pass

    def __str__(self):
        return f"Child hair color is {self.hair_color}"


print(Child())  # Child hair color is black


## overriden
class Child(Parent):
    hair_color = "brown"


# Extended
class Parent:
    speaks = ["English"]


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.speaks.append("Spanish")  # Extended


# Parent class functionality Extension
class JackRusselllTerrier(Dog):
    def speak(self, sound="arf"):
        return f"{self.name} say {sound}"


class GoldenRetriever(Dog):
    def speak(self, sound="Bark"):
        return super().speak(sound)


gold_retriver = GoldenRetriever("Buddy", 9)


print(isinstance(gold_retriver, Dog))  # True
