"""run all the code in order whenever we got a new response file"""

from code_folder.src.clean_responses import run_cleaning
from code_folder.src.separate_files import separate_into_files
from code_folder.src.suggestions import parse_suggestions
from code_folder.src.rating_height import get_heights_and_compare
from code_folder.utils.lookup import processed_data_folder, charts_folder
from code_folder.src.crotch_volume import crotch_volume
from code_folder.src.fit_issues import fit_issues
from code_folder.src.torso_proportions import torso_proportions
from code_folder.src.visualise import visualise

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
# fit_issues().to_csv(f"{processed_data_folder}/fit_issues.csv")
torso_proportions().to_csv(f"{processed_data_folder}/torso_proportions.csv")

## visualise
# fit_issue_fig_dict = visualise("fit_issues")
# for direction in fit_issue_fig_dict:
#     fig = fit_issue_fig_dict[direction]
#     fig.write_image(
#         f"{charts_folder}/fit_issues_{direction}.png",
#         height=500,
#         width=1000
#     )

# crotch_fig = visualise("crotch_volume")
# crotch_fig.write_image(
#     f"{charts_folder}/crotch_volume.png",
#     height=550,
#     width=950
# )

# height_fig_dict = visualise("rating_height")
# for birthsex_comp in height_fig_dict:
#     fig = height_fig_dict[birthsex_comp]

#     fig.write_image(
#         f"{charts_folder}/heights_rated_vs_{birthsex_comp}.png",
#         height=550,
#         width=950
#     )

torso_dict = visualise("torso_proportions")
for direction in torso_dict:
    fig = torso_dict[direction]
    if direction == "Transfemme":
        width = 1000
    elif direction == "Transmasc":
        width = 800

    fig.write_image(
        f"{charts_folder}/torso_proportions_{direction}.png",
        height=500,
        width=width
    )
