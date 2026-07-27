from code_folder.utils.lookup import separated_files_folder
import pandas as pd
from typing import Literal

# UTIL
def find_biggest(row:pd.Series):
    """find the biggest measurement out of chest, natural waist, and hip"""
    chest = row["chest"]
    waist = row["natural waist"]
    hip = row["hip"]
    if chest > waist and chest > hip:
        return "chest"
    if waist > chest and waist > hip:
        return "waist"
    if hip > chest and hip > waist:
        return "hip"

def biggest_measurement(unit:Literal["cm", "inch"]="cm"):
    """TODO"""

    df_dict = {}

    for direction in ["Transmasc", "Transfemme"]:
        # read in relevant data
        meas_filepath = f"{separated_files_folder}/measurements_in_{unit}_{direction}.csv"
        meas_df = pd.read_csv(meas_filepath, index_col="Timestamp")

        # get main torso measurements
        if direction == "Transmasc":
            chest = 'chest circumference (post-op or binder)'
        else:
            chest = 'bust circumference (standing/no binder)'
        get_columns = [
            chest,
            'natural waist circumference (REQUIRED)', 
            'hip circumference (REQUIRED)', 
        ]
        if direction == "Transmasc":
            get_columns.append("top surgery")
        meas_df = meas_df.get(get_columns)

        meas_df = meas_df.rename(columns={
            chest: "chest",
            'natural waist circumference (REQUIRED)':"natural waist", 
            'hip circumference (REQUIRED)':"hip", 
        })

        # separate by top surgery/no top surgery
        if direction == "Transmasc":
            meas_df["chest"] = meas_df["chest"].where(meas_df["top surgery"] == "Yes")
                    # we ignore bust measurement of non-op transmascs for now
            meas_df.pop("top surgery")
        
        meas_df = meas_df.dropna(how="any")

        meas_df["biggest"] = meas_df.apply(find_biggest, axis=1)

        df_dict[direction] = meas_df.groupby("biggest").count()["chest"]

    new_df = pd.DataFrame(
        df_dict, columns=["Transmasc","Transfemme"]
    )

    return new_df
