import pandas as pd

def compare_height_ratio(meas_1, meas_2):

    for direction in ["Transmasc", "Transfemme"]:
        filepath = f"code_folder/files/separated_data/measurement_ratio_to_height_{direction}.csv"
        df = pd.read_csv(filepath)

        new_ratio = df[meas_1] / df[meas_2]
        print(direction, round(new_ratio.mean(), 3))

if __name__ == "__main__":
    print("back width / front width")
    compare_height_ratio("back width","front width")

    # TODO chest to hip 
        # -> we need to get correct column per each bc it will be labelled differently

    # TODO we should make a util that can always find the column we want in the relevant data set
        # TODO also a util to separate or combine relevant transmasc chest measurements

    # TODO refactor a bunch of our running code to make a more sensible system to assess proportions
