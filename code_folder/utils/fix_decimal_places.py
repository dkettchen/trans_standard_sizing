import pandas as pd
from code_folder.utils.lookup import chest_meas, meas

def fix_decimal_places(input_df:pd.DataFrame, print_updates:bool=True):
    """
    checks for any measurements where the person likely just messed up the decimal point placement
    and fixes them (ex. 7146.0 when other values of that column were around 70 -> 71.46, 
    ex. 330.0 when other values of that column were around 30 -> 33.0)

    - accounts for decimals moved by up to 3 places (ex. 714.6, 7146.0, 71460.0 -> 71.46)
    - does not check for decimals that were moved down (ex. 7.146 would not be fixed)
    - if a value was far outside the range and not explained by decimal point placement, it removes it instead
    - prints whether it fixed it or couldn't figure it out

    returns a new df
    """
    new_df = input_df.copy()
    # check each unit separately
    for unit in ["cm", "inch"]:
        if print_updates:
            print("Now checking:", unit)
        unit_df = new_df.where(new_df["unit"] == unit)

        # check each measurement column
        for col in chest_meas + meas:
            # get one unit
            unit_col = unit_df[col]

            # check for values outside our general range of realistic measurements
            strange_values = list(unit_col.where(
                (unit_col < 0) | (
                    (unit_col > 220) & (unit == "cm")
                ) | (
                    (unit_col > 86) & (unit == "inch")
                )
            ).dropna(how="all"))

            # if there were such values
            if len(strange_values) != 0:
                if print_updates:
                    print("Strange values found:", col, strange_values)

                # get the average of the remaining values
                unit_avg = round(unit_col.mask(unit_col.isin(strange_values)).mean(), 2)

                for value in strange_values:
                    rectified = False
                    # see if it was just a misplaced decimal
                    for magnitude in [10, 100, 1000]:
                        if value / magnitude >= unit_avg - 10 and value / magnitude <= unit_avg + 10:
                            if print_updates:
                                print(f"Dividing value by {magnitude} to fix decimal place:", value, value / magnitude)
                            new_df[col] = new_df[col].mask(
                                (new_df[col] == value) & (new_df["unit"] == unit),
                                value / magnitude
                            )
                            rectified = True
                            break

                    # if it couldn't be figured out, print & remove it from data set for now
                    if not rectified: 
                        if print_updates:
                            print("❌ Puzzling value:", value, unit_avg)
                        new_df[col] = new_df[col].mask(
                            (new_df[col] == value) & (new_df["unit"] == unit)
                        )

    return new_df
