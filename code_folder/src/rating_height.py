import pandas as pd
from code_folder.utils.lookup import separated_files_folder, processed_data_folder
from datetime import datetime

# UTIL
def switch_heights(row):
    """
    if people misunderstood the question and marked that they were taller 
    by amab standards than by afab standards
    switches the two 
    """
    # if they marked afab as taller than amab -> switch em
    if (row["afab"] == "short" and row["amab"] in ["tall", "average"]) or (
        row["afab"] == "average" and row["amab"] == "tall"):
        afab = row["amab"]
        amab = row["afab"]
        row["amab"] = amab
        row["afab"] = afab
    return row

def get_heights_and_compare():
    """
    returns a df with the following columns
    
    - heights - the respondent's height measurement
    - amab - how they rated their height by afab standards
    - afab - how they rated their height by afab standards
    - direction - whether this was a Transmasc or Transfemme respondent

    if any respondents misunderstood the question and rated themselves as taller by amab standards
    than by afab standards (ex amab tall, afab short) -> swaps the values

    returns a df in order of timestamps
    """

    heights_dict = {}

    for direction in ["Transmasc", "Transfemme"]:

        # read in relevant data
        meas_filepath = f"{separated_files_folder}/measurements_in_cm_{direction}.csv"
        meas_df = pd.read_csv(meas_filepath, index_col="Timestamp")

        demo_filepath = f"{separated_files_folder}/demographic_qs_{direction}.csv"
        demo_df = pd.read_csv(demo_filepath, index_col="Timestamp")

        # get heights
        heights = meas_df["height (REQUIRED)"]
        heights_dict[direction] = {
            "heights": heights,
        }

        # get which standards it's about
        for trans_status in ["cis", "trans"]:
            # which birthsex does this describe?
            if (trans_status == "trans" and direction == "Transmasc") or (trans_status == "cis" and direction == "Transfemme"):
                birthsex = "afab"
            else:
                birthsex = "amab"

            # get whether they're tall or short compared to this birthsex
            standards = pd.DataFrame(index=demo_df.index)
            standards["standards"] = "average"
            standards = standards["standards"]
            standards = standards.mask(
                (demo_df["extra tall"] == f"By {trans_status} standards") | (demo_df["extra tall"] == "Both"),
                other = "tall"
            )
            standards = standards.mask(
                (demo_df["extra short"] == f"By {trans_status} standards") | (demo_df["extra short"] == "Both"),
                other = "short"
            )

            # save in dict
            heights_dict[direction][birthsex] = standards

        heights_dict[direction] = pd.DataFrame(heights_dict[direction])

        # some people misunderstood the question & marked it the wrong way around
        heights_dict[direction] = heights_dict[direction].apply(
            switch_heights,
            axis=1
        )

        # mark with direction
        heights_dict[direction]["direction"] = direction

    # combine both directions
    final_df = pd.concat([heights_dict["Transmasc"], heights_dict["Transfemme"]])

    # sort by date & turn back to string format
    final_df.index = final_df.index.to_series().apply(lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S"))
    final_df = final_df.sort_index()
    final_df.index = final_df.index.to_series().apply(lambda x: datetime.strftime(x, "%d/%m/%Y %H:%M:%S"))

    return final_df

if __name__ == "__main__":
    df = get_heights_and_compare()
    df.to_csv(f"{processed_data_folder}/rating_height.csv")