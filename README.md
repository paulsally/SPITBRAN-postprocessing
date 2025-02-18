# MITgcm-BFM postprocessing

MITgcm-BFM postprocessing contains scripts for comparing model output files with Copernicus Marine data.
- plot_cmems_mitgcm_var_values_point_month.py 
    - plots the evolution in time of the values of a variable of interest in one point. The script has been tested with var thetao and so (cur requires further development being a 2D)

## Prerequisites
- Create a conda environment with the following packages:
    - jupyter
    - notebook
    - matplotlib
    - netCDF4
    - numpy
    - python-dateutil

## Usage:
- Set config values (colours of plotted lines, geolocation, paths to directories of data to be plotted) in the file spitbran_config in the root directory of the project

```python
cfg_data_base_dirs = {
    "c-rean": r"/OCEANASTORE/database/CMEMS/rean-d",
    "m": r"/OCEANASTORE/progetti/spitbran2"
}
```
- Run script:
    - Interactively: Open the python script and run it in interactive window either via Visual Studio Code or on the Jupyter web innterface
        - In this case the script asks to input the required variable values (if data is not found no error is handled gracefully this needs more development)
    - Via command line pass the variables values as arguments, e.g.: 
        ```python
        python plot_cmems_mitgcm_var_values_point_month.py 201301 thetao
        ```

# Expected results
The script provides a link to open the result on a web page. This has the advantage of providing a certain degree of interactivity where the visibility of the curves can be toggled by clicking on the corresponding line in the legend.
The script also saves the result in a static image.