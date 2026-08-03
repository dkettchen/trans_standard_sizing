"""run all the code in order whenever we got a new response file"""

from code_folder.src.clean_responses import run_cleaning
from code_folder.src.separate_files import separate_into_files
from code_folder.src.suggestions import parse_suggestions
from code_folder.src.rating_height import get_heights_and_compare
from code_folder.utils.lookup import processed_data_folder, charts_folder
from code_folder.src.crotch_volume import crotch_volume
from code_folder.src.fit_issues import fit_issues
from code_folder.src.torso_proportions import torso_proportions
from code_folder.src.biggest_measurement import biggest_measurement
from code_folder.src.how_did_fit_change import fit_change
from code_folder.src.transmasc_bust_comparison import bust_comparison
from code_folder.src.visualise import visualise
from code_folder.src.visualise_ratios import compare

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
# torsos = torso_proportions()
# for key in torsos:
#     df = torsos[key]
#     df.to_csv(f"{processed_data_folder}/torso_proportions_{key}.csv", index=False)
# biggest_measurement().to_csv(f"{processed_data_folder}/biggest_measurement.csv")
# change = fit_change()
# for key in change:
#     df = change[key]
#     df.to_csv(f"{processed_data_folder}/how_did_fit_change_{key}.csv", index=False)
# bust_comparison("cm") # prints its own files

# TODO
# ✅ - how well did they fit standard sizing pre-transition vs how did they rate the change scatter
# - relevant measurements vs whether or not they reported fit issues
    # - may need multiple measurements ex. height + arm length for arm length fit issue
# ✅ - compare transmasc bust, binder & projected chest measurements where they were provided
    ## the two trendlines look very parallel on the chart
    ## -> seem to have ca 1.75-1.8cm distance between post-op chest & binder chest measurement
    ## -> that is firmly within the range for adding as ease!
        # -> similar approach to leaving some extra space for transfemme crotches, 
        # we can just add enough ease to make sure binder chests have space enough
        # without looking weird on post-op chests
            # code to calculate it is commented out in the vis file
# - thigh to hip ratio
# - waist to hip ratio

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

# TODO refactor for new output
# torso_dict = visualise("torso_proportions")
# for direction in torso_dict:
#     fig = torso_dict[direction]
#     if direction == "Transfemme":
#         width = 1000
#     elif direction == "Transmasc":
#         width = 800

#     fig.write_image(
#         f"{charts_folder}/torso_proportions_{direction}.png",
#         height=500,
#         width=width
#     )

# biggest_measurement_fig = visualise("biggest_measurement")
# biggest_measurement_fig.write_image(
#     f"{charts_folder}/biggest_measurements.png",
#     height=500,
#     width=1000
# )

# fig_dict = visualise("fit_change")
# for direction in fig_dict:
#     fig = fig_dict[direction]
#     fig.write_image(
#         f"{charts_folder}/how_did_fit_change_{direction}.png",
#         height=800,
#         width=800
#     )

# chest_fig = visualise("chest_measurements_in_cm_Transmasc")
# chest_fig.write_image(
#     f"{charts_folder}/transmasc_chests_to_underbust.png",
#     height=500,
#     width=520
# )

# compare measurements to each other
for x_col, y_col in [
    # note: when including 80s data, even the cis data largely does not align with itself
        # -> I've excluded the older data now in hopes of making it more comparable
        # -> this may also improve with more cis data
    ("hip", "thigh"),
        # transmascs do have wider hips than cis men for same thigh circ (bc hip bone will be diff)
        # so do transfemmes
        # transmascs have smaller thighs than cis women for same hip circ (bc hip bone will be same)
    ("hip", "waist"),
        # transmascs' hip/waist ratio is eerily close to military cis women in 2012 apparently
        # transmascs have wider hips than cis men for same waist circ
    ("hip", "height"), # aligns with the cis ppl of the same bones
    ("shoulder", "height"), # seems to be somewhat all over the place, 
                            # and cis data doesn't have the same range as trans one of extremes
    ("arm length","height"), # seems to be proportional across all genders, but obv height varies -> so does arm length
    # ("arm length","chest"), # TODO make sure it checks the relevant measurements
]:
    fig_dict = compare(x_col, y_col)

    for gender_combo in fig_dict:
        fig_dict[gender_combo].write_image(
            f"{charts_folder}/{x_col}_to_{y_col}_ratio_{gender_combo}.png",
            height=500,
            width=700
        )