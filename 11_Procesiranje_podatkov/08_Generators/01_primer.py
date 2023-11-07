# Iteration is the repetition of some kind of process over and over again.

# Iterating over a list
ez_list = [1, 2, 3]
for i in ez_list:
    print(i)

print("-----------------------")

# Iterating over a string
ez_string = "Generators"
for s in ez_string:
    print(s)

print("-----------------------")

# Iterating over a dictionary
ez_dict = {1: "First", 2: "Second"}
for key, value in ez_dict.items():
    print(key, value)

# We refer to any object that can support iteration as an iterable

# Ne deulje! ni iterable
# number = 12345
# for n in number:
#     print(n)
