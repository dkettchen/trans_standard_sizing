import pandas as pd
from code_folder.utils.standard_deviation import standard_deviation
from code_folder.utils.lookup import torso_meas, torso_dist

def compare_torso_measurements(row:pd.Series):
    """
    compares the torso measurements of the given row
    
    if the standard deviation of the measurements 
    is less than a fraction of the smallest measurement, 
    returns True
    """
    shorter_row = row.loc[torso_meas]
    if len(shorter_row.dropna()) > 0:
        stan_dev = standard_deviation(list(shorter_row.dropna()))
        fraction = 0.15
        if round(stan_dev/shorter_row.min(), 2) < fraction:
            return True

def compare_torso_distances(row:pd.Series):
    """
    compares the torso distances of the given row
    
    if the standard deviation of the measurements 
    is less than a fraction of the smallest measurement, 
    returns True
    """
    shorter_row = row.loc[torso_dist]
    if len(shorter_row.dropna()) > 0:
        stan_dev = standard_deviation(list(shorter_row.dropna()))
        fraction = 0.4
        if round(stan_dev/shorter_row.min(), 2) < fraction:
            return True

def compare_other_meas(row:pd.Series, col):
    # get the relevant reference column to compare to
    if col in ["shoulder (REQUIRED)", "arm length (REQUIRED)", "armhole height (front)", "head circumference"]:
        ref_col = "height (REQUIRED)"
    elif col == "shoulder to elbow":
        ref_col = "elbow to wrist"
    elif col == "shoulder width (back)":
        ref_col = "back width"
    elif col == "shoulder width (front) (REQUIRED)":
        ref_col = "front width"
    elif col == "clavicle to shoulder point distance":
        ref_col = "shoulder (REQUIRED)"

    elif col == "nipple/bust point distance":
        if "bust circumference (standing/no binder)" in row.dropna().index:
            ref_col = "bust circumference (standing/no binder)" 
            # prioritising non-binder version where available for pre-op transmascs 
            # as binder may put nips in a diff place
        else: 
            ref_col = "chest circumference (post-op or binder)"

    elif col == "nape of the neck to front natural waist":
        # compare the nape to waist measurement to the added length of nape to sternum - sternum to waist
        row["suit_front_combo"] = row["nape of the neck to end of ribcage/sternum"] \
                                + row["end of ribcage/sternum to natural waist"]
        ref_col = "suit_front_combo"
        # -> I guess where people's sternum ends can vary quite significantly

    # if either column is not present, skip
    if col not in row.dropna().index or ref_col not in row.dropna().index:
        return None
    
    # get ratio
    ratio = row[ref_col] / row[col]
    # check for ratio we're looking for
    if (
        col == "shoulder (REQUIRED)" and ratio > 7) or (
        col == "arm length (REQUIRED)" and ratio > 2.6) or (
        col == "armhole height (front)" and ratio > 6 and ratio < 15) or (
        col == "shoulder to elbow" and ratio > 0.5 and ratio < 1) or (
        col == "shoulder width (back)" and ratio > 0.6 and ratio < 1.2) or (
        col == "shoulder width (front) (REQUIRED)" and ratio > 0.5 and ratio < 1.3) or (
        col == "clavicle to shoulder point distance" and ratio > 0.5 and ratio < 1.2) or (
        col == "nipple/bust point distance" and ratio > 3.6) or (
        col == "head circumference" and ratio > 2.5 and ratio < 3.5) or (
        col == "nape of the neck to front natural waist" and ratio > 0.9 and ratio < 1.3
    ):
        return True

    if col == "" and not (ratio > 1 and ratio < 1):
        print(round(ratio, 2), row[ref_col], row[col])
