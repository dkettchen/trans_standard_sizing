import pandas as pd
import plotly.graph_objects as go
from re import split, sub
from code_folder.utils.get_all_clean_filepaths import get_filepaths
from code_folder.utils.calculate_trendline import calculate_trendline
import plotly.express as px

palette = px.colors.qualitative.Plotly


compare_by_genders = {
    "women_and_femmes": ("female", "Transfemme"),
    "men_and_mascs": ("male", "Transmasc"),
    "women_and_mascs": ("female", "Transmasc"),
    "men_and_femmes": ("male", "Transfemme"), 
    "trans_people": ("Transmasc", "Transfemme"),
    "everyone": ("female", "male", "Transfemme", "Transmasc"),
}


def compare(x_col, y_col, unit = "cm"):
    """
    creates a dict of scatter graphs comparing x_col values to y_col values where both were provided

    the keys are the name of a gender combo the scatter describes
    """

    fig_dict = {}

    # which cases are we interested in?
    if (x_col, y_col) in [
        ("hip", "height"),
        ("hip", "thigh"), # for now, bc there was not much of any patterns
        ("hip", "waist"), # only cis men's data so far is smaller hip for waist, everyone else is similar
    ]: # one chart of everyone will do
        to_compare = ["everyone"]
    elif (x_col, y_col) in [ # check everyone and compare trans ppl to cis ppl of target gender
        ("shoulder", "height"),
        ("arm length", "height"),
    ]:
        to_compare = ["everyone", "men_and_mascs", "women_and_femmes"]
    else: # just do all of them
        to_compare = compare_by_genders.keys()

    for gender_combo in to_compare:

        # make figure
        fig_dict[gender_combo] = go.Figure()

    # get mins & maxes
    x_min = None
    y_min = None
    x_max = None
    y_max = None

    colour_counter = 0

    filepaths = get_filepaths("Both", unit)
    for key in filepaths:
        filepath = filepaths[key]
        df = pd.read_csv(filepath)

        # reduce data points if there are too many to see detail
        if len(df) > 300:
            df = df.reset_index(drop=True)
            df = df.loc[df.index.where(df.index % 10 == 0).dropna(how="all")]

        # unpack key info
        if "Trans" in key:
            df = df.set_index("Timestamp")
            study = "The Trans Standard Sizing Project"
            year = 2026
            gender = key
        elif "ANSUR" in key:
            split_ansur = split(r"[_\.]", key)
            study = split_ansur[0]
            year = int(split_ansur[1])
            gender = split_ansur[2]
        else:
            raise ValueError(f"Data parsing not implemented yet for: {key}")

        # exclude the data from the 80s to prioritise newer data
        if year < 2000:
            continue

        # find relevant columns
        for col in df.columns:
            if x_col in col:
                if x_col in ["hip", "waist", "thigh"]:
                    if "high hip" in col or "low" in col or "front" in col or " to " in col or "from" in col:
                        continue
                elif x_col in ["height"]:
                    if "armhole" in col:
                        continue
                elif x_col in ["shoulder"]:
                    if " to " in col or "width" in col or "from" in col or "clavicle" in col:
                        continue
                elif x_col not in ["arm length"]:
                    print(col)
                x = col
            elif y_col in col:
                if y_col in ["hip", "waist", "thigh"]:
                    if "high hip" in col or "low" in col or "front" in col or " to " in col or "from" in col:
                        continue
                elif y_col in ["height"]:
                    if "armhole" in col:
                        continue
                elif y_col in ["shoulder"]:
                    if " to " in col or "width" in col or "from" in col or "clavicle" in col:
                        continue
                elif x_col not in ["arm length"]:
                    print(col)
                y = col

        # remove any none values
        df = df.get([x, y]).dropna(how="any")

        if (x_col, y_col) in [("hip", "height"),]:
            x = df.sort_values(y)[x]
            y = df.sort_values(y)[y]
        else:
            y = df.sort_values(x)[y]
            x = df.sort_values(x)[x]

        # make lists
        x = list(x)
        y = list(y)

        # removing some extreme outliers in the transmasc data (for better trendlines)
        if gender == "Transmasc" and "hip" in [x_col, y_col]:
            x = x[2:-2]
            y = y[2:-2]

        # update mins & maxs
        if not x_min or min(x) < x_min:
            x_min = min(x)
        if not y_min or min(y) < y_min:
            y_min = min(y)
        if not x_max or max(x) > x_max:
            x_max = max(x)
        if not y_max or max(y) > y_max:
            y_max = max(y)

        # add trendline
        trendline = calculate_trendline(x, y)

        # add to each fig we want
        for gender_combo in fig_dict:
            if gender in compare_by_genders[gender_combo]:
                # add measurements
                fig_dict[gender_combo].add_trace(go.Scatter(
                    x=x, y=y,
                    mode='markers',
                    name=key,
                    opacity=0.3,
                    marker_color=palette[colour_counter],
                ))

                # add trend line
                fig_dict[gender_combo].add_trace(go.Scatter(
                    x=x, y=trendline,
                    mode='lines',
                    name=f"{key} (trend)",
                    marker_color=palette[colour_counter],
                    showlegend=False
                ))

        colour_counter += 1

    for gender_combo in fig_dict:

        # set axes
        fig_dict[gender_combo].update_xaxes(range=[x_min - 5, x_max + 5],dtick = 10, title=x_col)
        fig_dict[gender_combo].update_yaxes(range=[y_min - 5, y_max + 5],dtick = 10, title=y_col)
        
        # add title etc
        fig_dict[gender_combo].update_layout(title=f"{x_col} to {y_col} ({unit})".capitalize())

    return fig_dict