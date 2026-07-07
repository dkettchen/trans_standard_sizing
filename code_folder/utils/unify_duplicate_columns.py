import pandas as pd
from re import sub

def unify_duplicate_columns(input_df:pd.DataFrame):
    """
    takes a read-in version of the response file data
    
    unifies any columns that had multiple versions due to 
    conditional logic work-around in google forms (ex age group, unit), 
    including relevant chest measurements (ex. underbust)

    for the sake of labelling, we're counting non-op transmasc chests with binder as "chest" measurements, 
    and without binder as a "bust" measurement, to group them by comparable shape and with post-op transmascs 
    and transfemmes respectively

    the various additional transfemme chest measurements remain untouched as they did not have other equivalents

    all columns that were labelled as "(transmasc)" or "(transfemme)" to differentiate
    now have this label removed as there are no more duplicates

    returns a new df (with new columns not in the original order)
    """
    new_df = input_df.copy()

    # unify duplicated columns
    duplicated_columns = [ # columns shared by both transmascs & transfemmes
        "other surgery",
        "standard HRT",
        "non-standard HRT",
        "consistent HRT for 3 years",
        "time on changed dose",
        "total time on HRT",
        "age group",
        "unit",
    ]
    for dup in duplicated_columns:
        # add one column's values to a new one
        new_df[dup] = new_df[dup + " (transmascs)"]
        # add the other columns' values where values are missing
        new_df.loc[new_df[dup + " (transmascs)"].isna(), dup] = new_df[dup + " (transfemmes)"]
        # then remove both old columns
        new_df.pop(dup + " (transmascs)")
        new_df.pop(dup + " (transfemmes)")

    # unify underbust measurements
    underbusts = [
        "underbust circumference (top surgery) (transmascs)",
        "underbust circumference (REQUIRED) (no top surgery) (transmascs)",
        "underbust circumference (loose) (REQUIRED) (transfemmes)"
    ]
    new_df["underbust circumference"] = new_df[underbusts[0]]
    new_df.loc[new_df["underbust circumference"].isna(), "underbust circumference"] = new_df[underbusts[1]]
    new_df.loc[new_df["underbust circumference"].isna(), "underbust circumference"] = new_df[underbusts[2]]
    for u in underbusts:
        new_df.pop(u)
    
    # unify bust/chest measurements
    # I will consider with binder to be the pre-op equivalent of a flat chest -> group w post-op values
    front_chests = [
        "front chest (top surgery) (transmascs)",
        "front bust (with binder) (no top surgery) (transmascs)",
    ]
    chests = [
        "chest circumference (REQUIRED) (top surgery) (transmascs)",
        "bust circumference (with binder) (no top surgery) (transmascs)",
    ]
    # and no binder pre-op to remain a "bust" measurement -> group w the transfemmes' main bust measurement
    busts = [
        "bust circumference (without binder) (no top surgery) (transmascs)",
        "bust circumference (standing) (REQUIRED) (transfemmes)",
    ]
    for measurement in [
        "front chest",
        "chest circumference (post-op or binder)",
        "bust circumference (standing/no binder)",
    ]:
        if measurement == "front chest":
            columns = front_chests
        elif "chest" in measurement:
            columns = chests
        elif "bust" in measurement:
            columns = busts
        
        # same method as before
        new_df[measurement] = new_df[columns[0]]
        new_df.loc[new_df[measurement].isna(), measurement] = new_df[columns[1]]
        for c in columns:
            new_df.pop(c)

    # do crotch volume too!
    # relabel answers to match each other
    new_df["extra crotch volume (transmascs)"] = new_df["extra crotch volume (transmascs)"].mask(
        new_df["extra crotch volume (transmascs)"] == "Yes",
        other="Extra"
    )
    new_df["no crotch volume (transfemmes)"] = new_df["no crotch volume (transfemmes)"].mask(
        new_df["no crotch volume (transfemmes)"] == "No",
        other="Extra"
    )
    new_df["no crotch volume (transfemmes)"] = new_df["no crotch volume (transfemmes)"].mask(
        new_df["no crotch volume (transfemmes)"] == "Yes",
        other="No"
    )
    # combine into one column
    new_df["crotch volume"] = new_df["extra crotch volume (transmascs)"]
    new_df.loc[new_df["crotch volume"].isna(), "crotch volume"] = new_df["no crotch volume (transfemmes)"]
    # remove old columns
    for c in [
        "extra crotch volume (transmascs)",
        "no crotch volume (transfemmes)"
    ]:
        new_df.pop(c)

    # now we can remove the transmasc/transfemme labels as there are no more duplicate columns
    renaming_columns = {}
    for column in new_df.columns:
        if "transmasc" in column:
            renaming_columns[column] = sub(r" \(transmascs\)", "", column)
        elif "transfemme" in column:
            renaming_columns[column] = sub(r" \(transfemmes\)", "", column)
    new_df = new_df.rename(columns=renaming_columns)

    return new_df
