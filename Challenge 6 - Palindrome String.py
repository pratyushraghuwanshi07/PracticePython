# Ask the user for a string and print out whether this string is a palindrome or not. (A palindrome is a string that reads the same forwards and backwards.)

#Slicing in python - https://www.geeksforgeeks.org/string-slicing-in-python/

user_string = input("Type a string: ")
reverse_string = user_string[::-1]
print(f"Reverse string is: {reverse_string}")
if user_string == reverse_string:
    print(f"The string {user_string} is palindrome")
else:
    print(f"The string {user_string} is not palindrome")