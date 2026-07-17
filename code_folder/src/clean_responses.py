from code_folder.src.clean_columns import run_clean_columns

from code_folder.src.clean_values import (
    shorten_values, fix_decimal_places, convert_unit_to, 
    check_realistic_min_max_values, check_against_standard_dev,
    fix_known_human_errors, fix_fixables
)


# temp file while we wait for full data
response_file = "code_folder/files/responses_6_july_2026.csv"

# read in and clean the columns
data = run_clean_columns(response_file)

# save cleaned/unified columns version without actually changing any values yet
data.to_csv("code_folder/files/responses_cleaned_columns.csv")

# then we clean the values
data = shorten_values(data)
data = fix_decimal_places(data, False)
data = fix_known_human_errors(data)
data = fix_fixables(data)
data = convert_unit_to(data, "cm")
data = check_realistic_min_max_values(data)
data = check_against_standard_dev(data)

data.to_csv("code_folder/files/responses_cleaned_columns_and_values_in_cm.csv")

# TODO 
# make clean files
    # we wanna make one big file with cleaned raw responses
        # make one as is & 2 with each unit
    # and then multiple files separating by 
        # - sections: 
            # base demo questions
            # measurements
                # -> convert to both units to compare easier
                # make 2 files -> one in cm, one in inches! so ppl can pick which they wanna look at/work with
                    # -> it would prolly be good to make full files in both too
            # standard sizing questions
        # - directions
            # put top surgery yes or no column at front

