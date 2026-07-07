from code_folder.utils.read_response_file import read_responses_file
from code_folder.utils.unify_duplicate_columns import unify_duplicate_columns
from code_folder.utils.unify_list_fields import unify_list_fields
from code_folder.utils.order_columns import order_columns

def run_clean_columns(response_file:str):
    """
    cleans, unifies, reorders the columns of the raw response file
    """
    data = read_responses_file(response_file)
    data = unify_duplicate_columns(data)
    data = unify_list_fields(data)
    data = order_columns(data)
    return data

# TODO 
# ✅ fix columns
    # ✅ rename columns etc for base convenience
    # ✅ unify same columns that were separated by transmascs/transfemmes
        # ✅ various of the transition responses
        # ✅ age group
        # ✅ unit
        # ✅ certain measurements
    # ✅ unify several fields that should be a list
        # ✅ sizing systems need to be combined
        # ✅ sizing instances need to be made into a list (of like tuples or smth to have system - size together)
        # ✅ check format for unusual heights?
        # ✅ suggestions
    # ✅ order new columns into a sensible order
# TODO test that these are doing what we want them to -> check data output