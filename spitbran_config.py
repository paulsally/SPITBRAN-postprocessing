from datetime import datetime

# Colours
cfg_colours = {
    "ref": "#76C893",
    "model": "#168AAD",
    "model_avg": "#1E6091"
}

# Geo Location and depth
cfg_latitude = 44.0
cfg_longitude = 9.0
# lat_idx = 250
# lon_idx = 380
cfg_depth_index = 0

# Set the paths to CMEMS and MITgcm-BFM base data directory
cfg_data_base_dirs = {
    "c": r"/OCEANASTORE/database/CMEMS/rean-d",
    "m": r"/OCEANASTORE/progetti/spitbran2/2013"
}

# Set the reference dates for the datasets
cfg_base_times = {
    "c": datetime(1900, 1, 1, 0, 0, 0),
    "m": datetime(1970, 1, 1, 0, 0, 0),
}

# Set the time units for datasets
cfg_base_time_unit = {
    "c": "seconds",
    "m": "minutes",
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


