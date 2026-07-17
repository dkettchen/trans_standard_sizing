import pandas as pd
from re import sub, split

rename_numbers = {
    0: "direction",

    # transmascs
    1: "extra crotch volume",
    2: "hysterectomy",
    3: "other surgery",
    4: "standard HRT",
    5: "non-standard HRT",
    6: "consistent HRT for 3 years",
    7: "time on changed dose",
    8: "total time on HRT",
    9: "very muscular",
    10: "age group",
    # transfemmes
    11: "breast augmentation",
    12: "breast reduction or mastectomy",
    13: "padded bra",
    14: "no crotch volume",
    15: "other surgery",
    16: "standard HRT",
    17: "non-standard HRT",
    18: "progesterone",
    19: "consistent HRT for 3 years",
    20: "time on changed dose",
    21: "total time on HRT",
    22: "age group",

    # measurements
    # transmascs
    23: "unit",
    24: "top surgery",

    # then there's a bunch of measurements 
    # where we just need to remove the emoji 
    # and make em lowercase for now

    # transfemmes
    38: "unit",

    # measurements continue until 118 (included)

    119: "did you shop in birth sex aisle pre-transition and remember your size(s)",
    120: "sizing system 1",
    121: "write in system 1",
    122: "size 1",
    123: "sizing system 2",
    124: "write in system 2",
    125: "size 2",
    126: "sizing system 3",
    127: "write in system 3",
    128: "size 3",
    129: "plus-size",
    130: "extra tall",
    131: "extra short",
    132: "how well did standard sizing fit pre-transition",
    133: "how did that change",

    # I think we can automatically clean up the common fit issues categories

    145: "other fit issues",
    
    # suggestions just need to be lowercased for now
    # as does survey origin
}

def read_responses_file(csv_filepath:str):
    """
    reads the given csv file (as downloaded from google sheets)

    returns a df with removed superfluous columns, and renamed rest of the columns 
    (they have not yet been unified where there's duplicates)
    """
    # read csv file (as downloaded from google sheets)
        # timestamp will be our index
        # and we do have a header col included
    df = pd.read_csv(csv_filepath, header=0, index_col="Timestamp")

    # drop superfluous "questions" (ex confirmation of consent that everyone had to click to proceed)
    df.pop("Please confirm:")
    df.pop("Please confirm that you fit the requirements to participate in this survey:")

    renaming_columns = {}
    for i, column in enumerate(df.columns):
        if i in rename_numbers:
            new_column = rename_numbers[i]
        elif "What are your most common fit issues with standard sizing" in column:
            # shorten automatically & label by body part
            split_item = [bit for bit in split(r"[\[\]]", column) if len(bit.strip()) > 0][-1].lower()
            split_item = split(r"\(", split_item)[0]
            new_column = "fit issue with " + split_item
        else:
            # make lowercase
            new_column = column.lower().strip()
        
        # remove emojis
        if "📏" in new_column:
            new_column = sub(r"📏 ", "",new_column)
            new_column += " (REQUIRED)"

        # label by direction where there might be duplicates
        if (i >= 1 and i <= 10) or (i >= 23 and i <= 37):
            # also mark transmasc sub section exclusive measurements
            if i >= 25 and i <= 33:
                new_column += " (top surgery)"
            elif i >= 34 and i <= 37:
                new_column += " (no top surgery)"
            new_column += " (transmascs)"
        elif (i >= 11 and i <= 22) or (i >= 38 and i <= 56):
            new_column += " (transfemmes)"

        renaming_columns[column] = new_column

    df = df.rename(columns=renaming_columns)

    return df
