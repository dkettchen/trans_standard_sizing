import pandas as pd

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
