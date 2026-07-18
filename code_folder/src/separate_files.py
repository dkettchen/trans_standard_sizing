import pandas as pd
from code_folder.utils.lookup import (
    cm_full_file, inch_full_file, 
    meas, chest_meas, 
    med_qs, body_qs, standard_sizing_qs, fit_issues,
    separated_files_folder
)

# read in both inch & cm files
for unit in ["cm", "inch"]:
    if unit == "cm":
        filepath = cm_full_file
    else:
        filepath = inch_full_file
    file_data = pd.read_csv(filepath, index_col="Timestamp")

    if unit == "cm":
        # get everyone's survey origin as it doesn't neatly fit into other categories
        survey_origin_srs = file_data["how did you find the survey?"]

        # write to a file
        survey_origin_file = f"{separated_files_folder}/survey_origin.csv"
        survey_origin_srs.to_csv(survey_origin_file, index=True)

    # separate by direction
    for direction in ["Transmasc", "Transfemme"]:
        dir_df = file_data.where(file_data["direction"] == direction).dropna(how="all")

        if unit == "cm": # we only need to do this for one unit, as it's the same data for both
            # separate out demo questions
            demo_df = dir_df.get(med_qs + body_qs)
            # remove empty columns (only used by other direction)
            demo_df = demo_df.dropna(how="all", axis=1)
            # write to file
            demo_file = f"{separated_files_folder}/demographic_qs_{direction}.csv"
            demo_df.to_csv(demo_file, index=True)

            # separate out standard sizing questions
            standard_sizing_df = dir_df.get(standard_sizing_qs + fit_issues + ['suggestions'])
            # remove empty columns (only used by other direction)
            standard_sizing_df = standard_sizing_df.dropna(how="all", axis=1)
            # write to file
            stan_size_file = f"{separated_files_folder}/standard_sizing_qs_{direction}.csv"
            standard_sizing_df.to_csv(stan_size_file, index=True)

        # separate out measurements for each unit + direction
        additional_columns = ["unit"]
        if direction == "Transmasc":
            additional_columns += ["top surgery"]
        meas_df = dir_df.get(additional_columns + chest_meas + meas)
        # remove empty columns (only used by other direction)
        meas_df = meas_df.dropna(how="all", axis=1)
        # write to file
        meas_file = f"{separated_files_folder}/measurements_in_{unit}_{direction}.csv"
        meas_df.to_csv(meas_file, index=True)


