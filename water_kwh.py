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
    :return: Energy required in kWh
    """
    specific_heat_capacity = 4186  # J/kg°C (Joules per kilogram per degree Celsius)
    joules_per_kwh = 3_600_000  # 1 kWh = 3.6 million Joules

    mass = liters  # 1 liter of water ≈ 1 kg
    delta_temp = temp_end - temp_start

    energy_joules = mass * specific_heat_capacity * delta_temp
    energy_kwh = energy_joules / joules_per_kwh

    return energy_kwh

def calculate_time_needed(energy_kwh, heater_power_kw):
    """
    Calculate the time required to heat the water given a heater's power.
    :param energy_kwh: Energy required in kWh
    :param heater_power_kw: Heater power in kW
    :return: Time in hours
    """
    if heater_power_kw <= 0:
        return float('inf')  # Prevent division by zero
    return energy_kwh / heater_power_kw

if __name__ == "__main__":
    liters = float(input("Enter amount of water in liters: "))
    temp_start = float(input("Enter starting temperature (°C): "))
    temp_end = float(input("Enter target temperature (°C): "))
    heater_power = float(input("Enter heater power in kW: "))

    energy_needed = calculate_energy(liters, temp_start, temp_end)
    time_needed = calculate_time_needed(energy_needed, heater_power)

    print(f"Energy required: {energy_needed:.2f} kWh")
    print(f"Time required with {heater_power:.2f} kW heater: {time_needed:.2f} hours")

