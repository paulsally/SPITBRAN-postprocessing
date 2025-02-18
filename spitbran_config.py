from pathlib import Path

# Colours
cfg_colours = {
    "c-rean": "#76C893",
    "model": "#168AAD",
    "model_avg": "#1E6091"
}

# Geo Location and depth
cfg_latitude = 44.0
cfg_longitude = 9.0
cfg_depth_index = 0

# Set the paths to CMEMS and MITgcm-BFM base data directory
cfg_data_base_dirs = {
    #"c-rean": r"/OCEANASTORE/database/CMEMS/rean-d",
    "c-rean": Path(r"~/SPITBRAN/DATA/CMEMS/rean-d").expanduser(),
    "m": Path(r"/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs").expanduser(),
}

# Set associations between variable name and file name
cfg_var_filename_map = {
    "thetao": {
        "c-rean": "tem",
        "m": "TEMP",
    },
    "so": {
        "c-rean": "sal",
        "m": "PSAL",
    },
}

# Set the default min max values for the color bar scale
cfg_var_min_max = {
    "thetao": {
        "c-rean": [11, 17],
        "m": [11, 17]
    },
    "so": {
        "c-rean": [36, 40],
        "m": [36, 40]
    }
}
