import pandas as pd
from re import split, sub

def shorten_values(input_df:pd.DataFrame):
    """
    shortens the values in direction and how did that change columns 
    and fixes any weird apostrophes to normal ones

    returns a new df
    """

    new_df = input_df.copy()
    
    fit_issues_renaming_dict = {
        "too little / small / narrow / tight / short": "too small",
        "too much / big / wide / loose / long": "too big",
    }

    # make sure 's are correct
    for col in new_df.columns:
        new_df[col] = new_df[col].apply(lambda x: sub(r"’", "'", x) if type(x) == str else x)

        if "fit issue" in col.lower(): # shorten the fit issues big/small responses
            new_df[col] = new_df[col].apply(
                lambda x: fit_issues_renaming_dict[x] if x in fit_issues_renaming_dict else x
            )

    # columns we want to shorten by removing extra bits
    for column in ["direction", "how did that change"]:
        # split at brackets, commas & trailing white spaces
        new_df[column] = new_df[column].apply(lambda x: split(r"[\(,]", x)[0].strip())

    # shorten these responses
    how_well_did_it_fit_renaming_dict = {
        'Very well, I could easily find clothes off-the-rack that fit me in most shops': "Very well", 
        'Somewhat well, I could usually find clothes off-the-rack, but experienced certain fit issues (ex. wrong length, ex. wrong circumference, etc)': "Somewhat well, but fit issues", 
        'Poorly, so I had to use specialist shops/sections (plus-size, extra tall, etc), but still experienced certain fit issues there (ex. wrong length, ex. wrong circumference, etc)': "Poorly, fit issues in special sections", 
        'Poorly, so I had to use specialist shops/sections (plus-size, extra tall, etc), but could easily find clothes there': "Poorly, special sections", 
        "Poorly, so I would have had to use specialist shops/sections (plus-size, extra tall, etc), but I didn't (very often; ex. because they weren't available to me).": "Poorly, didn't access special sections",
        'Very poorly, I have never had properly fitting clothes/I needed custom tailoring to have any clothes that fit correctly': "Very poorly", 
        "Not applicable (ex. I didn't shop in birth sex aisle, I only wore homemade clothes, etc)": "N/A", 
    }
    new_df["how well did standard sizing fit pre-transition"] = new_df["how well did standard sizing fit pre-transition"].apply(
        lambda x: how_well_did_it_fit_renaming_dict[x] if x in how_well_did_it_fit_renaming_dict else x
    )

    return new_df

