# MITgcm-BFM postprocessing

MITgcm-BFM postprocessing contains scripts for comparing model output files with Copernicus Marine data.

## Prerequisites
- Create a conda environment with the following packages:
    - jupyter
    - notebook
    - matplotlib
    - netCDF4
    - numpy
    - python-dateutil
## Usage:
- Set config values (colours of plotted lines, geolocation, paths to directories of data to be plotted)

```python
cfg_data_base_dirs = {
    "c": r"/OCEANASTORE/database/CMEMS/rean-d",
    "m": r"/OCEANASTORE/progetti/spitbran2/2013"
}
```
- Run python script:
    - Interactively: Open the python script and run in interactive window
        - In this case the script asks to input the required variables (if data is not found no error is handled gracefully this needs development)
    - Via command line 
        ```python
        python plot_cmems_mitgcm_var_values_point_month.py 201301 thetao
        ```