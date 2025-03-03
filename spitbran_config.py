# Geo Location and depth (for plotting time series)
cfg_latitude = 44.0
cfg_longitude = 9.0
cfg_depth_index = 0

cfg_datasets = {
    "c-rean": "CMEMS Rean",
    "c-obs": "CMEMS Obs",
    "m": "MITgcm-BFM"
}

# Colours
cfg_colours = {
    "c-rean": "#76C893",
    "c-obs": "#fb8500",
    "m": "#168aad",
    "m_avg": "#1e6091"
}

# Set the paths to CMEMS and MITgcm-BFM base data directory
cfg_data_base_dirs = {
    #"c-rean": r"/OCEANASTORE/database/CMEMS/rean-d",
    "c-rean": "~/SPITBRAN/DATA/CMEMS/rean-d",
    "c-obs": "~/SPITBRAN/DATA/CMEMS/obs",
    "m": "/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs"
}

# Set associations between variable common name and variable name in dataset
cfg_var_name = {
    "temp": {
        "c-rean": "thetao",
        "c-obs": "analysed_sst",
        "m": "thetao",
    },
    "so": {
        "c-rean": "so",
        "c-obs": "--",
        "m": "so",
    },
}
# Set associations between variable name and file name
cfg_var_filename_map = {
    "temp": {
        "c-rean": "tem",
        "c-obs": "tem",
        "m": "TEMP",
    },
    "so": {
        "c-rean": "sal",
        "m": "PSAL",
    },
}

# Set the default min max values for the color bar scale
cfg_var_min_max = {
    "temp": {
        "c-rean": [12, 30],
        "m": [12, 30]
    },
    "so": {
        "c-rean": [37, 39],
        "m": [37, 39]
    }
}

# Set flag for daily average
cfg_var_d_values_flag = {
    "temp": {
        "c-rean": False,
        "c-obs": False,
        "m": True
    },
    "so": {
        "c-rean": False,
        "c-obs": False,
        "m": True
    }
}

