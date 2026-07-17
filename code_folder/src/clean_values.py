# TODO 
# fix values
    # ✅ shorten certain values
    # check for & fix or omit unrealistic measurements
        # I did also put in one measurement incorrectly, so maybe we can hard code in to fix that response here
    # convert all measurements to both units

import pandas as pd
from re import split, sub
from code_folder.utils.standard_deviation import standard_deviation
from typing import Literal
from code_folder.utils.unit_conversion import convert_measurement, opposite_unit

def shorten_values(input_df:pd.DataFrame):
    """
    shortens the values in direction and how did that change columns 
    and fixes any weird apostrophes to normal ones

    returns a new df
    """

    new_df = input_df.copy()

    # make sure 's are correct
    new_df = new_df.apply(lambda x: sub(r"’", "'", x) if type(x) == str else x)

    # columns we want to shorten by removing extra bits
    for column in ["direction", "how did that change"]:
        # split at brackets, commas & trailing white spaces
        new_df[column] = new_df[column].apply(lambda x: split(r"[\(,]", x)[0].strip())

    return new_df


# TODO put these into a separate file bc they're currently just copied from order columns helper

# measurements
chest_meas = [ # chest measurements
    'underbust circumference', 
    'front chest', 
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only

    # post-op transmascss only
    'distance from clavicle to inner end of the scar (top surgery)', 
    'distance between inner ends of your scars (top surgery)', 
    'distance from clavicle to outer end of the scar (top surgery)', 
    'distance between outer ends of your scars (top surgery)', 
    'distance from clavicle to the lowest/bending/middle point of the scar (top surgery)', 
    'distance between lowest/bending/middle points of your scars (top surgery)', 

    # transfemmes only
    'underbust circumference (snug)', 
    'underbust circumference (tight)', 
    'strap length to underbust (front)', 
    'strap length to underbust (back)', 
    'front bust (standing)', 
    'bust circumference (bent over)', 
    'bust circumference (lying down)', 
    'overbust circumference', 
    'clavicle to overbust', 
    'clavicle to nipple/apex', 
    'top cup', 
    'bottom cup', 
    'outer arc', 
    'inner arc', 
    'breast spacing', 
    'bust circumference (padded bra)', 
]
meas = [ # other measurements
    'height (REQUIRED)', 
    'nape of the neck to floor', 
    'head circumference', 
    'neck circumference', 
    'base of neck circumference', 
    'shoulder (REQUIRED)', 
    'arm length (REQUIRED)', 
    'shoulder to elbow', 
    'elbow to wrist', 
    'bicep circumference (REQUIRED)', 
    'elbow circumference', 
    'wrist circumference', 
    'hand circumference', 
    'armhole height (front)', 
    'armhole height (back)', 
    'sleeve cap', 
    'armpit distance', 
    'front width', 
    'back width', 
    'shoulder width (front) (REQUIRED)', 
    'shoulder width (back)', 
    'clavicle to shoulder point distance', 
    'natural waist circumference (REQUIRED)', 
    'front (natural) waist', 
    'distance from clavicle to natural waist (front) (REQUIRED)', 
    'distance from clavicle to natural waist (front, with ruler)', 
    'side seam to natural waist', 
    'nipple/bust point distance', 
    'distance from shoulder to natural waist (front)', 
    'distance from nipple/bust point to natural waist', 
    'distance from underbust to natural waist', 
    'shoulder to natural waist (diagonal, front)', 
    'shoulder to natural waist (diagonal, back)', 
    'distance from nape of the neck to natural waist (back)', 
    'distance from shoulder to natural waist (back)', 
    'nape of the neck to end of ribcage/sternum', 
    'end of ribcage/sternum to natural waist', 
    'nape of the neck to front natural waist', 
    'high hip/low waist circumference (REQUIRED)', 
    'front (low) waist', 
    'natural waist to high hip/low waist distance (front)', 
    'natural waist to high hip distance (side)', 
    'natural waist to high hip distance (back)', 
    'hip circumference (REQUIRED)', 
    'front hip', 
    'natural waist to hip (front)', 
    'natural waist to hip (side)', 
    'natural waist to hip (back)', 
    'fly length (from natural waist)', 
    'rise to natural waist (REQUIRED)', 
    'crotch depth', 
    'outseam from natural waist (side) (REQUIRED)', 
    'outseam from natural waist (front)', 
    'outseam from natural waist (back)', 
    'inseam', 
    'thigh circumference (REQUIRED)', 
    'knee circumference', 
    'calf circumference', 
    'ankle circumference', 
    'foot entry circumference', 
    'knee to floor', 
    'ankle to floor', 
]
min_meas = [ # some selected measurements to gage proportion
    'height (REQUIRED)', 
    'arm length (REQUIRED)', 
    'bicep circumference (REQUIRED)', 
    'shoulder (REQUIRED)', 
    'underbust circumference',
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only
    'front (natural) waist', 
    'natural waist circumference (REQUIRED)', 
    'front (low) waist', 
    "high hip/low waist circumference (REQUIRED)",
    'front hip', 
    'hip circumference (REQUIRED)', 
    'outseam from natural waist (side) (REQUIRED)', 
    'inseam', 
    'thigh circumference (REQUIRED)', 
]

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

def fix_known_human_errors(input_df:pd.DataFrame):
    """
    All responses from our in person pride event stalls 
    were later entered manually into the online survey by yours truly

    We also had some measurements we know we measured wrong by accident

    This function fixes any wrongly-entered responses where correct data was found in our notes 
    and removes known wrongly measured values
    """
    new_df = input_df.copy()

    remove_values = [
        # Sophie measured the wrong measurement for shoulder 
        # (shoulder to shoulder instead of shoulder point to neck)
        ["28/06/2026 12:48:37", ["shoulder (REQUIRED)"]],
        ["28/06/2026 13:16:10", ["shoulder (REQUIRED)"]],

        # I measured to where the top of the bra would be, not the underbust like I was supposed to
        ["28/06/2026 12:20:26", ['strap length to underbust (front)', 'strap length to underbust (back)']],
        ["28/06/2026 13:01:41", ['strap length to underbust (front)', 'strap length to underbust (back)']],
        ["28/06/2026 13:40:45", ['strap length to underbust (front)', 'strap length to underbust (back)']],
    ]

    # # find in person responses & column we know was wrong to get the entry timestamp IDs
    # in_person_values = new_df.where(
    #     new_df['how did you find the survey?'] == "In person event"
    # ).dropna(how="all").get(
    #     ["shoulder (REQUIRED)" ]
    # )
    # print(in_person_values)

    # iterate through all identified rows
    for id, columns in remove_values:
        # and all relevant columns in those rows
        for c in columns:
            # remove value in question
            new_df.loc[id, c] = pd.NA

    return new_df

def fix_fixables(input_df:pd.DataFrame):
    """
    if any strange values we found can be fixed 
    (ex. reasonably obvious typos we can make an educated guess about supported by surrounding data 
    & proportional ratios gaged from remaining responses), 
    this function replaces the strange value with the fixed one

    must be run before converting units

    returns new df
    """
    new_df = input_df.copy()

    fixables = [
        ["05/07/2026 18:41:09", "nipple/bust point distance", 25] # likely typo
            # this person put 35 for nip distance, but this would not be remotely close 
            # to the range all other people's distances are in compared to chest/bust circ
                # notably considering that this person both had top surgery 
                # (-> can't be explained by weird binder placement of nips)
                # and didn't indicate ever being plus-size 
                # (-> can't be explained by larger post-op chest)
            # if we assume they just made a typo and meant to put 25, 
            # it would be firmly within the ratio compared to their chest circumference
            # so I'm making the executive decision that they probably made a typo 
            # and we can assume it was meant to be 25
    ]
    # fix each cell listed
    for id, c, v in fixables:
        new_df.loc[id, c] = v

    return new_df

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

smallest_measurements = [ # only these measurements can be smaller than 5 cm
    "distance between inner ends of your scars (top surgery)",
    "breast spacing",
]
min_max_values = { # in cm
    "hand circumference": [15,40],
    "head circumference": [50,70],
}
half_values = { # key mustn't be significantly smaller or close to value
                # check for <*0.2 to >*0.8
    "front hip": "hip circumference (REQUIRED)",
    "front (low) waist": "high hip/low waist circumference (REQUIRED)",
    "front (natural) waist": "natural waist circumference (REQUIRED)",
}
compared_to_other_meas = { # measurement + num shouldn't be smaller/bigger than other meas * decimal
    "outseam from natural waist (side) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "outseam from natural waist (front) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "outseam from natural waist (back) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "arm length (REQUIRED)": [10, "bigger than", "height (REQUIRED)", 0.5],
    "armpit distance": [0, "bigger than", "bicep circumference (REQUIRED)", 0.8],
    "chest circumference (post-op or binder)": [0, "smaller than", "underbust circumference", 0.8],
    "bust circumference (standing/no binder)": [0, "smaller than", "underbust circumference", 0.8],
}
def check_realistic_min_max_values(input_df:pd.DataFrame):
    """
    remove measurements that are outside a logical realistic range

    returns a new df
    """
    new_df = input_df.copy()

    for col in chest_meas + meas:

        # check any measurements other than smallest aren't too small
        if col not in smallest_measurements:
            # remove if smaller than 5
            new_df[col] = new_df[col].mask(
                new_df[col] < 5
            )

        # check min/max ranges
        if col in min_max_values:
            # remove if smaller than min or bigger than max
            new_df[col] = new_df[col].mask(
                (new_df[col] < min_max_values[col][0]) | (new_df[col] > min_max_values[col][1])
            )

        # check half measurements
        if col in half_values:
            # remove if <*0.2 to >*0.8
            new_df[col] = new_df[col].mask(
                (new_df[col] < new_df[half_values[col]] * 0.2) | (new_df[col] > new_df[half_values[col]] * 0.8)
            )

        # check other comparative measurements
        if col in compared_to_other_meas:
            # measurement + num shouldn't be smaller/bigger than other meas * decimal
            comp_data = compared_to_other_meas[col]

            if comp_data[1] == "smaller than":
                new_df[col] = new_df[col].mask(
                    (new_df[col] + comp_data[0] < new_df[comp_data[2]] * comp_data[3])
                )
            elif comp_data[1] == "bigger than":
                new_df[col] = new_df[col].mask(
                    (new_df[col] + comp_data[0] > new_df[comp_data[2]] * comp_data[3])
                )
    
    return new_df

# refactor TODO
# - ✅ fix decimal places first
# - ✅ then convert all measurements to same unit to have more data together (don't round so we can turn it back later)
# - ✅ get rid of categorically too small or big measurements (based on conditions)
# - ✅ check measurements against each other -> see if they make proportional sense if they're outliers
# - check against standard dev of total
# - if still outliers -> check against plus size standard dev to see if that explains it
# -> see what's left after that

# some of the stan dev flagged main meas we could simply compare to other main meas they're supposed to be close to
# -> do like a standard dev or range around avg of torso measurements & if they all match declare em fine
# also for certain things it might be better to take the standard dev of the ratio between ex height and measurement 
# (ex arm lengths etc) as that will give us a better idea of plausibility
    # might also catch our measuring errors

# UTILS
torso_meas = [ 
    'underbust circumference',
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only
    'natural waist circumference (REQUIRED)', 
    "high hip/low waist circumference (REQUIRED)",
    'hip circumference (REQUIRED)', 
]
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

torso_dist = [ # measurements from shoulder/neck area to natural waist -> should be in similar range
    'distance from clavicle to natural waist (front) (REQUIRED)', 
    'distance from clavicle to natural waist (front, with ruler)', 
    'distance from shoulder to natural waist (front)', 
    'shoulder to natural waist (diagonal, front)', 
    'shoulder to natural waist (diagonal, back)', 
    'distance from nape of the neck to natural waist (back)', 
    'distance from shoulder to natural waist (back)', 
]
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

# TODO WIP
def check_against_standard_dev(input_df:pd.DataFrame):
    new_df = input_df.copy()

    # check by direction
    for direction in ["Transmasc", "Transfemme"]:
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

                        # print what was found
                        # print("⭕ removing:", value, col, list(outlier_responses.index))
                            # currently removing:
                            # Transmasc
                            # ⭕ removing: 36.0 clavicle to shoulder point distance ['05/07/2026 18:41:09']
                            # Transfemme
                            # ⭕ removing: 45.72 shoulder (REQUIRED) ['28/06/2026 00:43:40']
                            # ⭕ removing: 78.74 arm length (REQUIRED) ['28/06/2026 00:43:40']

                        # remove any values that aren't realistic
                        new_df[col] = new_df[col].mask(
                            (new_df[col] == value) & (new_df["direction"] == direction)
                        )



                ## repeat calculations now that outliers were removed
                # to display averages n stuff

                # find standard deviation
                stan_dev = standard_deviation(list(new_df[col].where(new_df["direction"] == direction).dropna()))
                # find average
                col_avg = round(new_df[col].where(new_df["direction"] == direction).mean(), 2)

                if col in [
                    "chest circumference (post-op or binder)",
                    "bust circumference (standing/no binder)",
                    "height (REQUIRED)",
                    "natural waist circumference (REQUIRED)",
                    "hip circumference (REQUIRED)",
                ]:
                    in_avg = round(convert_measurement(col_avg, "cm"),2)
                    if col == "height (REQUIRED)":
                        inches = round(in_avg % 12,2)
                        feet = round(in_avg / 12)
                        in_avg = f"{feet}'" + f'{inches}"'
                    else: 
                        in_avg = f'{in_avg}"'

                    print(stan_dev, " - ", f"{col_avg} cm / {in_avg} for", col, direction)

            # else: # otherwise mark that there were no values found
                # print("No values found for:", col, "in", direction)

    # TODO make sure we actually fixed the values
    return new_df