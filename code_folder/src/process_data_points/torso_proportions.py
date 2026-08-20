import pandas as pd
from typing import Literal
from code_folder.utils.get_all_clean_filepaths import get_filepaths
from code_folder.utils.get_torso_get_columns import get_torso_get_columns

def torso_proportions(unit:Literal["cm", "inch"]="cm"):
    """
    gets overbust, chest/bust, underbust, waist, and hip circumferences for all available gender categories

    marks which gender category the data refers to and which study it is from ("Study name (year)")
    
    returns dict

    optionally you can specify which unit you wanna get the measurements in
    """

    # collect all filepath we wanna read in
    filepath_dict = get_filepaths(unit=unit)

    # what order we want the measurements to be output in
    circ_order = [
        # measurements in order
        'overbust', 'bust', 'chest', 'underbust', 'natural waist', 'waist', 'low waist', 'hip', 
        # additional columns
        "gender", "study"
    ]

    df_dict = {}

    for key in filepath_dict:
        # read file
        filepath = filepath_dict[key]
        if "Trans" in key:
            df = pd.read_csv(filepath, index_col="Timestamp")
        else: 
            df = pd.read_csv(filepath)

        # figure out what category's data the file contains
        if "female" in key:
            gender = "Cis woman"
        elif "male" in key:
            gender = "Cis man"
        else:
            gender = key

        if "Trans" in key:
            study = "Trans Standard Sizing (2026)"
        elif "ANSUR" in key:
            study = "ANSUR"
            if "1988" in key:
                study += " (1988)"
            else:
                study += " (2012)"
        else:
            raise ValueError("Study not found, please implement:", key)
        
        if gender not in df_dict:
            df_dict[gender] = []

        # get relevant columns and renaming dict
        renaming_dict = get_torso_get_columns(df, gender)
        desired_cols = list(renaming_dict.keys())

        # we want to be able to check for top surgery to be able to exclude binder measurements
        if gender == "Transmasc":
            desired_cols.append("top surgery")
        
        # get and rename
        df = df.get(desired_cols).rename(columns=renaming_dict)

        if gender == "Transmasc": # exclude binder chest measurements
            df["chest"] = df["chest"].where(df["top surgery"] == "Yes")
            df.pop("top surgery")

        # put in right order
        desired_cols = sorted(list(df.columns), key=lambda x:circ_order.index(x))
        df = df.get(desired_cols)

        # add which gender this data refers to
        df["gender"] = gender
        # add which study this data is from
        df["study"] = study

        # append all data we have for one 
        df_dict[gender].append(df)

    for gender in df_dict:
        df = pd.concat(df_dict[gender])
        desired_cols = sorted(list(df.columns), key=lambda x:circ_order.index(x))
        df_dict[gender] = df.get(desired_cols)

    return df_dict
