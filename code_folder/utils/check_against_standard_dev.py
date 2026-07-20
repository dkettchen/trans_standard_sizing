import pandas as pd
from code_folder.utils.standard_deviation import standard_deviation
from code_folder.utils.lookup import chest_meas, meas, torso_meas, torso_dist
from code_folder.utils.compare_measurements import (
    compare_torso_measurements, 
    compare_torso_distances, 
    compare_other_meas
)

def check_against_standard_dev(input_df:pd.DataFrame, print_what_is_removed:bool=False):
    new_df = input_df.copy()

    # check by direction
    for direction in ["Transmasc", "Transfemme"]:
        if print_what_is_removed:
            print(direction)
        temp_df = new_df.where(new_df["direction"] == direction)

        # check that torso measurements roughly make sense compared to each other
        temp_df["TORSO_MEASUREMENTS"] = temp_df.apply(compare_torso_measurements, axis=1)
        temp_df["TORSO_DISTANCES"] = temp_df.apply(compare_torso_distances, axis=1)

        # checking other measurements against relevant reference measurements where available
        for column in [
            "shoulder (REQUIRED)",
            "arm length (REQUIRED)",
            "armhole height (front)",
            "shoulder to elbow",
            "shoulder width (back)",
            "shoulder width (front) (REQUIRED)",
            "clavicle to shoulder point distance",
            "nipple/bust point distance",
            "head circumference",
            "nape of the neck to front natural waist",
            "ankle to floor",
        ]:
            temp_df[f"CHECK_{column}"] = temp_df.apply(compare_other_meas, args=[column], axis=1)

        
        for col in chest_meas + meas:
            # get col data
            col_srs = temp_df[col]

            # if there are any values for this column
            if len(col_srs.dropna() > 0):

                # omit min & max values if list is long enough 
                # to avoid scewing the ref values we're checking based on
                if len(col_srs.dropna()) > 10:
                    limited_range = col_srs.dropna().sort_values()[1:-1]
                else: # otherwise just use whole sample
                    limited_range = col_srs.dropna()

                # find standard deviation
                stan_dev = standard_deviation(list(limited_range))
                # find average
                col_avg = round(limited_range.mean(), 2)

                # check any values that are outside of standard dev:
                    # x4 seems to catch all the obviously incorrect ones 
                    # while leaving the ones I suspect to be real ones
                min_val = col_avg - stan_dev*4
                max_val = col_avg + stan_dev*4

                outliers = col_srs.where(
                    (col_srs < min_val) | (col_srs > max_val)
                )
                # if there were such outliers
                if len(outliers.dropna()) > 0:
                    # check each value
                    for value in list(outliers.dropna().unique()):
                        outlier_responses = temp_df.where(
                            (
                                temp_df["direction"] == direction
                            ) & (
                                temp_df[col] == value
                            )
                        ).dropna(how="all")

                        # check if the flagged measurement was already marked as proportionally sound
                        if col in torso_meas and (outlier_responses["TORSO_MEASUREMENTS"].unique()) == [True]:
                            continue
                        elif col in torso_dist and (outlier_responses["TORSO_DISTANCES"].unique()) == [True]:
                            continue
                        elif col in [ # measurements that have been checked
                            "shoulder (REQUIRED)",
                            "arm length (REQUIRED)",
                            "armhole height (front)",
                            "shoulder to elbow",
                            "shoulder width (back)",
                            "shoulder width (front) (REQUIRED)",
                            "clavicle to shoulder point distance",
                            "nipple/bust point distance",
                            "head circumference",
                            "ankle to floor",
                        ] and (outlier_responses[f"CHECK_{col}"].unique()) == [True]:
                            continue
                        elif col in [ # measurements that have been checked as ref
                            "front width", "back width", 
                            "nape of the neck to end of ribcage/sternum",
                            "end of ribcage/sternum to natural waist"
                        ]: 
                            if col == "front width":
                                ref_col = "shoulder width (front) (REQUIRED)"
                            elif col == "back width":
                                ref_col = "shoulder width (back)"
                            else: 
                                ref_col = "nape of the neck to front natural waist"
                            if (outlier_responses[f"CHECK_{ref_col}"].unique()) == [True]:
                                continue

                        if print_what_is_removed:
                            # print what was found
                            print("⭕ removing:", value, col, list(outlier_responses.index))
                                # currently removing:
                                # Transmasc
                                # ⭕ removing: 5.0 distance between lowest/bending/middle points of your scars (top surgery) ['01/07/2026 12:33:48']
                                # ⭕ removing: 36.0 clavicle to shoulder point distance ['05/07/2026 18:41:09']
                                # ⭕ removing: 24.0 natural waist to high hip distance (side) ['29/06/2026 00:52:46']
                                # Transfemme
                                # ⭕ removing: 45.72 shoulder (REQUIRED) ['28/06/2026 00:43:40']
                                # ⭕ removing: 78.74 arm length (REQUIRED) ['28/06/2026 00:43:40']
                                # ⭕ removing: 20.0 natural waist to high hip distance (side) ['20/07/2026 10:41:09']
                                # ⭕ removing: 19.0 natural waist to high hip distance (back) ['20/07/2026 10:41:09']

                        # remove any values that aren't realistic
                        new_df[col] = new_df[col].mask(
                            (new_df[col] == value) & (new_df["direction"] == direction)
                        )

            # else: # otherwise mark that there were no values found
                # print("No values found for:", col, "in", direction)

    return new_df