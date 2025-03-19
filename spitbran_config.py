# Geo Location and depth (for plotting time series)
cfg_latitude = 44.0
cfg_longitude = 9.0
cfg_depth_index = 0

cfg_datasets = {
    "c-rean": {
        "base_data_dir": "/OCEANASTORE/database/CMEMS/rean-d",
        "legend": "CMEMS Rean",
        "colour": {
            "main": "#46af6b",
            "seasonal": {
                "winter": "#46af6b",
                "summer": "#6DC58C",
            },
        },
        "var_name": {
            "temp": "thetao",
            "so": "so",
        },
        "var_filename": {
            "temp": "tem",
            "so": "sal",
        },
        "var_d_values_flag": False,
        "min_max": {
            "temp": [12, 30],
            "so": [37, 39],
        },
    },
    "c-obs": {
        "base_data_dir": "/OCEANASTORE/database/CMEMS/SST_MED_SST_L4_REP_OBSERVATIONS_010_021",
        "legend": "CMEMS Obs Sat",
        "colour": {
            "main": "#fb8500",
            "seasonal": {
                "winter": "#fb8500",
                "summer": "#",
            },
        },
        "var_name": {
            "temp": "analysed_sst",
            "so": "--",
        },
        "var_filename": {
            "temp": "sst",
            "so": "--",
        },
        "var_d_values_flag": False,
        "min_max": {
            "temp": [0, 0],
            "so": [0, 0],
        },
    },
    "m": {
        "base_data_dir": "/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs",
        "legend": "MITgcm-BFM",
        "colour": {
            "main": "#168aad",
            "seasonal": {
                "winter": "#168aad",
                "summer": "#26b7e3",
            },
            "avg": "#1e6091",
        },
        "var_name": {
            "temp": "thetao",
            "so": "so",
        },
        "var_filename": {
            "temp": "TEMP",
            "so": "PSAL",
        },
        "var_d_values_flag": True,
        "min_max": {
            "temp": [12, 30],
            "so": [37, 39],
        },
    },
}
