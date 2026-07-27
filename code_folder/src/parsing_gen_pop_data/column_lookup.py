"""lookup for column names and what they refer to in different datasets"""

ANSUR_I = {
    "all":[
        "SUBJECT_NUMBER", # ID
        "AB-EXT-DEPTH-SIT", # abdominal extension depth, sitting
        "ACROMION_HT", # acromial height
        "ACR_HT-SIT", # height, sitting
        "ACR-RADL_LNTH", # acromion-radiale length
        "ANKLE_CIRC", # ankle circumference -> ankle circumference
        "AXILLA_HT", # axilla height
        "ARM_CIRC-AXILLARY", # axillary arm circumference
        "FOOT_CIRC", # foot circumference (??)
        "INSTEP_LNTH", # length (??)
        "BIACROMIAL_BRTH", # biacromial breadth -> back width
        "ARMCIRCBCPS_FLEX", # biceps circumference, flexed -> biceps circumference
        "BIDELTOID_BRTH", # bideltoid breadth -> shoulder width back
        "BIMALLEOLAR_BRTH", # bimalleolar breadth
        "BISPINOUS_BRTH", # bispinous breadth
        "BITR_MENTON_ARC", # bitragion chin arc
        "BITR-CORONAL_ARC", # bitragion coronal arc
        "BITR-CRINION_ARC", # bitragion crinion arc
        "BITR-MINIMUM_FRNTAL_ARC", # bitragion frontal arc
        "BITR_SUBMANDIBULAR_ARC", # bitragion submandibular arc
        "BITR_SUBNASALE_ARC", # bitragion subnasale arc
        "BIZYGOMATIC_BRTH", # bizygomatic breadth
        "BUSTPOINT_TO_BUSTPOINT_BRTH", # bustpoint/thelion to bustpoint/thelion breadth
        "BUTTOCK_CIRC", # buttock circumference -> hip circumference
        "BUTT_DEPTH", # buttock depth
        "BUTT_HT", # buttock height
        "BUTT_KNEE_LNTH", # buttock-knee length
        "BUTT_POPLITEAL_LNTH", # buttock-popliteal length
        "CALF_CIRC", # calf circumference -> calf circumference
        "CALF_HT", # calf height
        "CERVIC_HT", # cervicale height -> nape to floor
        "CERVIC_HT_SITTING", # cervicale height, sitting
        "CHEST_BRTH", # chest breadth
        "CHEST_CIRC", # chest circumference -> chest circumference
        "CHEST_CIRC_AT_SCYE", # chest circumference at scye -> overbust
        "CHEST_CIRC-BELOW_BUST_", # chest circumference below breast -> underbust
        "CHEST_DEPTH", # chest depth
        "CHEST_HT", # chest height
        "CROTCH_HT", # crotch height -> inseam
        "CROTCH_UMBILICUS", # crotch length (omphalion)
        "CROTCH_NAT_WAIST", # crotch length (natural indentation) -> crotch length (waist to waist going between legs)
        "CRTCH_PST_NATURAL", # crotch length, posterior (natural indentation)
        "CRTCH_PST_OMPHALION", # crotch, posterior (omphalion)
        "EAR_BRTH", # ear breadth
        "EAR_LNTH", # ear length
        "EAR_LNTH-ABOVE_TRAGION", # ear length above tragion
        "EAR_PROTRUSION", # ear protrusion
        "ELBOW_CIRC-EXTENDED", # elbow circumference -> elbow circumference
        "ELBOW_REST_HT", # elbow rest height
        "EYE_HT-SITTING", # eye height, sitting
        "FOOT_BRTH", # foot breadth, horizontal (?)
        "FOOT_LNTH", # foot length
        "FOREARM_CIRC-FLEXED", # forearm circumference, flexed
        "FOREARM_TO_FOREARM_BRTH", # forearm-forearm breadth
        "FOREARM-HAND_LENTH", # forearm-hand length
        "FUNCTIONAL_LEG_LNTH", # functional leg length
        "GLUTEAL_FURROW_HT", # glutteal furrow height
        "HAND_BRTH_AT_METACARPALE", # hand breadth
        "HAND_CIRC_AT_METACARPALE", # hand circumference -> is without thumb, so not sleeve entry we measured
        "HAND_LNTH", # hand length
        "HEAD_BRTH", # head breadth
        "HEAD_CIRC", # head circumference
        "HEAD_LNTH", # head length
        "HEEL_ANKLE_CIRC", # heel ankle circumference -> foot entry
        "HEEL_BRTH", # heel breadth
        "HIP_BRTH", # hip breadth
        "HIP_BRTH_SITTING", # hip breadth, sitting
        "ILIOCRISTALE_HT", # iliocristale height
        "INTERPUPILLARY_DIST", # interpupillary distance
        "INTRSCY_DIST", # interscye distance
        "INTRSCY_MID_DIST", # interscye distance 
            # -> they both look like back width idk (69) is a bit lower than the other one, 
            # so I guess (70) is the correct one??
        "KNEE_CIRC", # knee circumference -> knee circumference
        "PATELLA-MID_HT", # knee height, midpatella -> knee height
        "KNEE_HT_-_SITTING", # knee height, sitting
        "LATERAL_FEMORAL_EPICONDYLE_HT", # lateral femoral epicondyle height
        "LATERAL-MALLEOUS_HT", # lateral malleous height -> closest to ankle height
        "THIGH_CIRC-DISTAL", # thigh circumference (further away (from the body??))
        "MENTON_TO_NASAL_ROOT_DEP_LNTH", # menton-sellion length (?)
        "MIDSHOULDER_HT-SITTING", # midshoulder height, sitting
        "NECK_TO_BUSTPOINT_LNTH", # neck-bustpoint/thelion length
        "NECK_CIRC-OVER_LARYNX", # neck circumference -> neck circumference
        "NECK_CIRC-BASE", # neck circumference, base -> neck base circumference
        "NECK_HT-LATERAL", # neck height (lateral) -> this is also nape to floor actually
        "OVRHD_REACH", # overhead fingertip reach
        "OVRHD_EXT_REACH", # overhead fingertip reach, extended
        "OVRHD_SIT_REACH", # overhead fingertip reach, sitting
        "POPLITEAL_HT-SITTING", # popliteal height, sitting
        "RADIALE-STYLION_LNTH", # radiale-stylion length
        "SCYE_CIRC_OVER_ACROMION", # scye circumference -> added up version of our scye measurements basically
        "SCYE_DEPTH", # scye depth
        "SHOULDER_CIRC", # shoulder circumference
        "SHOULDER_ELBOW_LNTH", # shoulder-elbow length -> shoulder elbow distance
        "SHOULDER_LNTH", # shoulder length -> shoulder
        "SITTING_HT", # sitting height
        "SPINE_TO_ELBOW_LNTH_(SL)", # sleeve length: spine-elbow
        "SPINE_TO_SCYE_LNTH_(SL)", # sleeve length: spine-scye -> half of back width (with arms out)
        "SPINE_TO_WRIST_LNTH_(SL)", # sleeve length: spine-wrist
        "SLEEVE-OUTSEAM_LNTH", # sleeve outseam -> arm length
        "SPAN", # span
        "STATURE", # stature -> height
        "STRAP_LNTH", # strap length
        "SUPRASTERNALE_HT", # suprasternale height
        "TENTH_RIB", # tenth rib height
        "THIGH_CIRC-PROXIMAL", # thigh circumference (closer (to the body?)) -> I assume this is the one we want
        "THIGH_CLEARANCE", # thigh clearance
        "THUMB_BRTH", # thumb breadth
        "THUMB-TIP_REACH", # thumbtip reach 
        "TROCHANTERION_HT", # tronchanteric height
        "VERTICAL_TRUNK_CIRC", # vertical trunk circumference (ascc or usa?? there seems to be a diff between genders?)
        "WAIST_NAT_LNTH", # waist back length (natural indentation) -> nape to nat waist
        "WAIST_OMPH_LNTH", # waist back length (omphalion)
        "WAIST_BRTH_OMPHALION", # waist breadth (omphalion)
        "WAIST_CIRC_NATURAL", # waist circumference (natural indentation) -> natural waist circumference
        "WAIST_CIRC-OMPHALION", # waist circumference (omphalion) 
            # -> this is not actual low waist bc omphalion means like belly button 
            # but is indicated as male pants waist on diagrams
        "WAIST_DEPTH-OMPHALION", # waist depth (omphalion)
        "WST_NAT_FRONT", # waist front length (natural indentation) -> clavicle to nat waist
        "WST_OMP_FRONT", # waist front length (omphalion)
        "WAIST_HT_NATURAL", # waist height (natural indentation) -> outseam to natural waist
        "WAIST_HT-OMPHALION", # waist height (omphalion)
        "WAIST_HT_SIT_NATURAL", # waist height, sitting (natural indentation) -> rise to natural waist
        "WAIST_HT-UMBILICUS-SITTING", # waist height, sitting
        "WAIST_HIP_LNTH", # waist-hip length -> omphalion waist to hip
        "WAIST_NATURAL_TO_WAIST_UMBILICUS", # waist (natural indentation) to waist (omphalion) length
        "WEIGHT", # weight
        "WRIST_TO_CENTER_OF_GRIP_LNTH", # wrist-center of grip length
        "WRIST_CIRC-STYLION", # wrist circumference -> wrist circumference
        "WRIST_HT", # wrist height
        "WRIST_HT-SITTING", # wrist height, sitting
        "WRIST_TO_INDEX_FINGER_LNTH", # wrist-index finger length
        "WRIST_TO_THUMBTIP_LNTH", # wrist-thumbtip length
        "WRST_LNTH_TO_WALL", # wrist-wall length
        "WRST_EXT_TO_WALL" # wrist-wall length, extended
    ],
    "to_compare":[
        "SUBJECT_NUMBER", # ID
        "ANKLE_CIRC", # ankle circumference -> ankle circumference
        "BIACROMIAL_BRTH", # biacromial breadth -> back width
        "ARMCIRCBCPS_FLEX", # biceps circumference, flexed -> biceps circumference
        "BIDELTOID_BRTH", # bideltoid breadth -> shoulder width back
        "BUTTOCK_CIRC", # buttock circumference -> hip circumference
        "CALF_CIRC", # calf circumference -> calf circumference
        "CERVIC_HT", # cervicale height -> nape to floor
        "CHEST_CIRC", # chest circumference -> chest circumference
        "CHEST_CIRC_AT_SCYE", # chest circumference at scye -> overbust
        "CHEST_CIRC-BELOW_BUST_", # chest circumference below breast -> underbust
        "CROTCH_HT", # crotch height -> inseam
        "CROTCH_UMBILICUS", # crotch length (omphalion)
        "CROTCH_NAT_WAIST", # crotch length (natural indentation) -> crotch length (waist to waist going between legs)
        "CRTCH_PST_NATURAL", # crotch length, posterior (natural indentation)
        "CRTCH_PST_OMPHALION", # crotch length, posterior (omphalion)
        "ELBOW_CIRC-EXTENDED", # elbow circumference -> elbow circumference
        "HAND_CIRC_AT_METACARPALE", # hand circumference -> is without thumb, so not sleeve entry we measured
        "HEAD_CIRC", # head circumference -> head circumference
        "HEEL_ANKLE_CIRC", # heel ankle circumference -> foot entry
        "INTRSCY_DIST", # interscye distance
        "INTRSCY_MID_DIST", # interscye distance 
            # -> they both look like back width idk (69) is a bit lower than the other one, 
            # so I guess (70) is the correct one??
        "KNEE_CIRC", # knee circumference -> knee circumference
        "PATELLA-MID_HT", # knee height, midpatella -> knee height
        "LATERAL-MALLEOUS_HT", # lateral malleous height -> closest to ankle height
        "NECK_CIRC-OVER_LARYNX", # neck circumference -> neck circumference
        "NECK_CIRC-BASE", # neck circumference, base -> neck base circumference
        "NECK_HT-LATERAL", # neck height (lateral) -> this is also nape to floor actually
        "SCYE_CIRC_OVER_ACROMION", # scye circumference -> added up version of our scye measurements basically
        "SCYE_DEPTH", # scye depth
        "SHOULDER_ELBOW_LNTH", # shoulder-elbow length -> shoulder elbow distance
        "SHOULDER_LNTH", # shoulder length -> shoulder
        "SPINE_TO_SCYE_LNTH_(SL)", # sleeve length: spine-scye -> half of back width (with arms out)
        "SLEEVE-OUTSEAM_LNTH", # sleeve outseam -> arm length
        "STATURE", # stature -> height
        "THIGH_CIRC-PROXIMAL", # thigh circumference (closer (to the body?)) -> I assume this is the one we want
        "WAIST_NAT_LNTH", # waist back length (natural indentation) -> nape to nat waist
        "WAIST_OMPH_LNTH", # waist back length (omphalion)
        "WAIST_CIRC_NATURAL", # waist circumference (natural indentation) -> natural waist circumference
        "WAIST_CIRC-OMPHALION", # waist circumference (omphalion) 
            # -> this is not actual low waist bc omphalion means like belly button 
            # but is indicated as male pants waist on diagrams
        "WST_NAT_FRONT", # waist front length (natural indentation) -> clavicle to nat waist
        "WST_OMP_FRONT", # waist front length (omphalion)
        "WAIST_HT_NATURAL", # waist height (natural indentation) -> outseam to natural waist
        "WAIST_HT-OMPHALION", # waist height (omphalion)
        "WAIST_HT_SIT_NATURAL", # waist height, sitting (natural indentation) -> rise to natural waist
        "WAIST_HIP_LNTH", # waist-hip length -> omphalion waist to hip
        "WAIST_NATURAL_TO_WAIST_UMBILICUS", # waist (natural indentation) to waist (omphalion) length
        "WEIGHT", # weight
        "WRIST_CIRC-STYLION", # wrist circumference -> wrist circumference
    ],
    "renaming_dict":{
        "SUBJECT_NUMBER": "UID",
        "ANKLE_CIRC": "ankle circumference",
        "BIACROMIAL_BRTH": "back width (shoulder blades)",
        "ARMCIRCBCPS_FLEX": "biceps circumference",
        "BIDELTOID_BRTH": "shoulder width (back)",
        "BUTTOCK_CIRC": "hip circumference",
        "CALF_CIRC": "calf circumference", 
        "CERVIC_HT": "nape to floor (1)",
        "CHEST_CIRC": "chest circumference",
        "CHEST_CIRC_AT_SCYE": "overbust",
        "CHEST_CIRC-BELOW_BUST_": "underbust",
        "CROTCH_HT": "inseam",
        "CROTCH_UMBILICUS": "crotch length (low waist)", 
        "CROTCH_NAT_WAIST": "crotch length (natural waist)",
        "ELBOW_CIRC-EXTENDED": "elbow circumference",
        "HAND_CIRC_AT_METACARPALE": "hand circumference (without thumb)",
        "HEAD_CIRC": "head circumference",
        "HEEL_ANKLE_CIRC": "foot entry",
        "INTRSCY_DIST": "back width (high)",
        "INTRSCY_MID_DIST": "back width (low)",
        "KNEE_CIRC": "knee circumference",
        "PATELLA-MID_HT": "knee to floor",
        "LATERAL-MALLEOUS_HT": "ankle to floor",
        "NECK_CIRC-OVER_LARYNX": "neck circumference",
        "NECK_CIRC-BASE": "base of neck circumference",
        "NECK_HT-LATERAL": "nape to floor (2)",
        "SCYE_CIRC_OVER_ACROMION": "scye circumference",
        "SHOULDER_ELBOW_LNTH": "shoulder to elbow",
        "SHOULDER_LNTH": "shoulder",
        "SPINE_TO_SCYE_LNTH_(SL)": "half back width (arms out)",
        "SLEEVE-OUTSEAM_LNTH": "arm length",
        "STATURE": "height",
        "THIGH_CIRC-PROXIMAL": "thigh circumference",
        "WAIST_NAT_LNTH": "distance from nape of the neck to natural waist (back)",
        "WAIST_OMPH_LNTH": "distance from nape of the neck to low waist (back)",
        "WAIST_CIRC_NATURAL": "natural waist circumference",
        "WAIST_CIRC-OMPHALION": "low waist circumference",
        "WST_NAT_FRONT": "distance from clavicle to natural waist (front)",
        "WST_OMP_FRONT": "distance from clavicle to low waist (front)", # waist front length (omphalion)
        "WAIST_HT_NATURAL": "outseam to natural waist",
        "WAIST_HT-OMPHALION": "outseam to low waist",
        "WAIST_HT_SIT_NATURAL": "rise to natural waist",
        "WAIST_HIP_LNTH": "low waist to hip distance",
        "WAIST_NATURAL_TO_WAIST_UMBILICUS": "natural waist to low waist distance",
        "WEIGHT": "weight",
        "WRIST_CIRC-STYLION": "wrist circumference", 
    }
}
ANSUR_II = {
    "all": [
        "subjectid", # 
        "abdominalextensiondepthsitting", # 
        "acromialheight", # 
        "acromionradialelength", # 
        "anklecircumference", #
        "axillaheight", # 
        "balloffootcircumference", # 
        "balloffootlength", # 
        "biacromialbreadth", # 
        "bicepscircumferenceflexed", # 
        "bicristalbreadth", # 
        "bideltoidbreadth", # 
        "bimalleolarbreadth", # 
        "bitragionchinarc", # 
        "bitragionsubmandibulararc", # 
        "bizygomaticbreadth", # 
        "buttockcircumference", # 
        "buttockdepth", # 
        "buttockheight", # 
        "buttockkneelength", # 
        "buttockpopliteallength", # 
        "calfcircumference", # 
        "cervicaleheight", # 
        "chestbreadth", # 
        "chestcircumference", # 
        "chestdepth", # 
        "chestheight", # 
        "crotchheight", # 
        "crotchlengthomphalion", # 
        "crotchlengthposterioromphalion", # 
        "earbreadth", # 
        "earlength", # 
        "earprotrusion", # 
        "elbowrestheight", # 
        "eyeheightsitting", # 
        "footbreadthhorizontal", # 
        "footlength", # 
        "forearmcenterofgriplength", # 
        "forearmcircumferenceflexed", # 
        "forearmforearmbreadth", # 
        "forearmhandlength", # 
        "functionalleglength", # 
        "handbreadth", # 
        "handcircumference", # 
        "handlength", # 
        "headbreadth", # 
        "headcircumference", # 
        "headlength", # 
        "heelanklecircumference", # 
        "heelbreadth", # 
        "hipbreadth", # 
        "hipbreadthsitting", # 
        "iliocristaleheight", # 
        "interpupillarybreadth", # 
        "interscyei", # 
        "interscyeii", # 
        "kneeheightmidpatella", # 
        "kneeheightsitting", # 
        "lateralfemoralepicondyleheight", # 
        "lateralmalleolusheight", # 
        "lowerthighcircumference", # 
        "mentonsellionlength", # 
        "neckcircumference", # 
        "neckcircumferencebase", # 
        "overheadfingertipreachsitting", # 
        "palmlength", # 
        "poplitealheight", # 
        "radialestylionlength", # 
        "shouldercircumference", # 
        "shoulderelbowlength", # 
        "shoulderlength", # 
        "sittingheight", # 
        "sleevelengthspinewrist", # 
        "sleeveoutseam", # 
        "span", # 
        "stature", # 
        "suprasternaleheight", # 
        "tenthribheight", # 
        "thighcircumference", # 
        "thighclearance", # 
        "thumbtipreach", # 
        "tibialheight", # 
        "tragiontopofhead", # 
        "trochanterionheight", # 
        "verticaltrunkcircumferenceusa", # 
        "waistbacklength", # 
        "waistbreadth", # 
        "waistcircumference", # 
        "waistdepth", # 
        "waistfrontlengthsitting", # 
        "waistheightomphalion", # 
        "weightkg", # 
        "wristcircumference", # 
        "wristheight", # 
        "Gender", # 
        "Date", # 
        "Installation", # 
        "Component", # 
        "Branch", # 
        "PrimaryMOS", # 
        "SubjectsBirthLocation", # 
        "SubjectNumericRace", # 
        "Ethnicity", # 
        "DODRace", # 
        "Age", # 
        "Heightin", # 
        "Weightlbs", # 
        "WritingPreference"
    ],
    "to_compare": [
        "subjectid", # ID
        "anklecircumference", # -> ankle circumference
        "biacromialbreadth", # -> back width
        "bicepscircumferenceflexed", # -> biceps circumference
        "bideltoidbreadth", # -> shoulder width back
        "buttockcircumference", # -> hip circumference
        "calfcircumference", # -> calf circumference
        "cervicaleheight", # -> nape to floor
        "chestcircumference", # -> chest circumference
        "crotchheight", # -> inseam
        "crotchlengthomphalion", # -> crotch length omphalion waist to waist
        "handcircumference", # -> closest to hand circumference
        "headcircumference", # -> head circumference
        "heelanklecircumference", # -> foot entry
        "interscyei", # -> also back width but for actual scyes
        "interscyeii", # 
        "kneeheightmidpatella", # -> knee height
        "lateralmalleolusheight", # -> closest to ankle height
        "neckcircumference", # -> neck circumference
        "neckcircumferencebase", # -> base of neck circumference
        "shoulderelbowlength", # -> shoulder elbow distance
        "shoulderlength", # -> shoulder
        "sleeveoutseam", # -> arm length
        "stature", # -> height
        "thighcircumference", # -> thigh circumference
        "waistbacklength", # 
        "waistcircumference", # -> which waist?
        "weightkg", # weight
        "wristcircumference", # 
        "Gender", # 
        "Age", # 
        "Heightin", # 
    ],
    "renaming_dict":{
        "subjectid":"UID", # ID
        "anklecircumference":"ankle circumference",
        "biacromialbreadth":"back width (shoulder blades)",
        "bicepscircumferenceflexed":"biceps circumference",
        "bideltoidbreadth":"shoulder width (back)",
        "buttockcircumference":"hip circumference",
        "calfcircumference":"calf circumference",
        "cervicaleheight":"nape to floor (1)",
        "chestcircumference":"chest circumference",
        "crotchheight":"inseam",
        "crotchlengthomphalion":"crotch length (low waist)",
        "handcircumference":"hand circumference (without thumb)",
        "headcircumference":"head circumference",
        "heelanklecircumference":"foot entry",
        "interscyei":"back width (high)",
        "interscyeii":"back width (low)",
        "kneeheightmidpatella":"knee to floor",
        "lateralmalleolusheight":"ankle to floor",
        "neckcircumference":"neck circumference",
        "neckcircumferencebase":"base of neck circumference",
        "shoulderelbowlength":"shoulder to elbow",
        "shoulderlength":"shoulder",
        "sleeveoutseam":"arm length",
        "stature":"height",
        "thighcircumference":"thigh circumference",
        "waistbacklength":"distance from nape of the neck to waist (back)",
        "waistcircumference":"waist circumference",
        "weightkg":"weight",
        "wristcircumference":"wrist circumference",
        "Age":"age",
    }
}