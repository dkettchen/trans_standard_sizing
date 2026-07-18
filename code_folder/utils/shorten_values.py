import pandas as pd
from re import split, sub

def shorten_values(input_df:pd.DataFrame):
    """
    shortens the values in direction and how did that change columns 
    and fixes any weird apostrophes to normal ones

    returns a new df
    """

    new_df = input_df.copy()

    # make sure 's are correct
    for col in new_df.columns:
        new_df[col] = new_df[col].apply(lambda x: sub(r"’", "'", x) if type(x) == str else x)

    # columns we want to shorten by removing extra bits
    for column in ["direction", "how did that change"]:
        # split at brackets, commas & trailing white spaces
        new_df[column] = new_df[column].apply(lambda x: split(r"[\(,]", x)[0].strip())

    return new_df

