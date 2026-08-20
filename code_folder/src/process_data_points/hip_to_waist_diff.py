import pandas as pd
from code_folder.utils.get_all_clean_filepaths import get_filepaths

def hip_to_waist_diff(unit="cm"):

    report = {}

    filepaths = get_filepaths("Both", unit)
    for key in filepaths:
        if "1988" in key:
            continue
        filepath = filepaths[key]
        df = pd.read_csv(filepath)

        waist_and_hip_cols = [col for col in df.columns if "waist" in col or "hip" in col]
        new_columns = {}
        for c in waist_and_hip_cols:
            if "circumference" in c:
                if "natural" in c:
                    new_columns[c] = "natural waist"
                elif "low" in c:
                    new_columns[c] = "low waist"
                elif "hip" in c:
                    new_columns[c] = "hip"

                elif "waist" in c:
                    new_columns[c] = "natural waist"
        
        rel_cols = df.get(new_columns.keys()).rename(columns=new_columns)

        for col in ["natural waist", "low waist", "hip"]:
            if col not in rel_cols.columns:
                rel_cols[col] = None

        rel_cols["waist_to_hip_diff"] = rel_cols["hip"] - rel_cols["natural waist"]
        rel_cols["low_waist_to_hip_diff"] = rel_cols["hip"] - rel_cols["low waist"]
        rel_cols["nat_to_low_waist_diff"] = rel_cols["low waist"] - rel_cols["natural waist"]

        rel_cols["waist_to_hip_ratio_comp_to_hip"] = (rel_cols["waist_to_hip_diff"] / rel_cols["hip"]) * 100
        rel_cols["low_waist_to_hip_ratio_comp_to_hip"] = (rel_cols["low_waist_to_hip_diff"] / rel_cols["hip"]) * 100
        rel_cols["nat_to_low_waist_ratio_comp_to_nat"] = (rel_cols["nat_to_low_waist_diff"] / rel_cols["natural waist"]) * 100

        report[key] = {
            "full_data": rel_cols,
            "averages": rel_cols.mean()
        }
    
    report_df = pd.DataFrame({key: report[key]["averages"] for key in report})
    print(report_df)

    # this cis data also looks strange -> we need to test all these w more cis data 
    # bc I am starting to just doubt this data set in general like-