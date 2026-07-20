from code_folder.utils.lookup import separated_files_folder
import pandas as pd

def crotch_volume():
    """
    counts how many transmasc & transfemme respondants indicated that they usually have more or less crotch volume
    """

    crotch_dict = {}

    for direction in ["Transmasc", "Transfemme"]:

        # read in relevant data
        demo_filepath = f"{separated_files_folder}/demographic_qs_{direction}.csv"
        demo_df = pd.read_csv(demo_filepath, index_col="Timestamp")

        # get relevant col
        count = demo_df.reset_index().groupby("crotch volume").count()["Timestamp"]

        crotch_dict[direction] = count

    return pd.DataFrame(crotch_dict)