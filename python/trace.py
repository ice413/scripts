#!/usr/bin/env python3

#====================================================
# Script Name:    trace.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-18 10:15:25
#====================================================

def calculate_trace_thickness(current, thickness=1.0, temperature_rise=10, length=100):
    """
    Calculate the trace thickness for a PCB based on the given inputs.

    Parameters:
    current (float): The current in Amperes.
    thickness (float): The thickness in ounces (default is 1.0 oz).
    temperature_rise (float): The temperature rise in Celsius (default is 10°C).
    length (float): The length of the trace in millimeters.

    Returns:
    float: The trace thickness in mils.
    """

    # Constants
    k = 0.024  # Constant for internal traces
    b = 0.44   # Constant for internal traces
    c = 0.725  # Constant for internal traces

    # Calculate the cross-sectional area in square mils
    area = (current / (k * (temperature_rise ** b))) ** (1 / c)

    # Calculate the trace thickness in mils
    trace_thickness = area / (thickness * 1.378)

    return trace_thickness

def mils_to_mm(mils):
    """
    Convert mils to millimeters.

    Parameters:
    mils (float): The value in mils.

    Returns:
    float: The value in millimeters.
    """
    return mils * 0.0254

def main():
    current = float(input("Enter the current in Amperes: "))
    thickness = float(input("Enter the thickness in ounces (default is 1.0 oz): ") or 1.0)
    temperature_rise = float(input("Enter the temp rise in celcius (default is 10c ): ") or 10)
    length = float(input("Enter the length of the trace in millimeters: "))

    # Using a default temperature rise of 10°C
    #temperature_rise = 10.0

    trace_thickness_mils = calculate_trace_thickness(current, thickness, temperature_rise, length)
    trace_thickness_mm = mils_to_mm(trace_thickness_mils)

    print(f"The trace thickness for the given inputs is {trace_thickness_mils:.2f} mils ({trace_thickness_mm:.2f} mm).")

if __name__ == "__main__":
    main()

