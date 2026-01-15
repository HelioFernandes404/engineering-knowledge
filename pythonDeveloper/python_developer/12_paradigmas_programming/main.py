# https://opensource.com/article/19/10/python-programming-paradigms

# Imperative programming

sample_characters = ['p', 'y', 't', 'h', 'o', 'n']
sample_string = ''

sample_string = sample_string + sample_characters[0]
sample_string = sample_string + sample_characters[1]
sample_string = sample_string + sample_characters[2]
sample_string = sample_string + sample_characters[3]
sample_string = sample_string + sample_characters[4]
sample_string = sample_string + sample_characters[5]

# using a for loop (also considered imperative)
for c in sample_characters:
    sample_string = sample_string + c
    print(sample_string)

# Functional programming
import functools
sample_string = functools.reduce(lambda x, y: x + y, sample_characters)
print(sample_string)


sample_list = [1, 2, 3, 4, 5]
import functools
sum = functools.reduce(lambda x, y: x + y, sample_list)
print(sum)
# 15


# Procedural programming ( subtype of imperative programming)
def stringify(characters):
    result = ''
    for c in characters:
        result = result + c
    return result

sample_string = = ['p', 'y', 't', 'h', 'o', 'n']
print(stringify(sample_string))

# Object-oriented programming
class StringOps:
    def __init__(self, characters):
        self.characters = characters

    def stringify(self):
        self.string = ''.join(self.characters)

sample_string=StringOps(sample_characters)
sample_string.stringify()
sample_string.string

   
# What programming paradigm should I choose?

# The choice of programming paradigm depends on the problem you are trying to solve.
# If you are working with data, functional programming is a good choice.
# If you are working with user interfaces, object-oriented programming is a good choice.
# If you are working with hardware, procedural programming is a good choice.
# If you are working with algorithms, imperative programming is a good choice.
# If you are working with a combination of these, you can mix and match paradigms as needed.