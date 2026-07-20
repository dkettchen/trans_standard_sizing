from code_folder.src.clean_columns import run_clean_columns
from code_folder.src.clean_values import run_clean_values
from code_folder.utils.print_averages import print_averages
from code_folder.utils.convert_unit import convert_unit_to
from code_folder.utils.lookup import response_file, clean_columns_file, cm_full_file, inch_full_file

print_what_outliers_were_removed = False

"""
cleans raw response data (ex. shorten, unify and reorder columns, omit or fix unrealistic values)
and saves to new files
"""

# read in and clean the columns
data = run_clean_columns(response_file)

# save cleaned/unified columns version without actually changing any values yet
data.to_csv(clean_columns_file)

# then we clean the values
data = run_clean_values(data, print_what_outliers_were_removed)
# print_averages(data) # to verify/sneak peak

# save to file in cm and inches
data.to_csv(cm_full_file)
convert_unit_to(data, "inch").to_csv(inch_full_file)

# TODO 
# - verify output to make sure nothing got messed up in this process
# - save separate files for
    # - the two directions (as we will always look at data by direction)
        # - put "top surgery" column at front of transmasc one
    # - base demo questions only
    # - measurements only
        # - one in cm, one in inches
    # - standard sizing questions only
# - save files of 
    # - averages & standard deviation where enough data available
    # - processed suggestions




