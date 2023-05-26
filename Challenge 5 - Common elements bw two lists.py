# Take two lists, say for example these two:

#   a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
#   b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
# and write a program that returns a list that contains only the elements that are common between the lists (without duplicates). Make sure your program works on two lists of different sizes.

# Extras:

# Randomly generate two lists to test this
# Write this in one line of Python (don’t worry if you can’t figure this out at this point - we’ll get to it soon)

import random

list1 = []
list2 = []
final_list = []
for i in range(15):
    list1.append(random.randint(1,100))
for i in range(10):
    list2.append(random.randint(1,100))

print(f"{list1} \n {list2}")

for i in list2:
    if i in list1:
        final_list.append(i)

print(f"Commong elements b/w 2 lists are: {final_list}")
    