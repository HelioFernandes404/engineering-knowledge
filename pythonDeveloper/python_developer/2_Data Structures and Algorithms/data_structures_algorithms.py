# Arrays and linked Lists

# Creating an Array in Python:
from array import *

# a = array(data, type, value, list)
a = array("d", [1.1, 3.5, 4.5])
print(a[1])  # Output: 3.5

## various data types and their codes.
# 'b' -> Represents signed integer of size 1 byte
# 'B' -> Represents unsigned integer of size 1 byte...
# https://www.edureka.co/blog/arrays-in-python/


# Basic array operations
len(a)  # Output: 3

## Adding/ Changing elements of an Array:
a.append(5.5)
# Output: array('d', [1.1, 3.5, 4.5, 5.5])

a.extend([6.6, 7.7, 8.8])
# Output: array('d', [1.1, 3.5, 4.5, 5.5, 6.6, 7.7, 8.8])

a.insert(2, 0.0)
# Output: array('d', [1.1, 3.5, 0.0, 4.5, 5.5, 6.6, 7.7, 8.8])

# Array Concatenation :
a = array("d", [1.1, 3.5, 4.5])
b = array("d", [10.0, 20.0, 30.0])
c = array("d")
c = a + b
print("Array c = ", c)
# Output: Array c = array('d', [1.1, 3.5, 4.5, 10.0, 20.0, 30.0])

# Removing/ Deleting elements of an array:

a = array("d", [1.1, 3.5, 4.5, 5.5])
print(a.pop())  # Output: 5.5 # removes the last element
print(a.pop(1))  # Output: 3.5 # removes the element at index 1

# Remover
a.remove(1.1)
# Output: array('d', 3, 4.5, 5.5)

# Slicing an array :
a = array("d", [1.1, 3.5, 4.5, 5.5])
print(a[0:2])  # Output: array('d', [1.1, 3.5]) de 0 á 3 ele vai printar

# Looping through an array:
a = array("d", [1.1, 3.5, 4.5])
print("All elements of the array:")
for x in a:
    print(x)

print("spacfic value")
for x in a[1:3]:
    print(x)

#  Make sure you practice as much as possible and revert your experience.
# https://www.edureka.co/blog/arrays-in-python/


# Hash Tables

# Heaps, stacks, and queues

# binary search trees

# Recursion

# sorting algorithms
