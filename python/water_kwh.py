#!/usr/bin/env python3

def calculate_energy(liters: float, temp_start: float, temp_end: float, cop: float) -> float:
    """
    Räknar ut energi för att värma vatten från temp_start till temp_end.
        
    :param liters: Mängd vatten, i liter (float)
    :param temp_start: StartTemp i Celsius (float)
    :param temp_end: MålTemp i Celsius (float)
    :param cop: Coefficient of Performance (COP) på din värmare (float)
    :return: Energi i kWh (float)
    """
    specific_heat_capacity: float = 4186.0  # J/kg°C
    joules_per_kwh: int = 3_600_000  # 1 kWh = 3,600,000 Joules
    mass: float = liters  # Assuming 1 liter of water is approximately 1 kg
    delta_temp: float = temp_end - temp_start
    
    energy_joules: float = mass * specific_heat_capacity * delta_temp
    energy_kwh_required: float = energy_joules / joules_per_kwh
    
    # Calculate the actual energy consumed by multiplying the required energy by COP
    energy_kwh_consumed: float = energy_kwh_required / cop
    
    return energy_kwh_consumed

def calculate_time_needed(energy_kwh_consumed: float, heater_power_kw: float) -> float:
    """
    Hur länge behöver din värmare arbeta för att värma vattnet?
    
    :param energy_kwh_consumed: Energi i kWh (float)
    :param heater_power_kw: Effekt in kW (float)
    :return: Tid i timmar (float)
    """
    if heater_power_kw <= 0:
        return float('inf')  # Prevent division by zero
    
    time_needed: float = energy_kwh_consumed / heater_power_kw
    return time_needed

def calculate_total_cost(energy_kwh_consumed: float, cost_per_kwh: float) -> tuple[float, float]:
    """
    Räknar ut kostnad för att värma poolen, baserat på kWh pris.
    
    :param energy_kwh_consumed: Förbrukad energi i kWh (float)
    :param cost_per_kwh: Kostnad per kWh i SEK (float)
    :return: Total kostnad i SEK (float), Totalt kWh använt (float)
    """
    total_cost: float = energy_kwh_consumed * cost_per_kwh
    return total_cost, energy_kwh_consumed

def calculate_cop(energy_consumed: float, electrical_power: float) -> float:
    """
    Calculate the Coefficient of Performance (COP) of a heating system.
    
    :param energy_consumed: Energy consumed in kWh (float)
    :param electrical_power: Electrical power consumption in kW (float)
    :return: COP (float)
    """
    if electrical_power <= 0:
        return float('inf')  # Prevent division by zero
    
    cop: float = energy_consumed / electrical_power
    return cop

if __name__ == "__main__":
    liters: float = float(input("Hur stor är poolen, i liter: "))
    temp_start: float = float(input("Start temp (°C): "))
    temp_end: float = float(input("Måltemp (°C): "))
    
    heater_power: float = float(input("kW på värmaren: "))
    cost_per_kwh: float = float(input("Kostnad per kWh i SEK: "))
    cop_value: float = float(input("COP-värde på värmare: "))
    
    energy_needed: float = calculate_energy(liters, temp_start, temp_end, cop_value)
    time_needed: float = calculate_time_needed(energy_needed, heater_power)
    total_cost, total_kwh_consumed = calculate_total_cost(energy_needed, cost_per_kwh)
    cop: float = calculate_cop(total_kwh_consumed, heater_power)
    
    print(f"Energy required (adjusted for COP): {energy_needed:.2f} kWh")
    print(f"Time required with {heater_power:.2f} kW heater: {time_needed:.2f} hours")
    print(f"Total cost: {total_cost:.2f}kr SEK")
    print(f"Total kWh consumed: {total_kwh_consumed:.2f} kWh")
    print(f"Coefficient of Performance (COP): {cop:.2f}")