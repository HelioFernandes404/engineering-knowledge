# Basic data structures

# Arrays
import array

# Create an array of integers
arr = array.array("i", [1, 2, 3, 4, 5])

# Access elements
print(arr[0])  # Output: 1

# Append an element
arr.append(6)
# Remove an element
arr.remove(3)
print(arr)  # Output


# List
# Create a list
my_list = [1, 2, 3, 4, 5]
print(my_list[0])
my_list.append(6)
my_list.remove(3)
print(my_list)

# Stacks
stack = []

# Push elements
stack.append(1)
stack.append(2)
stack.append(3)

print(stack.pop)  # Op: 3
print(stack.pop)  # Op: 2

print(stack)  # [1]

# Queues
from collections import deque

# Create a queue
queue = deque()


# Enqueue elements
queue.append(1)
queue.append(2)
queue.append(3)

print(queue.popleft())
# Output: 1

print(queue.appendleft())
# Output: 2

# Hash tables
# (Dictionary)

# Add key-value paris
hash_table = {}

# Add key-value pairs
hash_table["key1"] = "value1"

# Acess value
print(hash_table["key1"])


# remover a key-value pair
del hash_table["key1"]
