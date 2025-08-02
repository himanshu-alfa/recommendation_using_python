#!/usr/bin/env python3
"""
A simple Python program demonstrating basic programming concepts.
"""

def greet_user(name):
    """Function to greet a user by name."""
    return f"Hello, {name}! Welcome to Python programming."

def main():
    """Main function that runs the program."""
    # Simple greeting
    print("=== Simple Python Program ===")
    
    # Variables
    message = "Hello, World!"
    number = 42
    
    # Print basic information
    print(message)
    print(f"The answer to everything is: {number}")
    
    # Get user input and use function
    user_name = input("What's your name? ")
    greeting = greet_user(user_name)
    print(greeting)
    
    # Simple calculation
    x = 10
    y = 5
    result = x + y
    print(f"Simple math: {x} + {y} = {result}")
    
    print("Program completed successfully!")

if __name__ == "__main__":
    main()