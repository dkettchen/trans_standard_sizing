from code_folder.utils.lookup import separated_files_folder
import pandas as pd

def fit_issues():
    """TODO"""
    
    fit_issues_dict = {}

    for direction in ["Transmasc", "Transfemme"]:
        fit_issues_dict[direction] = {}

        # read in relevant data
        stan_size_filepath = f"{separated_files_folder}/standard_sizing_qs_{direction}.csv"
        stan_size_df = pd.read_csv(stan_size_filepath, index_col="Timestamp")

        # get relevant col
        grouping_cols = [c for c in stan_size_df.columns if "fit issue with" in c]

        for col in grouping_cols:
            count = stan_size_df.reset_index().groupby(col).count()["Timestamp"]
            fit_issues_dict[direction][col] = count

        fit_issues_dict[direction] = pd.DataFrame(fit_issues_dict[direction])
    
        fit_issues_dict[direction] = fit_issues_dict[direction].rename(index={
            "too big":f"too big ({direction})",
            "too small":f"too small ({direction})",
        })
    
    return pd.concat([fit_issues_dict["Transmasc"], fit_issues_dict["Transfemme"]]).transpose()
