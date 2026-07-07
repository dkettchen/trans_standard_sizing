import pandas as pd

def make_list(row:pd.Series, data_case:str):
    """
    takes a row and makes a list of data_case's 
    relevant column values if any

    - data_case="sizing": returns a list of tuples in format [(sizing system, size), ...]
        - if a sizing system or size didn't have a matching pair, 
        it will be left out, as it won't be usable data
    - data_case="suggestions": returns a list of strings [suggestion, ...]

    if no values were given, it returns none
    """
    collected_list = []
    for i in range(1,4):
        if data_case == "sizing":
            sizing_s = row[f"sizing system {i}"]
            size = row[f"size {i}"]
            if type(sizing_s) == str and type(size) == str:
                collected_list.append((sizing_s, size))
        elif data_case == "suggestions":
            suggestion = row[f"suggestion {i}"]
            if type(suggestion) == str:
                collected_list.append(suggestion)
    if len(collected_list) == 0:
        return None
    return collected_list
