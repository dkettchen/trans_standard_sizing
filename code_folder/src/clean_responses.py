from code_folder.src.clean_columns import run_clean_columns
from code_folder.src.clean_values import run_clean_values
from code_folder.utils.print_averages import print_averages
from code_folder.utils.convert_unit import convert_unit_to

"""
cleans raw response data (ex. shorten, unify and reorder columns, omit or fix unrealistic values)
and saves to new files
"""

file_folder = "code_folder/files/full_clean_response_data"
source_raw_file = "responses_6_july_2026.csv" # latest download -> not final data yet!
"""raw response data file as downloaded from google forms/sheets"""

# temp file while we wait for full data
response_file = f"{file_folder}/{source_raw_file}"

# read in and clean the columns
data = run_clean_columns(response_file)

# save cleaned/unified columns version without actually changing any values yet
data.to_csv(f"{file_folder}/raw_responses_cleaned_columns.csv")

# then we clean the values
data = run_clean_values(data)
# print_averages(data) # to verify/sneak peak

# save to file in cm and inches
data.to_csv(f"{file_folder}/cleaned_full_responses_in_cm.csv")
convert_unit_to(data, "inch").to_csv(f"{file_folder}/cleaned_full_responses_in_inch.csv")

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




