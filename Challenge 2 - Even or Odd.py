# The exercise comes first (with a few extras if you want the extra challenge or want to spend more time), followed by a discussion. Enjoy!

# Ask the user for a number. Depending on whether the number is even or odd, print out an appropriate message to the user

num = int(input("what the number?"))
if num%2 == 0:
  print(f"Your number {num} is even")
else:
  print(f"Your number {num} is odd")