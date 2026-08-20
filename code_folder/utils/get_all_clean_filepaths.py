from code_folder.lookup import separated_files_folder, clean_gen_pop_folder
from typing import Literal

def get_filepaths(which:Literal["Trans", "Cis", "Both"]="Both", unit:Literal["cm", "inch"]="cm"):
    """
    creates a dict of all the filepaths to the cleaned data files for the requested measurements
    
    by default it assembles all measurement data in cm
    """

    # collect all filepath we wanna read in
    filepath_dict = {}

    # get trans data
    if which in ["Trans", "Both"]:
        for direction in ["Transmasc", "Transfemme"]:
            filepath_dict[direction] = f"{separated_files_folder}/measurements_in_{unit}_{direction}.csv"

    # get cis data we have
    if which in ["Cis", "Both"]:
        for gender in ["male", "female"]:
            # ANSUR data
            for year in [1988, 2012]:
                meas_filepath = f"{clean_gen_pop_folder}/ANSUR_{year}_{gender}.csv"
                filepath_dict[f"ANSUR_{year}_{gender}"] = meas_filepath

    return filepath_dict
