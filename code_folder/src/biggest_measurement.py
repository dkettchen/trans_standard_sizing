import pandas as pd
from typing import Literal
from code_folder.utils.lookup import processed_data_folder, gender_categories

# UTILS
def find_biggest(row:pd.Series):
    """find the biggest measurement out of chest, waist, and hip
    
    if two measurements were tied for biggest, it'll return both (ie "chest and hip")
    """
    chest = row["chest"]
    waist = row["waist"]
    hip = row["hip"]
    if chest > waist and chest > hip:
        return "chest"
    if waist > chest and waist > hip:
        return "waist"
    if hip > chest and hip > waist:
        return "hip"
    if hip == chest and hip > waist:
        return "chest and hip"
    if hip == waist and hip > chest:
        return "waist and hip"
    if chest == waist and chest > hip:
        return "chest and waist"
    else: # if I guess all measurements were equal??
        print("What on earth are these measurements if we can't find the biggest?",chest, waist, hip)

def biggest_measurement(unit:Literal["cm", "inch"]="cm"):
    """
    returns a df

    columns are biggest and the 4 gender categories (cis men & women & transmascs & transfemmes)

    biggest is the different measurements (chest, waist, hip)
    - chest is "flat" chest for men and transmascs (i.e. excluding pre-op transmascs' bust/chest measurements)
    and bust for women and transfemmes
    - waist is natural waist where available or unspecified single waist measurement

    the values are the % of the people of the relevant category for whom that measurement was the biggest out of the three
    """

    df_dict = {}

    for gender in gender_categories:
        # read in the data we already prepared for torso proportions
        filepath = f"{processed_data_folder}/torso_proportions_{gender}.csv"
        meas_df = pd.read_csv(filepath)

        # get main torso measurements
        if gender in ["Transmasc", "Cis man"]:
            chest = 'chest'
        else:
            chest = 'bust'
        # replace pre-op transmascs' chest measurements with underbusts adjusted for usual diff to chest
        if gender == "Transmasc":
            # get all post-op respondants who also gave an underbust
            post_op = meas_df.get(["chest", "underbust"]).dropna(how="any")
            post_op["ratio"] = post_op["chest"] / post_op["underbust"]
            ratio = post_op["ratio"].mean() # -> ratio of underbust to chest

            # replace any NA values with projected/estimated chest measurement
            meas_df["chest"] = meas_df["chest"].mask(meas_df["chest"].isna(), other=meas_df["underbust"] * ratio)

        # use natural waist where available, otherwise use unspecified waist
        if "natural waist" in meas_df.columns and "waist" in meas_df.columns:
            meas_df["waist"] = meas_df["waist"].mask(meas_df["waist"].isna(), other=meas_df["natural waist"])
        elif "natural waist" in meas_df.columns:
            meas_df = meas_df.rename(columns={"natural waist":"waist"})

        # get the columns we want
        meas_df = meas_df.get([chest, 'waist', 'hip',]).dropna(how="any")

        # rename columns
        meas_df.columns = ["chest", "waist", "hip"]

        # find which measurement is biggest
        meas_df["biggest"] = meas_df.apply(find_biggest, axis=1)

        # count them & save for each gender
        df_dict[gender] = meas_df.groupby("biggest").count()["chest"]

    # combine into one df
    new_df = pd.DataFrame(
        df_dict, columns=gender_categories
    )

    # make into percent
    for col in new_df.columns:
        col_total = new_df[col].sum()
        new_df[col] = new_df[col].apply(lambda x: round((x / col_total) * 100, 2))

    return new_df
