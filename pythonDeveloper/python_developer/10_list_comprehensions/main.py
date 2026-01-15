# Python - List Comprehension

fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

for x in fruits:
    if "a" in x:
        newlist.append(x)

print(newlist)

# with only one line of code

newlist = [x for x in fruits if "a" in x]
print(newlist)

# The Syntax
# newlist = [expression for item in iterable if condition == True]

# Condition
newlist = [x for x in fruits if x != "apple"]

newlist = [x for x in fruits]

# Iterable
newlist = [x for x in range(10)]

# Iterable with condition
newlist = [x for x in range(10) if x < 5]
print(newlist)


# Expression
newlist = [x.upper() for x in fruits]

# Outcome
newlist = ["hello" for x in fruits]

# manipulating the outcome
newlist = [x if x != "banana" else "orange" for x in fruits]
