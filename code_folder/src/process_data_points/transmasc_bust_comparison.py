# - compare transmasc bust, binder & projected chest measurements where they were provided
    # -> how far are binder & projected chest apart?
        # -> maybe we could use that to inform how much ease we put into our transmasc standard sized tops 
        # so ppl can wear em over their binder too but it still won't look strange on someone post-op
        # -> similar to what I'm planning w transfemme crotch space

import pandas as pd
from typing import Literal
from code_folder.lookup import separated_files_folder, processed_data_folder

def bust_comparison(unit:Literal["cm", "inch"]="cm"):
    """
    retrieves transmasc chest measurements (chest, binder, bust, underbust)

    prints them to two files:
    - chest_measurements_in_{unit}_Transmasc.csv : full responses of individual people's measurements, 
    chest & binder have been separated, includes top surgery column
    - chest_ratios_and_averages_in_{unit}_Transmasc.csv : ratio to underbust, 
    average and total for each column's responses
    """
    # read in transmasc measurements data
    df = pd.read_csv(f"{separated_files_folder}/measurements_in_{unit}_Transmasc.csv")

    chest_meas_df = df.get([
        "top surgery",
        "underbust circumference",
        "chest circumference (post-op or binder)",
        "bust circumference (standing/no binder)"
    ]).rename(
        columns={
            "underbust circumference":"underbust",
            "chest circumference (post-op or binder)":"chest",
            "bust circumference (standing/no binder)":"bust"
        }
    )

    sorting_order = ["top surgery","underbust","chest","binder","bust",]

    # separate chest column between surgery status
    chest_meas_df["binder"] = chest_meas_df["chest"].where(chest_meas_df["top surgery"] == "No")
    chest_meas_df["chest"] = chest_meas_df["chest"].where(chest_meas_df["top surgery"] == "Yes")
    #sort
    chest_meas_df = chest_meas_df.get(sorted(chest_meas_df.columns, key=lambda x: sorting_order.index(x)))
    # save full data to a file
    chest_meas_df.to_csv(f"{processed_data_folder}/chest_measurements_in_{unit}_Transmasc.csv")
    # remove top surgery column
    chest_meas_df.pop("top surgery")

    values = {
        "ratio_to_underbust": {},
        "average": {},
        "total": {}
    }

    # calculate ratios
    for col in chest_meas_df.columns:
        # get total & average for each column
        values["average"][col] = round(float(chest_meas_df[col].mean()),2)
        values["total"][col] = len(chest_meas_df[col].dropna(how="all"))

        if col == "underbust": # no ratios for underbust
            continue

        # get ratio to underbust
        chest_meas_df[f"{col}_ratio"] = chest_meas_df[col] / chest_meas_df["underbust"]
        values["ratio_to_underbust"][col] = round(float(chest_meas_df[f"{col}_ratio"].mean()),2)

    # make df & sort
    new_df = pd.DataFrame(values).sort_values("average")

    # save to file
    new_df.to_csv(f"{processed_data_folder}/chest_ratios_and_averages_in_{unit}_Transmasc.csv")

