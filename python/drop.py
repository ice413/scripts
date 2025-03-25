#!/usr/bin/env python3
#====================================================
# Script Name:    drop.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-25 11:00:58
#====================================================

def calculate_resistance(length, width, thickness):
    """
    Calculate the resistance of a PCB trace based on the given inputs.

    Parameters:
    length (float): The length of the trace in millimeters.
    width (float): The width of the trace in millimeters.
    thickness (float): The thickness of the trace in ounces.

    Returns:
    float: The resistance in ohms.
    """
    # Constants
    resistivity_copper = 1.68e-8  # Resistivity of copper in ohm-meter
    thickness_meters = thickness * 35e-6  # Convert thickness from oz to meters (1 oz ≈ 35 µm)

    # Calculate the cross-sectional area in square meters
    cross_sectional_area = (width * 1e-3) * thickness_meters

    # Calculate the resistance in ohms
    resistance = (resistivity_copper * (length * 1e-3)) / cross_sectional_area

    return resistance

def calculate_voltage_drop(current, resistance):
    """
    Calculate the voltage drop across a PCB trace based on the given inputs.

    Parameters:
    current (float): The current in Amperes.
    resistance (float): The resistance in ohms.

    Returns:
    float: The voltage drop in volts.
    """
    return current * resistance

def main():
    current = float(input("Enter the current in Amperes: "))
    length = float(input("Enter the length of the trace in millimeters: "))
    width = float(input("Enter the width of the trace in millimeters: "))
    thickness = float(input("Enter the thickness of the trace in ounces: "))

    resistance = calculate_resistance(length, width, thickness)
    voltage_drop = calculate_voltage_drop(current, resistance)

    print(f"The resistance of the trace is {resistance:.6f} ohms.")
    print(f"The voltage drop across the trace is {voltage_drop:.6f} volts.")

if __name__ == "__main__":
    main()

