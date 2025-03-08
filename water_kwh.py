#!/usr/bin/env python3
#====================================================
# Script Name:    water_kwh.py
# Description:    <Your Description Here>
# Author:        claes-nilsson
# Created:       2025-03-08 08:44:37
# Modified:       <Will auto-update on save>
#====================================================

def calculate_energy(liters, temp_start, temp_end):
    """
    Calculate the energy required to heat water from temp_start to temp_end.
    :param liters: Amount of water in liters
    :param temp_start: Starting temperature in Celsius
    :param temp_end: Target temperature in Celsius
    :return: Energy required in Wh or kWh
    """
    specific_heat_capacity = 4186  # J/kg°C (Joules per kilogram per degree Celsius)
    joules_per_wh = 3_600  # 1 Wh = 3.6 kJ

    mass = liters  # 1 liter of water ≈ 1 kg
    delta_temp = temp_end - temp_start

    energy_joules = mass * specific_heat_capacity * delta_temp
    energy_wh = energy_joules / joules_per_wh

    return energy_wh

if __name__ == "__main__":
    liters = float(input("Enter amount of water in liters: "))
    temp_start = float(input("Enter starting temperature (°C): "))
    temp_end = float(input("Enter target temperature (°C): "))

    energy_needed = calculate_energy(liters, temp_start, temp_end)

    if energy_needed >= 1000:
        print(f"Energy required: {energy_needed / 1000:.2f} kWh")
    else:
        print(f"Energy required: {energy_needed:.2f} Wh")

