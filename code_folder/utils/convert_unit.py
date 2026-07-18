import pandas as pd
from typing import Literal
from code_folder.utils.unit_conversion import convert_measurement, opposite_unit
from code_folder.utils.lookup import chest_meas, meas

def convert_unit_to(input_df:pd.DataFrame, unit:Literal["cm", "inch"]):
    """
    converts all measurements in the df from their original unit to the given one if not already in that unit
    
    updates unit column accordingly and returns new df
    """
    new_df = input_df.copy()

    opp_unit = opposite_unit(unit)

    for col in new_df.columns:
        if col in meas or col in chest_meas:
            new_df.loc[new_df["unit"] == opp_unit, col] \
            = new_df.loc[new_df["unit"] == opp_unit, col].apply(
                lambda x: round(convert_measurement(x, opp_unit), 3)
            )
            # if col in min_meas:
            #     print(new_df[col].min(), new_df[col].max(), col)
    
    new_df["unit"] = unit

    return new_df
