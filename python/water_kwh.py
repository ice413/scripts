#!/usr/bin/env python3

def calculate_energy(liters: float, temp_start: float, temp_end: float) -> float:
    """
    Calculate the energy required to heat water from temp_start to temp_end.
    
    :param liters: Amount of water in liters (float)
    :param temp_start: Starting temperature in Celsius (float)
    :param temp_end: Target temperature in Celsius (float)
    :return: Energy required in kWh (float)
    """
    specific_heat_capacity: float = 4186.0  # J/kg°C
    joules_per_kwh: int = 3_600_000  # 1 kWh = 3,600,000 Joules
    mass: float = liters  # Assuming 1 liter of water is approximately 1 kg
    delta_temp: float = temp_end - temp_start
    
    energy_joules: float = mass * specific_heat_capacity * delta_temp
    energy_kwh: float = energy_joules / joules_per_kwh
    
    return energy_kwh

def calculate_time_needed(energy_kwh: float, heater_power_kw: float) -> float:
    """
    Calculate the time required to heat the water given a heater's power.
    
    :param energy_kwh: Energy required in kWh (float)
    :param heater_power_kw: Heater power in kW (float)
    :return: Time in hours (float)
    """
    if heater_power_kw <= 0:
        return float('inf')  # Prevent division by zero
    
    time_needed: float = energy_kwh / heater_power_kw
    return time_needed

def calculate_total_cost(energy_kwh: float, cost_per_kwh: float) -> tuple[float, float]:
    """
    Calculate the total cost based on the energy required and cost per kWh.
    
    :param energy_kwh: Energy required in kWh (float)
    :param cost_per_kwh: Cost per kWh in dollars (float)
    :return: Total cost in SEK (float), Total kWh consumed (float)
    """
    total_cost: float = energy_kwh * cost_per_kwh
    return total_cost, energy_kwh

if __name__ == "__main__":
    liters: float = float(input("Hur stor är poolen, i liter: "))
    temp_start: float = float(input("Start temp (°C): "))
    temp_end: float = float(input("Måltemp (°C): "))
    
    heater_power: float = float(input("kW på värmaren: "))
    cost_per_kwh: float = float(input("Kostnad per kWh i SEK: "))
    
    energy_needed: float = calculate_energy(liters, temp_start, temp_end)
    time_needed: float = calculate_time_needed(energy_needed, heater_power)
    total_cost, total_kwh = calculate_total_cost(energy_needed, cost_per_kwh)
    
    print(f"Energy required: {energy_needed:.2f} kWh")
    print(f"Time required with {heater_power:.2f} kW heater: {time_needed:.2f} hours")
    print(f"Total cost: {total_cost:.2f}kr SEK")
    print(f"Total kWh consumed: {total_kwh:.2f} kWh")