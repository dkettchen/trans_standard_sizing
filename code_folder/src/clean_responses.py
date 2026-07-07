from code_folder.src.clean_columns import run_clean_columns
# temp file while we wait for full data
response_file = "code/files/responses_6_july_2026.csv"

data = run_clean_columns(response_file)



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

