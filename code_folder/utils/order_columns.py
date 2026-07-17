import pandas as pd

# column categories in order we want for now
# general info
general = [ # general
    'direction', 
    'age group', 
    'unit', 
    'how did you find the survey?', 
    'suggestions'
]
HRT = [ # HRT
    'standard HRT', 
    'consistent HRT for 3 years', 
    'total time on HRT', 
    # transfemmes only
    'progesterone', 
]
surgeries = [ # surgeries and padding/tucking
    # transmascs only
    'top surgery', 

    # transfemmes only
    'breast augmentation', 
    'breast reduction or mastectomy', 
    'padded bra', 

    # transmascs only
    'hysterectomy', 

    # both
    'crotch volume', 
    'other surgery', 
]
bodytypes = [ # body type info
    'plus-size', 
    'extra tall', 
    'extra short', 
    # transmascs only
    'very muscular', 
]
standard_sizing = [ # relationship to standard sizing
    'did you shop in birth sex aisle pre-transition and remember your size(s)', 
    'pre-transition sizes', 

    'how well did standard sizing fit pre-transition', 
    'how did that change', 
]
fit_issues = [ # fit issues
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
    'other fit issues', 
]
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

def order_columns(input_df:pd.DataFrame):
    """
    takes a df with unified columns

    returns it in an order that integrates new columns into a sensible order
    """
    new_df = input_df.copy()

    new_df = new_df.get(
        general + HRT + surgeries + bodytypes + standard_sizing + fit_issues + chest_meas + meas
    )

    return new_df
