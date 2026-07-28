import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from code_folder.utils.lookup import processed_data_folder, gender_categories, suffix
from re import sub

four_colours = ["lightskyblue","royalblue", "hotpink","crimson"]

colours = {
    "fit_issues": four_colours,
    "crotch_volume": four_colours,
    "rating_height": {
        "tall":"red", 
        "average":"orange", 
        "short":"darkgreen",
        "actual average":"hotpink",
    },
    "biggest_measurement": {
        "chest":"yellowgreen",
        "waist":"lightgreen",
        "hip":"darkgreen",
        "chest and waist": "olivedrab",
        "waist and hip": "limegreen",
        "chest and hip": "greenyellow",
    }
}

def visualise(data_case):
    """
    datacase=crotch_volume|fit_issues|rating_height|torso_proportions|biggest_measurement
    """

    # read relevant data in
    filepath = f"{processed_data_folder}/{data_case}.csv"
    df = pd.read_csv(filepath, index_col=0)

    if data_case in colours:
        palette = colours[data_case]

    # vis with relevant type of graph

    # grouped bars for fit issues
    if data_case == "fit_issues":
        graph_type = "grouped bar"

        fig_dict = {}
        counter = 0
        for direction in ["Transmasc", "Transfemme"]:
            # remove empty columns for that direction if any
            direction_df = df.get([f'too big ({direction})', f'too small ({direction})']).dropna(how="all")

            # sort by most common complaint per direction
            if direction == "Transmasc":
                direction_df = direction_df.sort_values(f'too big ({direction})', ascending=False)
            else:
                direction_df = direction_df.sort_values(f'too small ({direction})', ascending=False)

            # make figure
            x = [c if "circumference" not in c else sub("circumference", "circ.", c) for c in  direction_df.index]
            fig = go.Figure(data=[
                go.Bar(name=f'too big', x=x, y=direction_df[f'too big ({direction})'], marker_color=palette[counter]),
                go.Bar(name=f'too small', x=x, y=direction_df[f'too small ({direction})'], marker_color=palette[counter+1]),
            ])
            # move colours up
            counter += 2

            # update graph
            fig.update_layout(
                barmode='group', 
                title=f"Reported fit issues by {direction.lower()}s (%)",
            )
            fig.update_yaxes(range=[0,100])

            # save to dict
            fig_dict[direction] = fig

        # return both graphs in a dict
        return fig_dict

    # pies of crotch volume
    elif data_case == "crotch_volume":
        graph_type = "pie"

        # make subplots
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type':'domain'}, {'type':'domain'}]], 
            subplot_titles=['Transmasc', 'Transfemme']
        )
        # add traces for each direction's data
        fig.add_trace(
            go.Pie(
                labels=["Habitually packing <br>or bottom surgery", "No extra volume"], 
                values=df["Transmasc"], name="Transmascs",
                marker_colors=colours[data_case][:2][::-1]
            ),
            1, 1
        )
        fig.add_trace(
            go.Pie(
                labels=["Extra volume", "Habitually tucking <br>or bottom surgery"],
                values=df["Transfemme"], name="Transfemmes",
                marker_colors=colours[data_case][2:][::-1]
            ),
            1, 2
        )

        # update figure
        fig.update_traces(
            textinfo='label+percent',
            insidetextorientation="horizontal",
            textposition='inside'
        )
        fig.update_layout(
            title="Usual crotch volume by direction",
            uniformtext_minsize=12, 
            uniformtext_mode='hide'
        )

    # scatters for each birthsex
    elif data_case == "rating_height":
        graph_type = "scatter"

        # calculate our own averages bc I can't easily find a global average online, only by country
        average_heights = {
            "afab": df["heights"].where(df["direction"] == "Transmasc").mean(),
            "amab": df["heights"].where(df["direction"] == "Transfemme").mean(),
        }

        fig_dict = {}
        
        for birthsex in ["afab", "amab"]:
            # ['heights', 'amab', 'afab', 'direction']

            fig = make_subplots(rows=1, cols=2, subplot_titles=("Transmascs", "Transfemmes"))

            placement_counter = 0.95
            for s in ["tall", "average", "short", "actual average"]:
                fig.add_annotation(
                    text=s,
                    xref="paper", yref="paper",
                    x=0.02, y=placement_counter, showarrow=False,
                    bgcolor=palette[s],
                    font_color="white",
                    font_size=13,
                    borderpad=4,
                )
                placement_counter -= 0.075

            counter = 1
            for direction in ["Transmasc", "Transfemme"]:

                direction_df = df.where(df["direction"] == direction).dropna(how="all")

                # add actual average height
                fig.add_shape(type="line",
                    x0=0, y0=average_heights[birthsex], x1=len(direction_df), y1=average_heights[birthsex],
                    line=dict(color=palette["actual average"],width=2),
                    row=1, col=counter
                )

                # add the data
                fig.add_trace(
                    go.Scatter(
                        x=[i for i in range(len(direction_df))], 
                        y=direction_df["heights"],
                        marker_color=direction_df[birthsex].apply(
                            lambda x: palette[x]
                        ),
                        mode='markers'
                    ),
                    row=1, col=counter
                )

                counter += 1
            
            fig.update_layout(
                showlegend=False, 
                title=f"Height rating compared to {birthsex} people",
            )
            fig.update_yaxes(range=[140,210])
            fig.update_xaxes(showticklabels=False)

            fig_dict[birthsex] = fig

        return fig_dict

    # scatters for torso measurements
    # TODO add cis data
    elif data_case == "torso_proportions":
        fig_dict = {}
        mode = "lines+markers"

        for direction in df["direction"].unique():
            direction_df = df.where(df["direction"] == direction).dropna(how="all").dropna(how="all",axis=1)
            direction_df.pop("direction")

            if direction == "Transfemme":
                direction_df = direction_df.rename(columns={"chest": "bust"})
            columns = direction_df.columns

            fig = go.Figure()

            for response in direction_df.index:
                fig.add_trace(
                    go.Scatter(
                        x = columns,
                        y = direction_df.loc[response],
                        mode = mode
                    )
                )

            title = f"{direction} torso circumferences"
            if direction == "Transmasc":
                title += " (post-top surgery chest measurements only)"

            fig.update_yaxes(range=[55,175])
            fig.update_layout(
                showlegend=False,
                title=title
            )

            fig_dict[direction] = fig
        return fig_dict

    # grouped bars for biggest measurements
    elif data_case == "biggest_measurement":
        graph_type = "grouped bar"

        # make figure
        fig = go.Figure()

        labels = [sub("man", "men", i) if "man" in i else i + "s" for i in df.columns]
        for i in df.index:
            
            fig.add_trace(
                go.Bar(
                    name=i, x=labels, y=df.loc[i], 
                    text=df.loc[i], textposition="auto",
                    marker_color=palette[i]
                )
            )

        # update graph
        fig.update_layout(
            barmode='group', 
            title=f"Biggest torso circumference measurement (%)",
        )
        fig.update_yaxes(range=[0,100])

    else:
        fig = go.Figure()


    return fig