"""run all the code in order whenever we got a new response file"""

from code_folder.src.clean_responses import run_cleaning
from code_folder.src.separate_files import separate_into_files
from code_folder.src.suggestions import parse_suggestions
from code_folder.src.rating_height import get_heights_and_compare
from code_folder.utils.lookup import processed_data_folder
from code_folder.src.crotch_volume import crotch_volume
from code_folder.src.fit_issues import fit_issues

# ## clean and format raw data
# # clean data
# run_cleaning()
# # separate into smaller files
# separate_into_files()

# ## process data into insights
# # what garments did people request?
# parse_suggestions().to_csv(f"{processed_data_folder}/suggestion_counts.csv", index=True)
# # how did people rate their height compared to amab & afab people
# get_heights_and_compare().to_csv(f"{processed_data_folder}/rating_height.csv")
# # how likely is each direction to have extra crotch volume
# crotch_volume().to_csv(f"{processed_data_folder}/crotch_volume.csv")
# what are the most reported fit issues by direction
fit_issues().to_csv(f"{processed_data_folder}/fit_issues.csv")


## visualise
