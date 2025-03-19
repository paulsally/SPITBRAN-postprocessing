# MITgcm-BFM postprocessing

MITgcm-BFM postprocessing contains scripts for comparing model output files with Copernicus Marine data (Reanalysis and Observations).
- map_var_compare_layers.py
    - plots maps side by side of variable of interest at depth index 0 and depth index 1. Tested with temperature (input temp) and salinity (input so). Also plots map of difference.
- map_var_day.py
    - plots maps side by side of CMEMS Reanalysis and MITgcm-BFM output. Tested with temp and so.
- plot_var_values_point.py 
    - plots the evolution in time of the values of a variable of interest in one point. Tested with var temp (thetao in CMEMS Reanalysis and MITgcm and analysed_sst in CMEMS Observations) and so (salinity).
- get_gg_cmems.sh, get_cmems.sh
    - shell scripts to download datasets from CMEMS Reanalysis (launch get_gg_cmems.sh with arguments and this will call get_cmems.sh for every day of download, e.g. './get_gg_cmems.sh "2024-04-01" "2024-04-02"')
- get_gg_cmems_obs.sh, get_cmems_obs.sh
    - shell scripts to download datasets from CMEMS Observations (launch get_gg_cmems_obs.sh with arguments and this will call get_cmems_obs.sh for every day of download, e.g. './get_gg_cmems_obs.sh "2024-04-01" "2024-04-02"')
- get_cmems_insitu.sh
    - shell scripts to download datasets from CMEMS Insitu Observations (launch it with arguments, e.g. './get_cmems_insitu.sh mediterrane 2012/*')

## Prerequisites
- Create a conda environment with the following packages:
    - jupyter
    - notebook
    - matplotlib
    - netCDF4
    - numpy
    - python-dateutil
    (Jupyter and notebook to run scripts interactively)

## Usage:
- Set config values (colours of plotted lines, geolocation, paths to directories of data to be plotted) in the file spitbran_config.py file in the root directory of the project

```python
cfg_datasets = {
    "c-rean": {
        "base_data_dir": "/OCEANASTORE/database/CMEMS/rean-d",
        "legend": "CMEMS Rean",
        "colour": {
            "main": "#46af6b",
            "seasonal": frozenset({
                "winter": "#46af6b",
                "summer": "#6DC58C",
            }),
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
        ...
}
```
- Run scripts:
    - Interactively: Open the python script and run it in interactive window either via Visual Studio Code or on the Jupyter web innterface
        - In this case the script prompts to input the values of required variables (if data is not found no error is handled gracefully this needs more development)
    - Via command line pass the variables values as arguments, e.g.: 
        ```python
        python plot_var_values_point_month.py 201211 temp
        ```

# Expected results
- map_var_compare_layers.py 
    - side by side maps of first and second layers for comparison of cmems reanalysis and MITgcm at given day. 
    - single static images (.png) of each layer for later comparison using an image/file comparison tool
    - comparison map for both cmems reanalysis and MITgcm run
    Tested with temp (thetao) and salinity (so).
- map_var_day.py 
    - maps side by side of cmems reanalysis and MITgcm on given day.
- plot_var_values_point_month.py 
    - provides a link to open the result on a web page on localhost (needs portforwarding if not done automatically). This, i.e. the use of matplotlib.use('webAgg') has the advantage of providing a certain degree of interactivity where the visibility of the curves can be toggled by clicking on the corresponding line in the legend.
    - static image (.png) of the same plot.
- get_gg_cmems.sh, get_cmems.sh, get_gg_cmems_obs.sh, get_cmems_obs.sh, get_cmems_insitu.sh
    - .nc files of required CMEMS datasets downloaded in specified storage path
