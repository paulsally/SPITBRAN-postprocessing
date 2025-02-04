# Colours
cfg_colours = {
    "ref": "#76C893",
    "model": "#168AAD",
    "model_avg": "#1E6091"
}

# Geo Location and depth
cfg_latitude = 44.0
cfg_longitude = 9.0
cfg_depth_index = 0

# Set the paths to CMEMS and MITgcm-BFM base data directory
cfg_data_base_dirs = {
    "c": r"/OCEANASTORE/database/CMEMS/rean-d",
    "m": r"/OCEANASTORE/progetti/spitbran2"
}

# Set associations between variable name and file name
cfg_var_filename_map = {
    "thetao": {
        "c": "tem",
        "m": "TEMP",
    },
    "cur": {
        "c": "cur",
        "m": "RFVL",
    },
    "so": {
        "c": "sal",
        "m": "PSAL",
    },
}
