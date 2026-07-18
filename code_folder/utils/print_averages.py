import pandas as pd
from code_folder.utils.standard_deviation import standard_deviation
from code_folder.utils.unit_conversion import convert_measurement
from code_folder.utils.lookup import chest_meas, meas

def print_averages(input_df:pd.DataFrame):
    """prints averages and standard deviation of relevant measurements in input data"""

    # check by direction
    for direction in ["Transmasc", "Transfemme"]:
        print(direction)

        for col in chest_meas + meas:

            list_for_sd = list(input_df[col].where(input_df["direction"] == direction).dropna())

            # make sure there's enough values for this measurement
            if len(list_for_sd) < 5:
                continue

            # find standard deviation
            stan_dev = standard_deviation(list_for_sd)
            # find average
            col_avg = round(input_df[col].where(input_df["direction"] == direction).mean(), 2)

            if col in [
                "chest circumference (post-op or binder)",
                "bust circumference (standing/no binder)",
                "height (REQUIRED)",
                "natural waist circumference (REQUIRED)",
                "hip circumference (REQUIRED)",
            ]:
                in_avg = round(convert_measurement(col_avg, "cm"),2)
                if col == "height (REQUIRED)":
                    inches = round(in_avg % 12,2)
                    feet = round(in_avg / 12)
                    in_avg = f"{feet}'" + f'{inches}"'
                else: 
                    in_avg = f'{in_avg}"'

                print(stan_dev, " - ", f"{col_avg} cm / {in_avg} for", col, direction)
