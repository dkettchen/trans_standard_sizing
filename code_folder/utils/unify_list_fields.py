import pandas as pd
from code_folder.utils.make_list import make_list

def unify_list_fields(input_df:pd.DataFrame):
    """
    makes the sizing systems/sizes, 
    and suggestions into list values instead of multiple columns

    for multiple choice questions with two options, 
    replaces any responses that selected both with "Both"

    """
    new_df = input_df.copy()

    ## sizing systems & sizes given
    # add sizing systems where write-in
    for i in range(1,4): # 1,2,3
        new_df.loc[new_df[f"sizing system {i}"] == "A sizing system not listed here", f"sizing system {i}"] \
            = new_df[f"write in system {i}"].apply(lambda x: "Other system: " + x if type(x) == str else x)
    # make a list of tuples/lists w system-size
    new_df["pre-transition sizes"] = new_df.apply(make_list, args=["sizing"], axis=1)
    # remove now-redundant columns
    for i in range(1,4):
        for item in [
            f"sizing system {i}",
            f"write in system {i}",
            f"size {i}",
        ]:
            new_df.pop(item)

    ## multiple choice
    # for multiple choice options, if someone ticked both options
    # it puts them as a comma-separated list string 
    # -> for those that only had two options, replace that with "Both"
    for column in ["plus-size", "extra tall", "extra short"]:
        new_df[column] = new_df[column].apply(lambda x : "Both" if type(x) == str and "," in x else x)
    
    # unify if no columns into their y/n column
    for col_1, col_2 in [
        ('standard HRT', 'non-standard HRT'),
        ("consistent HRT for 3 years", 'time on changed dose')
    ]:
        new_df.loc[new_df[col_1] == "No", col_1] = new_df[col_2].apply(lambda x: "No, " + x if type(x) == str else x)
        new_df.pop(col_2)

    # suggestions should be a list too
    new_df["suggestions"] = new_df.apply(make_list, args=["suggestions"], axis=1)
    for i in range(1,4):
        new_df.pop(f"suggestion {i}")
    
    return new_df
