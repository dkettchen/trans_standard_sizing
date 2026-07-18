import pandas as pd
from code_folder.utils.lookup import (
    chest_meas, meas, 
    smallest_measurements, 
    min_max_values, 
    half_values, 
    compared_to_other_meas
)

def check_realistic_min_max_values(input_df:pd.DataFrame):
    """
    remove measurements that are outside a logical realistic range

    returns a new df
    """
    new_df = input_df.copy()

    for col in chest_meas + meas:

        # check any measurements other than smallest aren't too small
        if col not in smallest_measurements:
            # remove if smaller than 5
            new_df[col] = new_df[col].mask(
                new_df[col] < 5
            )

        # check min/max ranges
        if col in min_max_values:
            # remove if smaller than min or bigger than max
            new_df[col] = new_df[col].mask(
                (new_df[col] < min_max_values[col][0]) | (new_df[col] > min_max_values[col][1])
            )

        # check half measurements
        if col in half_values:
            # remove if <*0.2 to >*0.8
            new_df[col] = new_df[col].mask(
                (new_df[col] < new_df[half_values[col]] * 0.2) | (new_df[col] > new_df[half_values[col]] * 0.8)
            )

        # check other comparative measurements
        if col in compared_to_other_meas:
            # measurement + num shouldn't be smaller/bigger than other meas * decimal
            comp_data = compared_to_other_meas[col]

            if comp_data[1] == "smaller than":
                new_df[col] = new_df[col].mask(
                    (new_df[col] + comp_data[0] < new_df[comp_data[2]] * comp_data[3])
                )
            elif comp_data[1] == "bigger than":
                new_df[col] = new_df[col].mask(
                    (new_df[col] + comp_data[0] > new_df[comp_data[2]] * comp_data[3])
                )
    
    return new_df
