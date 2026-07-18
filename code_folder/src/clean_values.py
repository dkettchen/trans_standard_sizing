import pandas as pd
from code_folder.utils.shorten_values import shorten_values
from code_folder.utils.fix_decimal_places import fix_decimal_places
from code_folder.utils.fix_human_error import fix_known_human_errors
from code_folder.utils.fix_fixables import fix_fixables
from code_folder.utils.convert_unit import convert_unit_to
from code_folder.utils.check_realistic_min_max_values import check_realistic_min_max_values
from code_folder.utils.check_against_standard_dev import check_against_standard_dev

def run_clean_values(input_df:pd.DataFrame):
    """
    takes a df of response data with cleaned columns

    cleans values by shortening some of them, and fixing (ex. if the person obviously messed up the decimal place) 
    or omitting (ex. if it's unrealistic in proportion to other measurements hence unusable) unrealistic measurements
    
    returns a new df
    """
    data = input_df.copy()

    # then we clean the values
    data = shorten_values(data)
    data = fix_decimal_places(data, False)
    data = fix_known_human_errors(data)
    data = fix_fixables(data)
    data = convert_unit_to(data, "cm")
    data = check_realistic_min_max_values(data)
    data = check_against_standard_dev(data)

    return data

# TODO test that these are doing what we want them to -> check data output