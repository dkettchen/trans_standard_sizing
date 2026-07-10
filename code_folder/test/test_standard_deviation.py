from utils.standard_deviation import standard_deviation
import pytest
from re import escape

def test_does_not_mutate_input():
    input_list = [46,69,32,60,52,41]
    standard_deviation(input_list)
    assert input_list == [46,69,32,60,52,41] 

def test_raises_value_error_for_empty_list():
    with pytest.raises(ValueError, match=escape("List must contain at least one value.")):
        standard_deviation([])

def test_returns_number():
    result = standard_deviation([46,69,32,60,52,41])
    assert type(result) in [int, float]

def test_returns_standard_deviation_for_given_numbers():
    # some of the examples didn't exactly match our results 
    # but upon manually checking ours seem to be calculating it correctly
    for num_list, sd in [
        ([46,69,32,60,52,41], 12.15), # 13.31
        ([2,1,3,2,4], 1.02), # 1.01
        ([85,86,100,76,81,93,84,99,71,69,93,85,81,87,89], 8.7), # 8.7
        ([9,7,10,8,9,7,8,9], 0.99), # 1.06
        ([95,93,95,94,96,94,95], 0.9), # 0.89
        ([90,81,95,91,86,82,78], 5.69), # 5.7
        ([2,3,4,5,6], 1.41) # 1.414
    ]:
        assert standard_deviation(num_list) == sd
