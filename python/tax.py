#!/usr/bin/env python3
#====================================================
# Script Name:    tax.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-18 07:40:56
#====================================================

def calculate_percentage(a, b):
    try:
        percentage = (b / a) * 100
        return round(percentage, 2)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."

# Get user input
a = float(input("How much did you earn: "))
b = float(input("How much in tax: "))

# Calculate and display result
result = calculate_percentage(a, b)
print(f"You paid {result}% in tax.")

