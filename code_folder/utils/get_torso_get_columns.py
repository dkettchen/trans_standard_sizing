from typing import Literal
import pandas as pd

def get_torso_get_columns(df:pd.DataFrame, gender:Literal["Transmasc", "Transfemme", "Cis woman", "Cis man"]):
    """
    goes through given df's columns and creates a renaming dict with 
    all the torso circumference columns available 
    and the simplified name to rename them to

    looks for the following types of columns:
    - overbust
    - bust for cis women and transfemmes
    - chest for cis men and transmasc
    - natural waist
    - low waist
    - waist if it wasn't specified which one it is
    - hip

    returns a renaming dict with original column name keys and simplified column name values

    it contains any columns from the above list that were found
    """
    desired_cols = {}
    found_waist = False
    for c in df.columns:
        col = c.lower()

        # exclude other measurements that mention the one we're looking for
        if "front" in col or "snug" in col or "tight" in col \
        or "bent over" in col or "lying" in col or "padded bra" in col:
            continue

        if "overbust circumference" in col or col == "overbust":
            desired_cols[c] = "overbust"
        elif "chest circumference" in col:
            # if it was labelled the same for cis men and women
            if gender in ["Cis man", "Transmasc"]:
                desired_cols[c] = "chest"
            else: desired_cols[c] = "bust"
        elif "bust circumference" in col and "underbust" not in col and "overbust" not in col:
            # we don't need the bust measurement for the pre-op transmasc
            if gender == "Transmasc":
                continue
            # if it was labelled the same for cis men and women
            if gender in ["Cis man"]:
                desired_cols[c] = "chest"
            else: desired_cols[c] = "bust"
        elif "underbust circumference" in col or col == "underbust":
            desired_cols[c] = "underbust"
        elif "waist circumference" in col and "natural" in col:
            found_waist = True
            desired_cols[c] = "natural waist"
        elif "waist circumference" in col and ("low" in col or "high hip" in col):
            found_waist = True
            desired_cols[c] = "low waist"
        elif "hip circumference" in col:
            desired_cols[c] = "hip"
    
    # if they didn't differentiate/specify which waist they measured
    if not found_waist and "waist circumference" in df.columns:
        desired_cols["waist circumference"] = "waist"

    return desired_cols
