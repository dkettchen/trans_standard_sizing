from code_folder.utils.lookup import separated_files_folder
import pandas as pd
from typing import Literal

def torso_proportions(unit:Literal["cm", "inch"]="cm"):
    """
    gets chest, underbust, natural waist, low waist, and hip circumferences for either direction
    
    returns dict

    optionally you can specify which unit you wanna get the measurements in
    """

    df_list = []

    for direction in ["Transmasc", "Transfemme"]:
        # read in relevant data
        meas_filepath = f"{separated_files_folder}/measurements_in_{unit}_{direction}.csv"
        meas_df = pd.read_csv(meas_filepath, index_col="Timestamp")

        # get main torso measurements
        if direction == "Transmasc":
            chest = 'chest circumference (post-op or binder)'
            meas_df["overbust circumference"] = None
        else:
            chest = 'bust circumference (standing/no binder)'
        get_columns = [
            "overbust circumference",
            chest,
            'underbust circumference',
            'natural waist circumference (REQUIRED)', 
            "high hip/low waist circumference (REQUIRED)",
            'hip circumference (REQUIRED)', 
        ]
        if direction == "Transmasc":
            get_columns.append("top surgery")
        meas_df = meas_df.get(get_columns)

        meas_df = meas_df.rename(columns={
            "overbust circumference":"overbust",
            chest: "chest",
            'underbust circumference':"underbust",
            'natural waist circumference (REQUIRED)':"natural waist", 
            "high hip/low waist circumference (REQUIRED)":"low waist",
            'hip circumference (REQUIRED)':"hip", 
        })

        # separate by top surgery/no top surgery
        if direction == "Transmasc":
            meas_df["chest"] = meas_df["chest"].where(meas_df["top surgery"] == "Yes")
                    # we ignore bust measurement of non-op transmascs for now
            meas_df.pop("top surgery")

        meas_df["direction"] = direction
        df_list.append(meas_df)

    return pd.concat(df_list)
