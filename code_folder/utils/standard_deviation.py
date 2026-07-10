from statistics import mean
from math import sqrt

# ✅ TESTED
def standard_deviation(list_of_nums:list[float|int]):
    """
    calculates the standard deviation of the given list of numbers
    """
    if len(list_of_nums) == 0:
        raise ValueError("List must contain at least one value.")

    # calculate mean of numbers
    avg = mean(list_of_nums)

    variance_nums = []

    # for each number
    for num in list_of_nums:
        # substract mean
        diff = num - avg

        # square result
        square_diff = diff * diff
    
        variance_nums.append(square_diff)

    # mean of squared differences -> called variance
    variance = mean(variance_nums)

    # take square root of variance
    std_dev = sqrt(variance)

    return round(std_dev, 2)
