"""clean raw response file & separate into section files (measurements, demo data, etc)"""

from code_folder.src.cleaning_responses.clean_responses import run_cleaning
from code_folder.src.cleaning_responses.separate_files import separate_into_files

## clean and format raw data
# clean data
run_cleaning()
# separate into smaller files
separate_into_files()
