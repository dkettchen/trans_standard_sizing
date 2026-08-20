from code_folder.lookup import gen_pop_folder, clean_gen_pop_folder
import pandas as pd
from code_folder.utils.detect_encoding import detect_encoding
from code_folder.src.parsing_gen_pop_data.column_lookup import ANSUR_I, ANSUR_II

# ansur raw filepaths
ANSUR = {
    1988: {
        "female":f"{gen_pop_folder}/ANSUR/ansurWomen.csv",
        "male":f"{gen_pop_folder}/ANSUR/ansurMen.csv",
    },
    2012: {
        "female":f"{gen_pop_folder}/ANSUR/ANSUR_II_FEMALE_Public.csv",
        "male":f"{gen_pop_folder}/ANSUR/ANSUR_II_MALE_Public.csv",
    }
}
"""
A nested dict of filepaths to our copies of the ANSUR files, labelled by year and gender

ANSUR is a survey of US military personnel in 1988 and 2012.
ANSUR II (2012) includes reservists, while the first one didn't. ANSUR I is used for various standards.

I am mostly happy for these because they have a number of measurements and 
I was able to download them for free from this website:
https://www.openlab.psu.edu/data/

This is military personnel, so I assume the bodytype and age range is limited by that, 
but we are looking at generalised proportions to compare to, so hopefully it'll do well enough for that.
"""

def clean_ANSUR():
    """
    - reads in ansur files
    - retrieves relevant columns we can compare to our own measurement data
    - relabels the columns
    - turns all measurements into cm (and kg for weight)
    - saves the result to a new csv file each in the clean_gen_pop_folder,
    labelled by the survey name (ANSUR), year, and gender (ex. ANSUR_2012_male.csv)
    """

    for year in ANSUR:
        # get relevant columns reference
        if year == 1988:
            ref = ANSUR_I
        elif year == 2012:
            ref = ANSUR_II
        
        renaming_dict = ref["renaming_dict"]

        for gender in ANSUR[year]:
            filepath = ANSUR[year][gender]

            # read in file
            df = pd.read_csv(filepath, encoding=detect_encoding(filepath), encoding_errors="replace")

            # prevent column differences catching
            if year == 2012 and gender == "female":
                new_cols = [c.lower() if c not in ["Age"] else c for c in df.columns]
                df.columns = new_cols

            # get only the columns we're interested in
            df = df.get(list(renaming_dict.keys()))
            # rename them
            df = df.rename(columns=renaming_dict)

            # set subject ID as index
            df = df.set_index("UID")

            # turn measurements into cm and kg
            for col in df.columns:
                if col not in ["age"]:
                    df[col] = df[col] / 10

            # print to a new file
            df.to_csv(f"{clean_gen_pop_folder}/ANSUR_{year}_{gender}.csv", index=False)

if __name__ == "__main__":
    clean_ANSUR()