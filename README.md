# MITgcm-BFM postprocessing

MITgcm-BFM postprocessing contains scripts for comparing model output files with Copernicus Marine data (Reanalysis and Observations).
- map_var_compare_layers.py
    - plots maps side by side of variable of interest at depth index 0 and depth index 1. Tested with temperature (input temp for thetao) and salinity (input so). Also plots map of difference.
- map_var_day.py
    - plots maps side by side of CMEMS Reanalysis and MITgcm-BFM output. Tested with temp and so.
- plot_var_values_point_month.py 
    - plots the evolution in time of the values of a variable of interest in one point. Tested with var temp (thetao in CMEMS Reanalysis and MITgcm and analysed_sst in CMEMS Observations) and so (salinity).

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
- Set config values (colours of plotted lines, geolocation, paths to directories of data to be plotted) in the file spitbran_config in the root directory of the project

```python
cfg_data_base_dirs = {
    "c-rean": r"/OCEANASTORE/database/CMEMS/rean-d",
    "c-obs": r"~/SPITBRAN/DATA/CMEMS/obs",
    "m": r"/OCEANASTORE/progetti/spitbran2"
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
