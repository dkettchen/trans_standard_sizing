# files

file_folder = "code_folder/files"
full_file_folder = f"{file_folder}/full_clean_response_data"
separated_files_folder = f"{file_folder}/separated_data"
source_raw_file = "responses_6_july_2026.csv" # latest download -> not final data yet!
"""raw response data file as downloaded from google forms/sheets"""

response_file = f"{file_folder}/{source_raw_file}"
clean_columns_file = f"{full_file_folder}/raw_responses_cleaned_columns.csv"
cm_full_file = f"{full_file_folder}/cleaned_full_responses_in_cm.csv"
inch_full_file = f"{full_file_folder}/cleaned_full_responses_in_inch.csv"

# measurements
chest_meas = [ # chest measurements
    'underbust circumference', 
    'front chest', 
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only

    # post-op transmascss only
    'distance from clavicle to inner end of the scar (top surgery)', 
    'distance between inner ends of your scars (top surgery)', 
    'distance from clavicle to outer end of the scar (top surgery)', 
    'distance between outer ends of your scars (top surgery)', 
    'distance from clavicle to the lowest/bending/middle point of the scar (top surgery)', 
    'distance between lowest/bending/middle points of your scars (top surgery)', 

    # transfemmes only
    'underbust circumference (snug)', 
    'underbust circumference (tight)', 
    'strap length to underbust (front)', 
    'strap length to underbust (back)', 
    'front bust (standing)', 
    'bust circumference (bent over)', 
    'bust circumference (lying down)', 
    'overbust circumference', 
    'clavicle to overbust', 
    'clavicle to nipple/apex', 
    'top cup', 
    'bottom cup', 
    'outer arc', 
    'inner arc', 
    'breast spacing', 
    'bust circumference (padded bra)', 
]
meas = [ # other measurements
    'height (REQUIRED)', 
    'nape of the neck to floor', 
    'head circumference', 
    'neck circumference', 
    'base of neck circumference', 
    'shoulder (REQUIRED)', 
    'arm length (REQUIRED)', 
    'shoulder to elbow', 
    'elbow to wrist', 
    'bicep circumference (REQUIRED)', 
    'elbow circumference', 
    'wrist circumference', 
    'hand circumference', 
    'armhole height (front)', 
    'armhole height (back)', 
    'sleeve cap', 
    'armpit distance', 
    'front width', 
    'back width', 
    'shoulder width (front) (REQUIRED)', 
    'shoulder width (back)', 
    'clavicle to shoulder point distance', 
    'natural waist circumference (REQUIRED)', 
    'front (natural) waist', 
    'distance from clavicle to natural waist (front) (REQUIRED)', 
    'distance from clavicle to natural waist (front, with ruler)', 
    'side seam to natural waist', 
    'nipple/bust point distance', 
    'distance from shoulder to natural waist (front)', 
    'distance from nipple/bust point to natural waist', 
    'distance from underbust to natural waist', 
    'shoulder to natural waist (diagonal, front)', 
    'shoulder to natural waist (diagonal, back)', 
    'distance from nape of the neck to natural waist (back)', 
    'distance from shoulder to natural waist (back)', 
    'nape of the neck to end of ribcage/sternum', 
    'end of ribcage/sternum to natural waist', 
    'nape of the neck to front natural waist', 
    'high hip/low waist circumference (REQUIRED)', 
    'front (low) waist', 
    'natural waist to high hip/low waist distance (front)', 
    'natural waist to high hip distance (side)', 
    'natural waist to high hip distance (back)', 
    'hip circumference (REQUIRED)', 
    'front hip', 
    'natural waist to hip (front)', 
    'natural waist to hip (side)', 
    'natural waist to hip (back)', 
    'fly length (from natural waist)', 
    'rise to natural waist (REQUIRED)', 
    'crotch depth', 
    'outseam from natural waist (side) (REQUIRED)', 
    'outseam from natural waist (front)', 
    'outseam from natural waist (back)', 
    'inseam', 
    'thigh circumference (REQUIRED)', 
    'knee circumference', 
    'calf circumference', 
    'ankle circumference', 
    'foot entry circumference', 
    'knee to floor', 
    'ankle to floor', 
]
min_meas = [ # some selected measurements to gage proportion
    'height (REQUIRED)', 
    'arm length (REQUIRED)', 
    'bicep circumference (REQUIRED)', 
    'shoulder (REQUIRED)', 
    'underbust circumference',
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only
    'front (natural) waist', 
    'natural waist circumference (REQUIRED)', 
    'front (low) waist', 
    "high hip/low waist circumference (REQUIRED)",
    'front hip', 
    'hip circumference (REQUIRED)', 
    'outseam from natural waist (side) (REQUIRED)', 
    'inseam', 
    'thigh circumference (REQUIRED)', 
]

smallest_measurements = [ # only these measurements can be smaller than 5 cm
    "distance between inner ends of your scars (top surgery)",
    "breast spacing",
]
min_max_values = { # in cm
    "hand circumference": [15,40],
    "head circumference": [50,70],
}
half_values = { # key mustn't be significantly smaller or close to value
                # check for <*0.2 to >*0.8
    "front hip": "hip circumference (REQUIRED)",
    "front (low) waist": "high hip/low waist circumference (REQUIRED)",
    "front (natural) waist": "natural waist circumference (REQUIRED)",
}
compared_to_other_meas = { # measurement + num shouldn't be smaller/bigger than other meas * decimal
    "outseam from natural waist (side) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "outseam from natural waist (front) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "outseam from natural waist (back) (REQUIRED)": [0, "smaller than", "height (REQUIRED)", 0.5],
    "arm length (REQUIRED)": [10, "bigger than", "height (REQUIRED)", 0.5],
    "armpit distance": [0, "bigger than", "bicep circumference (REQUIRED)", 0.8],
    "chest circumference (post-op or binder)": [0, "smaller than", "underbust circumference", 0.8],
    "bust circumference (standing/no binder)": [0, "smaller than", "underbust circumference", 0.8],
}

torso_meas = [ 
    'underbust circumference',
    'chest circumference (post-op or binder)', # transmascs only
    'bust circumference (standing/no binder)', # transfemmes & non-op transmascs only
    'natural waist circumference (REQUIRED)', 
    "high hip/low waist circumference (REQUIRED)",
    'hip circumference (REQUIRED)', 
]
torso_dist = [ # measurements from shoulder/neck area to natural waist -> should be in similar range
    'distance from clavicle to natural waist (front) (REQUIRED)', 
    'distance from clavicle to natural waist (front, with ruler)', 
    'distance from shoulder to natural waist (front)', 
    'shoulder to natural waist (diagonal, front)', 
    'shoulder to natural waist (diagonal, back)', 
    'distance from nape of the neck to natural waist (back)', 
    'distance from shoulder to natural waist (back)', 
]

# other columns
other_qs = [
    # 'direction', 
    # 'unit', 
    'how did you find the survey?', 
    'suggestions', 
]
med_qs = [
    'standard HRT', 
    'consistent HRT for 3 years', 
    'total time on HRT', 
    'progesterone', 
    'top surgery', 
    'breast augmentation', 
    'breast reduction or mastectomy', 
    'padded bra', 
    'hysterectomy', 
    'crotch volume', 
    'other surgery', 
]
body_qs = [
    'age group', 
    'plus-size', 
    'extra tall', 
    'extra short', 
    'very muscular', 
]
standard_sizing_qs = [
    'did you shop in birth sex aisle pre-transition and remember your size(s)', 
    'pre-transition sizes', 
    'how well did standard sizing fit pre-transition', 
    'how did that change', 
]
fit_issues = [
    'fit issue with shoulder width', 
    'fit issue with sleeve circumference', 
    'fit issue with sleeve length', 
    'fit issue with chest width', 
    'fit issue with breast space ', 
    'fit issue with waist size', 
    'fit issue with torso length ', 
    'fit issue with hip width', 
    'fit issue with pant crotch fit', 
    'fit issue with leg circumference', 
    'fit issue with leg length', 
    'other fit issues'
]