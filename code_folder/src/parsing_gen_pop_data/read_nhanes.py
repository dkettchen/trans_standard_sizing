"""
find raw files on this website: https://wwwn.cdc.gov/nchs/nhanes/default.aspx (1999-2026!)
    - there are also older studies on there w different coverage I'm guessing
    - I've got files for 2013-2023 for now -> clean & format those for now

- we want the examination ones and then check for some measurements to find the relevant section
- they have documentation on there 
- there are also tutorials abt how to use this dataset bc they're like weighted:
    - https://wwwn.cdc.gov/nchs/nhanes/analyticguidelines.aspx
    - https://wwwn.cdc.gov/nchs/nhanes/QualityAnalysesGuidelines.aspx

OK SO:
this file cleans the raw data
- adds demo data to measurements
- excludes minors
- excludes pregnant folks (as their waist measurement would be impacted)
- labels gender column (as original just has numbers)
- relabels age to be our age groups
- gets only relevant columns:
    - Gender
    - Age
    - measurements including where present:
        - weight
        - head circumference
        - standing height
        - upper leg length
        - upper arm length
        - arm circumference
        - waist circumference
        - hip circumference (only included in recent years apparently)
-> separates the result by gender & saves to gen_pop_data_clean folder under NHANES_{year-year}_{male/female}.csv
"""

import os
import pandas as pd
from code_folder.lookup import gen_pop_folder, clean_gen_pop_folder

# retrieve all files from folder

RAW_NHANES_FOLDER = f"{gen_pop_folder}/NHANES"

folders = [f"{RAW_NHANES_FOLDER}/{f}" for f in os.listdir(RAW_NHANES_FOLDER) if "." not in f and "documentation" not in f]

paths = {}

for folder in folders:
    # get years from path
    start_year = int(folder[-9:-5])
    end_year = int(folder[-4:])
    paths[start_year] = {}

    # get all files
    files = [f"{folder}/{file}" for file in os.listdir(folder)]

    # identify which file is which
    for filepath in files:
        if "DEMO" in filepath:
            if "legend" in filepath:
                paths[start_year]["DEMO_legend"] = filepath
            else:
                paths[start_year]["DEMO_data"] = filepath
        elif "legend" in filepath:
            paths[start_year]["BODY_MEAS_legend"] = filepath
        else:
            paths[start_year]["BODY_MEAS_data"] = filepath

    # format actual data
    data_collection = {}
    for data in ["DEMO", "BODY_MEAS"]:

        ## prepare legend data
        # read in the respective legend for which column is what
        legend = pd.read_csv(paths[start_year][f"{data}_legend"], index_col=0, header=None)

        # rename columns
        renaming_dict = {
            1: "CODE",
            # 2: "TYPE",
            # 3: "NUMBER",
            legend.columns[-1] : "DESCRIPTION"
        }
        legend = legend.rename(columns=renaming_dict)
        # retrieve only code & its description
        legend = legend.get(["CODE", "DESCRIPTION"])
        # set code as index
        legend = legend.set_index("CODE")

        # turn into a dict
        legend_dict = legend.to_dict()

        ## then read in data
        df = pd.read_csv(paths[start_year][f"{data}_data"])
        df = df.rename(columns=legend_dict["DESCRIPTION"])

        ## rename and sort by demo data
        if data == "DEMO":
            get_columns = [
                'Respondent sequence number', 'Data release cycle',
                'Interview/Examination status', 'Gender', 'Age in years at screening',
                'Race/Hispanic origin',
                'Race/Hispanic origin w/ NH Asian',
                'Country of birth',
                'Pregnancy status at exam',
                'Full sample 2-year interview weight',
                'Full sample 2-year MEC exam weight', 'Masked variance pseudo-stratum',
                'Masked variance pseudo-PSU', 'Ratio of family income to poverty'
            ]

            min_get_columns = [
                'Respondent sequence number', 
                'Gender', 
                'Age in years at screening',
                'Pregnancy status at exam',
            ]

            df = df.get(min_get_columns)

            # check which number is which gender
            # df["Pregnancy status at exam"] = df["Pregnancy status at exam"].apply(lambda x: None if x == 0 else x)
            # who_be_pregnant = df.groupby("Gender").count()["Pregnancy status at exam"]
            # # women seem to be number 2 in all of them

            # translate gender number to readable marker
            df["Gender"] = df["Gender"].apply(lambda x : "F" if x == 2 else "M" if x == 1 else "?")

            # fix age info to match ours
            df = df.rename(columns={"Age in years at screening": "Age"})

            # exclude minors
            df = df.where(df["Age"] >= 18).dropna(how="all")
                # all the ? genders seem to be some kind of strange value in both respondent number & age column
                # 3.687825e-40 -> so it ends up excluding them here with the minors
                # -> presumably not nbs then
            # assign age ranges
            def get_age_group(age:float|int):
                """returns age group string based on which one age falls into"""
                # these values should've already been excluded but just to make sure
                if age < 18:
                    return None
                
                # find correct age group
                if age <= 29:
                    return "18-29"
                if age <= 39:
                    return "30-39"
                if age <= 49:
                    return "40-49"
                if age <= 59:
                    return "50-59"
                if age >= 60:
                    return "60+"
            df["Age"] = df["Age"].apply(get_age_group)

            # exclude pregnant folks, bc it'll mess up their measurements for our purposes
            df = df.where(df["Pregnancy status at exam"] == 0).dropna(how="all")
            df.pop("Pregnancy status at exam")

        ## set respondent number as index
        df = df.set_index("Respondent sequence number")

        data_collection[data] = df

    # join demo data to measurements
    data_df = data_collection["DEMO"].join(data_collection["BODY_MEAS"]).drop_duplicates()

    # isolate relevant measurements
    get_columns = [
        c for c in data_df.columns if c not in [
            'Body Measures Component Status Code',
        ] and "Comment" not in c and "Recumbent" not in c and "BMI" not in c and "Body Mass Index" not in c \
        and "Sagittal Abdominal Diameter" not in c
        # Sagittal Abdominal Diameter is how big ur belly is like measured from the back to the front, depth, not circ
        # -> could be useful but we don't have an equivalent measurement to compare it to in our data
    ]
    # we seem to have height & weight data, as well as some partial arm & leg lengths, 
    # arm circ & waist circ (unspecified), and only in recent years hip circ 
    # -> no chest measurements rip
    data_df = data_df.get(get_columns)
    data_df = data_df.dropna(how="any") # remove empty measurement responses

    for gender in ["female", "male"]:
        # separate by gender
        gender_df = data_df.where(data_df["Gender"] == gender[0].upper()).dropna(how="all")

        # save data
        gender_df.to_csv(f"{clean_gen_pop_folder}/NHANES_{start_year}-{end_year}_{gender}.csv")





