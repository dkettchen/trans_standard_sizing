from typing import Literal

def opposite_unit(unit):
    """
    returns the other unit for the given one
    
    opposite_unit("cm") -> "in"
    opposite_unit("in") -> "cm"
    """
    if unit == "cm":
        return "in"
    return "cm"

def cm_to_inch(cm:int|float):
    return cm/2.54

def inch_to_cm(inches:int|float):
    return inches*2.54

# ✅ TESTED
def convert_measurement(input_measurement:int|float, unit:Literal["cm", "in"]):
    """
    takes a measurement and its unit

    converts the given measurement from the given unit to the other one
    """
    if unit == "cm":
        new_measurement = cm_to_inch(input_measurement)
    else:
        new_measurement = inch_to_cm(input_measurement)

    return new_measurement

