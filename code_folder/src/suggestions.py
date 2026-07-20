import pandas as pd
from code_folder.utils.lookup import separated_files_folder, processed_data_folder
from re import split, sub

items = {
    "yes": {
        "pants": [
            "pant", "trouser", "bottom", "chino", "cargo", 
            "jean", "jogger", "shorts", "trunk", "slack"
        ],
        "shorts": [
            "shorts", "trunks"
        ],
        "underwear bottoms": [
            "trunks", "boxer", "underwear", "panty", "panties", "brief",
        ],
        "bra": [
            "bra",
        ],
        "lingerie": [
            "lingerie", "sexy", 
        ],
        "swimwear": [
            "swim", "speedo", "bikini",
        ],
        "dress": [
            "dress", "maxi", "pinafore",
        ],
        "shirt": [
            "shirt", "button-up", "long-sleeve",
        ],
        "t-shirt": [
            "t-shirt",
        ],
        "skirt": [
            "skirt"
        ],
        "waistcoat": [
            "waistcoat", "vest",
        ],
        "jacket": [
            "coat", "jacket", "blazer",
        ],
        "suit": [
            "suit", "dress shirt", "dress trouser", "dress pant", 
            "waistcoat", "vest", "button-up", "shirt", "formal",
            "tux", "sport coat"
        ],
        "jumpsuit": [
            "overall", "jumpsuit", "dungaree", "romper",
        ],
        "sportswear/athleisure": [
            "sport", "legging", "jogger", "jersey",
        ],
        "tank top": [
            "tank", "spaghetti"
        ],
        "blouse": [
            "blouse"
        ],
        "tops": [
            "top", "shirt", "blouse", "upper body",
        ],
        "shoes": [
            "shoe",
        ],
        # shoes (shouldn't be here but I guess we'll count it if people put it)
        # scrubs / workwear
        # adjustable waists (this is not a garment babes)
        # alternative clothes
        # extra designs
        # extra bits
        # longer sleeves

        


    },
    "no": {
        "pants": [
            "panty", "panties", "boxer shorts",
        ],
        "shorts": [
            "boxer shorts",
        ],
        "underwear bottoms": [
            "swim"
        ],
        "bra": [

        ],
        "lingerie": [

        ],
        "swimwear": [

        ],
        "dress": [
            "dress shirt", "dress trouser", "dress pant",
        ],
        "shirt": [
            "t-shirt", "shirt dress",
        ],
        "t-shirt": [

        ],
        "skirt": [

        ],
        "waistcoat": [

        ],
        "jacket": [
            "waistcoat",
        ],
        "suit": [
            "suited", "jumpsuit", "t-shirt", "shirt dress", "swim",
        ],
        "jumpsuit": [

        ],
        "sportswear/athleisure": [
            "sport coat", # this is a blazer apparently
        ],
        "tank top": [

        ],
        "blouse": [

        ],
        "tops": [

        ],
        "shoes": [

        ],
    }
}

def parse_suggestions():
    """
    counts how many transmascs and transfemmes requested certain types of garments in their suggestions
    
    returns a df with a Transmasc and Transfemme column, garment category index, and count values
    """

    suggesto_count = {}

    for direction in ["Transmasc", "Transfemme"]:
        # print("💘 Now parsing suggestions for:", direction)

        # make a dict for each direction
        suggesto_count[direction] = {}

        # read in relevant data
        filepath = f"{separated_files_folder}/standard_sizing_qs_{direction}.csv"
        df = pd.read_csv(filepath, index_col="Timestamp")

        # get suggestos
        suggestion_col = df["suggestions"]

        # turn from string back to list
        parsed_col = suggestion_col.apply(
            lambda x: [] if type(x) != str else [v.lower() for v in split(r"([\"'], [\"'])", x[2:-2]) if v[1:3] != ", "]
        )
        # remove dashes for consistency
        parsed_col = parsed_col.apply(
            lambda x: [sub(r"-"," ", y) for y in x]
        )
        # reduce whitespaces to a single whitespace
        parsed_col = parsed_col.apply(
            lambda x: [sub(r"\s+"," ", y) for y in x]
        )

        # reintroduce dashes to make easier to identify
        for word in ["button-up", "t-shirt", "long-sleeve"]:
            # t shirt -> t-shirt
            parsed_col = parsed_col.apply(
                lambda x: [sub(sub("-", " ", word),word, y) for y in x]
            )
            # tshirt -> t-shirt
            parsed_col = parsed_col.apply(
                lambda x: [sub(sub("-", "", word),word, y) for y in x]
            )

        # # look at all suggestions
        # for suggestions in parsed_col:
        #     if len(suggestions) == 0:
        #         continue
        #     for s in suggestions:
        #         print(s)

        for item in items["yes"]:
            if item not in suggesto_count[direction]:
                suggesto_count[direction][item] = 0

            # print("🔁 Now checking for:", item)

            # for each response's suggestions
            for suggestions in parsed_col:
                if len(suggestions) == 0:
                    continue

                for s in suggestions:

                    item_bool = False
                    for word in items["yes"][item]:
                        if word in s:
                            item_bool = True
                            break
                    if item_bool:
                        for word in items["no"][item]:
                            if word in s:
                                if (item in ["pants","shorts"] and word == "boxer shorts" and "swim trunks" in s)\
                                or (item in ["underwear bottoms"] and word == "swim" and "boxer shorts" in s)\
                                or (item in ["shirt", "suit"] and word == "t-shirt" and "shirt" in sub("t-shirt", " ", s))\
                                or (item in ["suit"] and word == "suited" and "button-up" in s):
                                    continue
                                # print(f"❌ Found exclusion word for {item} in:", s, word)
                                item_bool = False

                    if item_bool:
                        suggesto_count[direction][item] += 1
                        # print(s)

    # make plain counts into a dataframe
    suggesto_df = pd.DataFrame(suggesto_count)
    return suggesto_df

if __name__ == "__main__":
        count_df = parse_suggestions()
        # print(count_df)
        count_df.to_csv(f"{processed_data_folder}/suggestion_counts.csv", index=True)