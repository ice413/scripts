#!/usr/bin/python3
#====================================================
# Script Name:    volt-div.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-07 22:39:20
# Modified:       <Will auto-update on save>
#====================================================

import sys

def e12_resistors():
    vin = float(input("Input voltage: ").strip())
    vout_desired = float(input("Output voltage: ").strip())
    
    if vin < vout_desired:
        print("Vin must be greater than or equal to Vout.")
        return
    
    e12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    solutions = []
    
    for r1 in e12:
        for r2 in e12:
            total = r1 + r2
            if total == 0:
                continue
            vout_calculated = (r2 / total) * vin
            error = abs(vout_calculated - vout_desired)
            solutions.append((vout_calculated, r1, r2, error))
    
    # Filter solutions with error within 5% of desired Vout
    filtered_solutions = []
    for sol in solutions:
        calculated_vout, r1, r2, error = sol
        if error <= 0.05 * vout_desired:
            filtered_solutions.append(sol)
    
    # Sort by current (ascending) and then by voltage error
    filtered_solutions.sort(key=lambda x: (vin / (x[0] + x[1]), abs(x[2] - vout_desired)))
    
    print(f"\nClosest E12 resistor combinations for Vin={vin}V, Vout≈{vout_desired}V:")
    for sol in filtered_solutions:
        calculated_vout, r1, r2, error = sol
        print(f"R1: {r1}Ω, R2: {r2}Ω → Calculated Vout={calculated_vout:.3f}V (Error: ±{error:.3f}V)")
    
    if not filtered_solutions:
        print("No valid combinations found within 5% error.")

def main():
    print("Welcome to the E12 Resistor Calculator!")
    print("This tool helps you find the closest E12 resistor combinations for your desired output voltage.")
    e12_resistors()

# Run the main function
if __name__ == "__main__":
    main()
