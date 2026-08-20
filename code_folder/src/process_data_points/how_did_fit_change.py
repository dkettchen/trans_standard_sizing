from code_folder.lookup import separated_files_folder, processed_data_folder
import pandas as pd

def fit_change():
    """TODO"""

    fit_change_dict = {}
    improvement_dict = {}

    for direction in ["Transmasc", "Transfemme"]:
        # read in relevant data
        stan_size_filepath = f"{separated_files_folder}/standard_sizing_qs_{direction}.csv"
        stan_size_df = pd.read_csv(stan_size_filepath, index_col="Timestamp")
        
        # get relevant data
        df = stan_size_df.where( # exclude N/A responses
            (stan_size_df["how well did standard sizing fit pre-transition"] != "Not applicable") & (
                stan_size_df["how did that change"] != "Not applicable"
            )
        ).dropna(how="all")
        total = len(
            df.get([
                "how well did standard sizing fit pre-transition",
                "how did that change",
            ]).dropna(how="any")
        )

        # relabel poorly answers to unify them into one category
        df["how well did standard sizing fit pre-transition"] = df["how well did standard sizing fit pre-transition"].apply(
            lambda x : "Poorly" if type(x) == str and "Poorly" in x and "Very" not in x else x
        ).apply(
            lambda x : "Somewhat well" if type(x) == str and "Somewhat well" in x else x
        )
        
        # count each combo
        df = df.groupby(
            [
                "how well did standard sizing fit pre-transition",
                "how did that change",
            ]
        ).count().rename(
            columns={"did you shop in birth sex aisle pre-transition and remember your size(s)":"count"}
        )["count"]

        for now in [
            "For the better", "Neutrally", "For the worse"
        ]:
            for then in [
                "Very poorly", "Poorly", "Somewhat well", "Very well", 
            ]:
                
                if (then, now) not in df.index:
                    df.loc[(then, now)] = 0
        
        df = df.reset_index()

        # turn into percent
        df["count"] = df["count"].apply(
            lambda x: round((x / total) * 100, 2)
        )

        # save
        fit_change_dict[direction] = df

        # calculate how many fit well or very well & had neutral or for the worse changes
        df = df.where(df["count"] != 0).dropna(how="all")
        fit_poorly = round(df.where(
            df["how well did standard sizing fit pre-transition"].isin(["Poorly", "Very Poorly"])
        )["count"].sum(), 2)
        fit_well = round(df.where(
            df["how well did standard sizing fit pre-transition"].isin(["Somewhat well", "Very well"])
        )["count"].sum(), 2)
        improvement = round(df.where(
            df["how did that change"].isin(["For the better"]) & \
            df["how well did standard sizing fit pre-transition"].isin(["Somewhat well", "Very well"])
        )["count"].sum(), 2)
        no_improvement = round(df.where(
            df["how did that change"].isin(["Neutrally", "For the worse"]) & \
            df["how well did standard sizing fit pre-transition"].isin(["Somewhat well", "Very well"])
        )["count"].sum(), 2)
        actively_worse = round(df.where(
            df["how did that change"].isin(["For the worse"]) & \
            df["how well did standard sizing fit pre-transition"].isin(["Somewhat well", "Very well"])
        )["count"].sum(), 2)
        improvement_dict[direction] = {
            "fit_poorly_pre_transition": fit_poorly,
            "fit_well_pre_transition": fit_well,
            "better": improvement,
            "neutral": round(no_improvement - actively_worse, 2),
            "worse": actively_worse,
            "neutral_or_worse": no_improvement,
        }
    
    pd.DataFrame(improvement_dict).to_csv(f"{processed_data_folder}/did_fit_improve_for_those_who_fit_standard_sizing.csv")

    return fit_change_dict


