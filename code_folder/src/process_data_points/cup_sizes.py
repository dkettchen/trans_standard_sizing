import pandas as pd
from re import split
from code_folder.utils.get_all_clean_filepaths import get_filepaths
from code_folder.utils.convert_unit import convert_measurement
from string import ascii_uppercase

# TODO test!
def calculate_cup(row:pd.Series):
    """
    takes a row with "bust" and "underbust" values in inches
    
    returns the calculated cup size in letter size
    """
    difference = row["bust"] - row["underbust"]

    counter = 0.5

    if difference <= counter:
        return "AA"
    
    for letter in ascii_uppercase:
        if difference > counter and difference <= counter + 1:
            return letter
        counter += 1


def cup_sizes(unit = "inch"):
    """calculate cup sizes for transfemmes & cis women"""

    filepaths = get_filepaths("Both", unit)
    for key in filepaths:
        if "fem" not in key:
            continue
        filepath = filepaths[key]
        df = pd.read_csv(filepath)

        chest_columns = [col for col in df.columns if "bust" in col or "chest" in col]
        underbust_found = False
        for c in chest_columns:
            if "underbust" in c:
                underbust_found = True
        if not underbust_found:
            continue

        get_rename_dict = {}
        for c in chest_columns:
            if "distance" in c or "strap" in c or "over" in c or "lying" in c or "clavicle" in c \
            or "padded" in c or "nipple" in c or "snug" in c or "tight" in c or "front" in c:
                continue
            if "underbust" in c:
                get_rename_dict[c] = "underbust"
            else:
                get_rename_dict[c] = "bust"

        # unpack key info
        if "Trans" in key:
            df = df.set_index("Timestamp")
            study = "The Trans Standard Sizing Project"
            year = 2026
            gender = key
        elif "ANSUR" in key:
            split_ansur = split(r"[_\.]", key)
            study = split_ansur[0]
            year = int(split_ansur[1])
            gender = split_ansur[2]
        else:
            raise ValueError(f"Data parsing not implemented yet for: {key}")

        relevant_columns = df.get(get_rename_dict.keys()).rename(columns=get_rename_dict).dropna(how="any")

        # turn measurements into inches if we didn't already save them like that
        if unit == "inch" and study == "ANSUR":
            for col in relevant_columns:
                relevant_columns[col] = relevant_columns[col].apply(convert_measurement, args=["cm"])
        
        # calculate their cup sizes
        relevant_columns["cup_size"] = relevant_columns.apply(calculate_cup, axis=1)

        total = len(relevant_columns)

        percentages = relevant_columns.groupby("cup_size").count().apply(lambda x: round((x/total) *100,2))["bust"]

        # ok I'm calling bs on the 80s data bc there is no way that DDs/Es 
        # are the most common cup size among the military women when supposedly B-D is the normal average smh
            # the more recent ansur data doesn't have underbust, so I will need to find other data rippppp
            # investigate if NHANES has it & if so how to use NHANES data properly
            # otherwise find more data rip
        print(percentages)



