# Import necessary libraries
import numpy as np 
import json
import os 
import sys
import random
import math

# Import specific functions from a utility module for pose alignment
from utils_pose_alignment import get_urdf_path, convert_gripper_to_aligned_pose, convert_aligned_to_gripper_pose

# Set directories for test and JSON files
test_dir = r'/home/dm/Documents/Dataset/hithand_transfered'
json_directory = (r'/home/dm/Documents/Dataset/graspit_grasps/Allegro')

# Get list of all JSON files in the directory
json_files = [pos_json for pos_json in os.listdir(json_directory) if pos_json.endswith('.json')]

# Threshold and initialize object set
th = 3 
objects = set([])

# Dictionary to store information for different grippers
grippers= {
    # "fetch_gripper": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "franka_panda": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "sawyer": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "wsg_50": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "Barrett": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "robotiq_3finger": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "jaco_robot": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "Allegro": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "shadow_hand": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "HumanHand": {'object_id':[], 'pose':[], 'og_gripper':[]},
    # "h5_hand": {'object_id':[], 'pose':[], 'og_gripper':[]},
    "hithand": {'object_id':[], 'pose':[], 'og_gripper':[]},
}

# Loop through each JSON file
i = 0
for file in json_files:
    json_path = os.path.join(json_directory, file)

    # Open and load JSON file into dictionary
    fd = open(json_path)
    dict = json.load(fd)
    
    # Add object ID to the set of objects
    objects.add(dict['object_id'])

    # Filter poses based on fall_time threshold
    tmp = np.array(dict['fall_time'])
    pose = np.array(dict['pose'])
    
    pose = pose[tmp >= th]
    
    # Randomly sample 50 or fewer poses
    x = len(pose)
    y = min(x, 50)
    samples = random.sample(range(x), y)
    pose = pose[samples]
    
    # Loop through each gripper to store relevant information
    for gripper in grippers:
        if gripper == dict['gripper']:
            continue

        # Store object ID, original gripper, and pose for each gripper
        new_pose = pose
        grippers[gripper]['object_id'] += ([dict['object_id']] * len(pose))
        grippers[gripper]['og_gripper'] += ([dict['gripper']] * len(pose))
        grippers[gripper]['pose'] += (pose.tolist())

    i += 1

# Loop through each gripper and create a new JSON file with transformed poses
for gripper in grippers:
    if len(grippers[gripper]['object_id']) == 0:
        continue

    # Define object set and gripper directory
    gripper_dir = os.path.join(test_dir, gripper)
    # object_set = {"Animal_Planet_Foam_2Headed_Dragon", "Racoon", "Nestle_Nips_Hard_Candy_Peanut_Butter"}
    object_set = {
    "11pro_SL_TRX_FG",
    "2_of_Jenga_Classic_Game",
    "3D_Dollhouse_Happy_Brother",
    "3D_Dollhouse_Lamp",
    "3D_Dollhouse_Refrigerator",
    "3D_Dollhouse_Sink",
    "3D_Dollhouse_Sofa",
    "3D_Dollhouse_Swing",
    "3D_Dollhouse_TablePurple",
    "3M_Antislip_Surfacing_Light_Duty_White",
    "45oz_RAMEKIN_ASST_DEEP_COLORS",
    "5_HTP",
    "ACE_Coffee_Mug_Kristen_16_oz_cup",
    "adiZero_Slide_2_SC",
    "Air_Hogs_Wind_Flyers_Set_Airplane_Red",
    "AllergenFree_JarroDophilus",
    "AMBERLIGHT_UP_W",
    "Android_Figure_Chrome",
    "Android_Figure_Panda",
    "Animal_Crossing_New_Leaf_Nintendo_3DS_Game",
    "Animal_Planet_Foam_2Headed_Dragon",
    "Apples_to_Apples_Kids_Edition",
    "Arm_Hammer_Diaper_Pail_Refills_12_Pack_MFWkmoweejt",
    "Aroma_Stainless_Steel_Milk_Frother_2_Cup",
    "ASICS_GEL1140V_WhiteBlackSilver",
    "Asus_80211ac_DualBand_Gigabit_Wireless_Router_RTAC68R",
    "Avengers_Thor_PLlrpYniaeB",
    "Balderdash_Game",
    "Beetle_Adventure_Racing_Nintendo_64",
    "Beta_Glucan",
    "Beyonc_Life_is_But_a_Dream_DVD",
    "BIA_Cordon_Bleu_White_Porcelain_Utensil_Holder_900028",
    "BIA_Porcelain_Ramekin_With_Glazed_Rim_35_45_oz_cup",
    "Big_Dot_Aqua_Pencil_Case",
    "Big_O_Sponges_Assorted_Cellulose_12_pack",
    "Black_and_Decker_PBJ2000_FusionBlade_Blender_Jars",
    "Black_and_Decker_TR3500SD_2Slice_Toaster",
    "BlackBlack_Nintendo_3DSXL",
    "Black_Decker_CM2035B_12Cup_Thermal_Coffeemaker",
    "Black_Decker_Stainless_Steel_Toaster_4_Slice",
    "Black_Elderberry_Syrup_54_oz_Gaia_Herbs",
    "Black_Forest_Fruit_Snacks_28_Pack_Grape",
    "Bradshaw_International_11642_7_Qt_MP_Plastic_Bowl",
    "Breyer_Horse_Of_The_Year_2015",
    "Brisk_Iced_Tea_Lemon_12_12_fl_oz_355_ml_cans_144_fl_oz_426_lt",
    "Brother_Ink_Cartridge_Magenta_LC75M",
    "Brother_Printing_Cartridge_PC501",
    "Calphalon_Kitchen_Essentials_12_Cast_Iron_Fry_Pan_Black",
    "Canon_225226_Ink_Cartridges_BlackColor_Cyan_Magenta_Yellow_6_count",
    "Central_Garden_Flower_Pot_Goo_425",
    "Chefmate_8_Frypan",
    "Chef_Style_Round_Cake_Pan_9_inch_pan",
    "Chelsea_BlkHeelPMP_DwxLtZNxLZZ",
    "CLIMACOOL_BOAT_BREEZE_IE6CyqSaDwN",
    "Closetmaid_Premium_Fabric_Cube_Red",
    "Clue_Board_Game_Classic_Edition",
    "Cole_Hardware_Antislip_Surfacing_Material_White",
    "Cole_Hardware_Bowl_Scirocco_YellowBlue",
    "Cole_Hardware_Butter_Dish_Square_Red",
    "Cole_Hardware_Deep_Bowl_Good_Earth_1075",
    "Cole_Hardware_Dishtowel_Blue",
    "Cole_Hardware_Dishtowel_BlueWhite",
    "Cole_Hardware_Dishtowel_Multicolors",
    "Cole_Hardware_Dishtowel_Red",
    "Cole_Hardware_Dishtowel_Stripe",
    "Cole_Hardware_Electric_Pot_Assortment_55",
    "Cole_Hardware_Hammer_Black",
    "Cole_Hardware_Mini_Honey_Dipper",
    "Cole_Hardware_Mug_Classic_Blue",
    "Cole_Hardware_Plant_Saucer_Brown_125",
    "Cole_Hardware_Saucer_Electric",
    "Cole_Hardware_Saucer_Glazed_6",
    "Cole_Hardware_School_Bell_Solid_Brass_38",
    "Connect_4_Launchers",
    "Corningware_CW_by_Corningware_3qt_Oblong_Casserole_Dish_Blue",
    "Craftsman_Grip_Screwdriver_Phillips_Cushion",
    "Crayola_Bonus_64_Crayons",
    "Creatine_Monohydrate",
    "Crosley_Alarm_Clock_Vintage_Metal",
    "Crunch_Girl_Scouts_Candy_Bars_Peanut_Butter_Creme_78_oz_box",
    "Curver_Storage_Bin_Black_Small",
    "Design_Ideas_Drawer_Store_Organizer",
    "Deskstar_Desk_Top_Hard_Drive_1_TB",
    "Diamond_Visions_Scissors_Red",
    "Diet_Pepsi_Soda_Cola12_Pack_12_oz_Cans",
    "Digital_Camo_Double_Decker_Lunch_Bag",
    "Dino_3",
    "Dino_4",
    "Dino_5",
    "Dixie_10_ounce_Bowls_35_ct",
    "Dog",
    "Don_Franciscos_Gourmet_Coffee_Medium_Decaf_100_Colombian_12_oz_340_g",
    "Down_To_Earth_Ceramic_Orchid_Pot_Asst_Blue",
    "Down_To_Earth_Orchid_Pot_Ceramic_Red",
    "DPC_Handmade_Hat_Brown",
    "DPC_tropical_Trends_Hat",
    "DRAGON_W",
    "Ecoforms_Cup_B4_SAN",
    "Ecoforms_Garden_Pot_GP16ATurquois",
    "Ecoforms_Plant_Bowl_Atlas_Low",
    "Ecoforms_Plant_Bowl_Turquoise_7",
    "Ecoforms_Plant_Container_12_Pot_Nova",
    "Ecoforms_Plant_Container_B4_Har",
    "Ecoforms_Plant_Container_GP16AMOCHA",
    "Ecoforms_Plant_Container_QP6CORAL",
    "Ecoforms_Plant_Container_S24NATURAL",
    "Ecoforms_Plant_Plate_S11Turquoise",
    "Ecoforms_Plant_Pot_GP9AAvocado",
    "Ecoforms_Plant_Saucer_SQ1HARVEST",
    "Ecoforms_Pot_Nova_6_Turquoise",
    "Ecoforms_Saucer_SQ3_Turquoise",
    "Elephant",
    "Embark_Lunch_Cooler_Blue",
    "Envision_Home_Dish_Drying_Mat_Red_6_x_18",
    "Final_Fantasy_XIV_A_Realm_Reborn_60Day_Subscription",
    "Firefly_Clue_Board_Game",
    "FisherPrice_Make_A_Match_Game_Thomas_Friends",
    "Fresca_Peach_Citrus_Sparkling_Flavored_Soda_12_PK",
    "Frozen_Olafs_In_Trouble_PopOMatic_Game",
    "Fujifilm_instax_SHARE_SP1_10_photos",
    "Full_Circle_Happy_Scraps_Out_Collector_Gray",
    "GARDEN_SWING",
    "Google_Cardboard_Original_package",
    "GoPro_HERO3_Composite_Cable",
    "Granimals_20_Wooden_ABC_Blocks_Wagon",
    "Granimals_20_Wooden_ABC_Blocks_Wagon_g2TinmUGGHI",
    "Great_Jones_Wingtip_kAqSg6EgG0I",
    "Grreat_Choice_Dog_Double_Dish_Plastic_Blue",
    "Grreatv_Choice_Dog_Bowl_Gray_Bones_Plastic_20_fl_oz_total",
    "HeavyDuty_Flashlight",
    "Hefty_Waste_Basket_Decorative_Bronze_85_liter",
    "Hey_You_Pikachu_Nintendo_64",
    "Hilary",
    "Home_Fashions_Washcloth_Linen",
    "Home_Fashions_Washcloth_Olive_Green",
    "Horses_in_Pink_Pencil_Case",
    "House_of_Cards_The_Complete_First_Season_4_Discs_DVD",
    "HP_1800_Tablet_8GB_7",
    "Hyaluronic_Acid",
    "HyperX_Cloud_II_Headset_Gun_Metal",
    "InterDesign_Over_Door",
    "INTERNATIONAL_PAPER_Willamette_4_Brown_Bag_500Count",
    "IsoRich_Soy",
    "Jansport_School_Backpack_Blue_Streak",
    "Jawbone_UP24_Wireless_Activity_Tracker_Pink_Coral_L",
    "JBL_Charge_Speaker_portable_wireless_wired_Green",
    "Just_For_Men_Mustache_Beard_Brushin_Hair_Color_Gel_Kit_Jet_Black_M60",
    "Kanex_MultiSync_Wireless_Keyboard",
    "Kingston_DT4000MR_G2_Management_Ready_USB_64GB",
    "Kotex_U_Tween_Pads_16_pads",
    "Kotobuki_Saucer_Dragon_Fly",
    "KS_Chocolate_Cube_Box_Assortment_By_Neuhaus_2010_Ounces",
    "LACING_SHEEP",
    "LADYBUG_BEAD",
    "Lenovo_Yoga_2_11",
    "Little_Debbie_Cloud_Cakes_10_ct",
    "Little_Debbie_Donut_Sticks_6_cake_donuts_10_oz_total",
    "Logitech_Ultimate_Ears_Boom_Wireless_Speaker_Night_Black",
    "Lovable_Huggable_Cuddly_Boutique_Teddy_Bear_Beige",
    "Marc_Anthony_Skip_Professional_Oil_of_Morocco_Conditioner_with_Argan_Oil",
    "Marc_Anthony_True_Professional_Oil_of_Morocco_Argan_Oil_Treatment",
    "Marc_Anthony_True_Professional_Strictly_Curls_Curl_Defining_Lotion",
    "Markings_Desk_Caddy",
    "Markings_Letter_Holder",
    "Mens_ASV_Billfish_Boat_Shoe_in_Dark_Brown_Leather_zdHVHXueI3w",
    "Mens_Santa_Cruz_Thong_in_Chocolate_La1fo2mAovE",
    "Mens_Santa_Cruz_Thong_in_Tan_r59C69daRPh",
    "Mist_Wipe_Warmer",
    "NAPA_VALLEY_NAVAJO_SANDAL",
    "Neat_Solutions_Character_Bib_2_pack",
    "Nescafe_Memento_Latte_Caramel_8_08_oz_23_g_packets_64_oz_184_g",
    "NESCAFE_NESCAFE_TC_STKS_DECAF_6_CT",
    "Nescafe_Tasters_Choice_Instant_Coffee_Decaf_House_Blend_Light_7_oz",
    "Nestle_Candy_19_oz_Butterfinger_Singles_116567",
    "Nestle_Carnation_Cinnamon_Coffeecake_Kit_1913OZ",
    "Nestle_Nesquik_Chocolate_Powder_Flavored_Milk_Additive_109_Oz_Canister",
    "Nestle_Nips_Hard_Candy_Peanut_Butter",
    "Nestle_Pure_Life_Exotics_Sparkling_Water_Strawberry_Dragon_Fruit_8_count_12_fl_oz_can",
    "Nestle_Raisinets_Milk_Chocolate_35_oz_992_g",
    "Nestle_Skinny_Cow_Dreamy_Clusters_Candy_Dark_Chocolate_6_pack_1_oz_pouches",
    "Nestl_Skinny_Cow_Heavenly_Crisp_Candy_Bar_Chocolate_Raspberry_6_pack_462_oz_total",
    "Netgear_Ac1750_Router_Wireless_Dual_Band_Gigabit_Router",
    "Netgear_N750_Wireless_Dual_Band_Gigabit_Router",
    "Nikon_1_AW1_w11275mm_Lens_Silver",
    "Nintendo_2DS_Crimson_Red",
    "Nips_Hard_Candy_Rich_Creamy_Butter_Rum_4_oz_1133_g",
    "Nordic_Ware_Original_Bundt_Pan",
    "Now_Designs_Bowl_Akita_Black",
    "Now_Designs_Dish_Towel_Mojave_18_x_28",
    "Now_Designs_Snack_Bags_Bicycle_2_count",
    "Object_REmvBDJStub",
    "Office_Depot_Canon_CLI_221BK_Ink_Cartridge_Black_2946B001",
    "Olive_Kids_Birdie_Lunch_Box",
    "Olive_Kids_Birdie_Munch_n_Lunch",
    "Olive_Kids_Birdie_Pack_n_Snack",
    "Olive_Kids_Birdie_Sidekick_Backpack",
    "Olive_Kids_Butterfly_Garden_Munch_n_Lunch_Bag",
    "Olive_Kids_Butterfly_Garden_Pencil_Case",
    "Olive_Kids_Dinosaur_Land_Munch_n_Lunch",
    "Olive_Kids_Dinosaur_Land_Pack_n_Snack",
    "Olive_Kids_Game_On_Lunch_Box",
    "Olive_Kids_Trains_Planes_Trucks_Munch_n_Lunch_Bag",
    "Orbit_Bubblemint_Mini_Bottle_6_ct",
    "Organic_Whey_Protein_Unflavored",
    "Ortho_Forward_Facing",
    "Ortho_Forward_Facing_3Q6J2oKJD92",
    "Ortho_Forward_Facing_CkAW6rL25xH",
    "Ortho_Forward_Facing_QCaor9ImJ2G",
    "OXO_Cookie_Spatula",
    "OXO_Soft_Works_Can_Opener_SnapLock",
    "Pass_The_Popcorn_Movie_Guessing_Game",
    "Paul_Frank_Dot_Lunch_Box",
    "Pennington_Electric_Pot_Cabana_4",
    "PEPSI_NEXT_CACRV",
    "Perricone_MD_AcylGlutathione_Eye_Lid_Serum",
    "Perricone_MD_Best_of_Perricone_7Piece_Collection_MEGsO6GIsyL",
    "Perricone_MD_Firming_Neck_Therapy_Treatment",
    "Philips_EcoVantage_43_W_Light_Bulbs_Natural_Light_2_pack",
    "Philips_Sonicare_Tooth_Brush_2_count",
    "Phillips_Caplets_Size_24",
    "Phillips_Milk_of_Magnesia_Saline_Laxative_Liquid_Original",
    "Poise_Ultimate_Pads_Long",
    "Polar_Herring_Fillets_Smoked_Peppered_705_oz_total",
    "Pony_C_Clamp_1440",
    "Poppin_File_Sorter_Blue",
    "Provence_Bath_Towel_Royal_Blue",
    "Racoon",
    "Razer_Abyssus_Ambidextrous_Gaming_Mouse",
    "Razer_BlackWidow_Stealth_2014_Keyboard_07VFzIVabgh",
    "Razer_Blackwidow_Tournament_Edition_Keyboard",
    "Razer_BlackWidow_Ultimate_2014_Mechanical_Gaming_Keyboard",
    "Razer_Goliathus_Control_Edition_Small_Soft_Gaming_Mouse_Mat",
    "Razer_Kraken_71_Chroma_headset_Full_size_Black",
    "Razer_Kraken_Pro_headset_Full_size_Black",
    "Razer_Naga_MMO_Gaming_Mouse",
    "Razer_Taipan_Black_Ambidextrous_Gaming_Mouse",
    "Razer_Taipan_White_Ambidextrous_Gaming_Mouse",
    "Reebok_COMFORT_REEFRESH_FLIP",
    "Reebok_DMX_MAX_MANIA_WD_D",
    "Reebok_ZIGSTORM",
    "REEF_BRAIDED_CUSHION",
    "Reef_Star_Cushion_Flipflops_Size_8_Black",
    "Remington_1_12_inch_Hair_Straightener",
    "Remington_TStudio_Hair_Dryer",
    "Remington_TStudio_Silk_Ceramic_Hair_Straightener_2_Inch_Floating_Plates",
    "Retail_Leadership_Summit",
    "Retail_Leadership_Summit_eCT3zqHYIkX",
    "Retail_Leadership_Summit_tQFCizMt6g0",
    "RJ_Rabbit_Easter_Basket_Blue",
    "Room_Essentials_Bowl_Turquiose",
    "Room_Essentials_Fabric_Cube_Lavender",
    "Room_Essentials_Kitchen_Towels_16_x_26_2_count",
    "Room_Essentials_Mug_White_Yellow",
    "Room_Essentials_Salad_Plate_Turquoise",
    "Saccharomyces_Boulardii_MOS_Value_Size",
    "Samsung_CLTC406S_Toner_Cartridge_Cyan_1pack",
    "Santa_Cruz_Mens_G7kQXK7cIky",
    "Sapota_Threshold_4_Ceramic_Round_Planter_Red",
    "Schleich_African_Black_Rhino",
    "Schleich_Allosaurus",
    "Schleich_Bald_Eagle",
    "Schleich_Hereford_Bull",
    "Schleich_Lion_Action_Figure",
    "Schleich_S_Bayala_Unicorn_70432",
    "Schleich_Spinosaurus_Action_Figure",
    "Schleich_Therizinosaurus_ln9cruulPqc",
    "Seagate_1TB_Backup_Plus_portable_drive_Blue",
    "Seagate_3TB_Central_shared_storage",
    "Seagate_Archive_HDD_8_TB_Internal_hard_drive_SATA_6Gbs_35_ST8000AS0002",
    "Sea_to_Summit_Xl_Bowl",
    "Shark",
    "Shaxon_100_Molded_Category_6_RJ45RJ45_Shielded_Patch_Cord_White",
    "Shurtape_Gaffers_Tape_Silver_2_x_60_yd",
    "Smith_Hawken_Woven_BasketTray_Organizer_with_3_Compartments_95_x_9_x_13",
    "Snack_Catcher_Snack_Dispenser",
    "Sootheze_Cold_Therapy_Elephant",
    "Sootheze_Toasty_Orca",
    "Spritz_Easter_Basket_Plastic_Teal",
    "Squirrel",
    "Sterilite_Caddy_Blue_Sky_17_58_x_12_58_x_9_14",
    "Super_Mario_3D_World_Deluxe_Set",
    "Sushi_Mat",
    "Swiss_Miss_Hot_Cocoa_KCups_Milk_Chocolate_12_count",
    "Tag_Dishtowel_18_x_26",
    "Tag_Dishtowel_Basket_Weave_Red_18_x_26",
    "Tag_Dishtowel_Dobby_Stripe_Blue_18_x_26",
    "Tag_Dishtowel_Green",
    "Tag_Dishtowel_Waffle_Gray_Checks_18_x_26",
    "Target_Basket_Medium",
    "TERREX_FAST_X_GTX",
    "The_Coffee_Bean_Tea_Leaf_KCup_Packs_Jasmine_Green_Tea_16_count",
    "Threshold_Bamboo_Ceramic_Soap_Dish",
    "Threshold_Basket_Natural_Finish_Fabric_Liner_Small",
    "Threshold_Bead_Cereal_Bowl_White",
    "Threshold_Bistro_Ceramic_Dinner_Plate_Ruby_Ring",
    "Threshold_Dinner_Plate_Square_Rim_White_Porcelain",
    "Threshold_Hand_Towel_Blue_Medallion_16_x_27",
    "Threshold_Performance_Bath_Sheet_Sandoval_Blue_33_x_63",
    "Threshold_Porcelain_Coffee_Mug_All_Over_Bead_White",
    "Threshold_Porcelain_Pitcher_White",
    "Threshold_Porcelain_Serving_Bowl_Coupe_White",
    "Threshold_Porcelain_Spoon_Rest_White",
    "Threshold_Porcelain_Teapot_White",
    "Threshold_Ramekin_White_Porcelain",
    "Threshold_Salad_Plate_Square_Rim_Porcelain",
    "Threshold_Textured_Damask_Bath_Towel_Pink",
    "Threshold_Tray_Rectangle_Porcelain",
    "Timberland_Mens_Earthkeepers_Stormbuck_Lite_Plain_Toe_Oxford",
    "Top_Paw_Dog_Bow_Bone_Ceramic_13_fl_oz_total",
    "Top_Paw_Dog_Bowl_Blue_Paw_Bone_Ceramic_25_fl_oz_total",
    "Toysmith_Windem_Up_Flippin_Animals_Dog",
    "Toys_R_Us_Treat_Dispenser_Smart_Puzzle_Foobler",
    "Travel_Mate_P_series_Notebook",
    "TriStar_Products_PPC_Power_Pressure_Cooker_XL_in_Black",
    "Twinlab_100_Whey_Protein_Fuel_Chocolate",
    "Ubisoft_RockSmith_Real_Tone_Cable_Xbox_360",
    "UGG_Bailey_Bow_Womens_Clogs_Black_7",
    "US_Army_Stash_Lunch_Bag",
    "Utana_5_Porcelain_Ramekin_Large",
    "Vans_Cereal_Honey_Nut_Crunch_11_oz_box",
    "VANS_FIRE_ROASTED_VEGGIE_CRACKERS_GLUTEN_FREE",
    "Weisshai_Great_White_Shark",
    "Weston_No_22_Cajun_Jerky_Tonic_12_fl_oz_nLj64ZnGwDh",
    "Wilton_Pearlized_Sugar_Sprinkles_525_oz_Gold",
    "Wilton_PreCut_Parchment_Sheets_10_x_15_24_sheets",
    "W_Lou_z0dkC78niiZ",
    "Womens_Betty_Chukka_Boot_in_Grey_Jersey_Sequin",
    "Xyli_Pure_Xylitol",
    "YumYum_D3_Liquid",
    "002_master_chef_can",
    "003_cracker_box",
    "004_sugar_box",
    "005_tomato_soup_can",
    "006_mustard_bottle",
    "007_tuna_fish_can",
    "008_pudding_box",
    "009_gelatin_box",
    "010_potted_meat_can",
    "011_banana",
    "021_bleach_cleanser",
    "024_bowl",
    "025_mug",
    "035_power_drill",
    "037_scissors",
    "052_extra_large_clamp"}

    j = 0
    for obj in object_set:
        # Create output file path
        output_path = os.path.join(test_dir, gripper + '-' + obj + '.json')
        if os.path.exists(output_path): 
            continue
        
        # Initialize new JSON dictionary
        new_json = {}

        # Filter poses and original grippers based on object ID
        obj_arr = np.array(grippers[gripper]['object_id'])
        obj_arr = obj_arr == obj
        
        pose_arr = np.array(grippers[gripper]['pose'])
        tmp_pose = pose_arr[obj_arr]
        
        # Swap columns for quaternion reordering
        tmp_pose[:, [6, 3, 4, 5]] = tmp_pose[:, [3, 4, 5, 6]]

        # Filter original grippers
        og_arr = np.array(grippers[gripper]['og_gripper'])
        tmp_og = og_arr[obj_arr]
        
        # Initialize transformed pose array
        transformed_pose = np.zeros_like(tmp_pose)

        # Transform poses using custom functions for gripper alignment
        c = 0
        for pose in tmp_pose:
            transformed_pose[c] = convert_gripper_to_aligned_pose(pose, tmp_og[c])
            transformed_pose[c] = convert_aligned_to_gripper_pose(transformed_pose[c], gripper)
            c += 1
        
        # Reorder quaternion columns again
        transformed_pose[:, [3, 4, 5, 6]] = transformed_pose[:, [6, 3, 4, 5]]

        # Output the shape of the transformed pose
        pose_shape = transformed_pose.shape
        if pose_shape[0] == 0:
            continue

        # Update new JSON data
        new_json['gripper'] = gripper
        new_json['object_id'] = obj
        new_json['pose'] = transformed_pose.tolist()
        new_json['og_gripper'] = tmp_og.tolist()   

        # Write the transformed data to a new JSON file
        with open(output_path, 'w') as outfile:
            print("Created file: ", output_path)
            json.dump(new_json, outfile)

        j += 1
