from code_folder.utils.unit_conversion import convert_measurement, cm_to_inch, inch_to_cm

def test_does_not_mutate_input():
    num = 3
    convert_measurement(num, "cm")
    assert num == 3
def test_returns_number():
    result = convert_measurement(3, "cm")
    assert type(result) in [int, float]
def test_returns_new_number():
    num = 3
    result = convert_measurement(num, "cm")
    assert result != num
def test_returns_different_number():
    result = convert_measurement(3, "cm")
    assert result != 3
def test_returns_cm_for_inch_input():
    result = convert_measurement(3, "inch")
    assert result == inch_to_cm(3)
def test_returns_inch_for_cm_input():
    result = convert_measurement(3, "cm")
    assert result == cm_to_inch(3)
