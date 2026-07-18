import pandas as pd

def fix_fixables(input_df:pd.DataFrame):
    """
    if any strange values we found can be fixed 
    (ex. reasonably obvious typos we can make an educated guess about supported by surrounding data 
    & proportional ratios gaged from remaining responses), 
    this function replaces the strange value with the fixed one

    must be run before converting units

    returns new df
    """
    new_df = input_df.copy()

    fixables = [
        ["05/07/2026 18:41:09", "nipple/bust point distance", 25] # likely typo
            # this person put 35 for nip distance, but this would not be remotely close 
            # to the range all other people's distances are in compared to chest/bust circ
                # notably considering that this person both had top surgery 
                # (-> can't be explained by weird binder placement of nips)
                # and didn't indicate ever being plus-size 
                # (-> can't be explained by larger post-op chest)
            # if we assume they just made a typo and meant to put 25, 
            # it would be firmly within the ratio compared to their chest circumference
            # so I'm making the executive decision that they probably made a typo 
            # and we can assume it was meant to be 25
    ]
    # fix each cell listed
    for id, c, v in fixables:
        new_df.loc[id, c] = v

    return new_df
