#!/usr/bin/env python3
#====================================================
# Script Name:    gtrace.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-18 10:35:56
#====================================================
import tkinter as tk
from tkinter import ttk

def calculate_trace_thickness(current, thickness=1.0, temperature_rise=10):
    """
    Calculate the trace thickness for a PCB based on the given inputs.

    Parameters:
    current (float): The current in Amperes.
    thickness (float): The thickness in ounces (default is 1.0 oz).
    temperature_rise (float): The temperature rise in Celsius.

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

def calculate_and_display():
    current = float(current_entry.get())
    thickness = float(thickness_entry.get())
    temperature_rise = float(temp_rise_entry.get())

    trace_thickness_mils = calculate_trace_thickness(current, thickness, temperature_rise)
    trace_thickness_mm = mils_to_mm(trace_thickness_mils)

    result_label.config(text=f"Trace Thickness: {trace_thickness_mils:.2f} mils ({trace_thickness_mm:.2f} mm)")

# Create the main window
root = tk.Tk()
root.title("PCB Trace Thickness Calculator")

# Create and place the input fields and labels
ttk.Label(root, text="Current (A):").grid(column=0, row=0, padx=10, pady=5)
current_entry = ttk.Entry(root)
current_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(root, text="Thickness (oz):").grid(column=0, row=1, padx=10, pady=5)
thickness_entry = ttk.Entry(root)
thickness_entry.grid(column=1, row=1, padx=10, pady=5)
thickness_entry.insert(0, "1.0")

ttk.Label(root, text="Temperature Rise (°C):").grid(column=0, row=2, padx=10, pady=5)
temp_rise_entry = ttk.Entry(root)
temp_rise_entry.grid(column=1, row=2, padx=10, pady=5)

# Create and place the calculate button
calculate_button = ttk.Button(root, text="Calculate", command=calculate_and_display)
calculate_button.grid(column=0, row=3, columnspan=2, pady=10)

# Create and place the result label
result_label = ttk.Label(root, text="Trace Thickness: ")
result_label.grid(column=0, row=4, columnspan=2, pady=10)

# Run the application
root.mainloop()
