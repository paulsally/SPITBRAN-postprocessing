"""
Script Name: map_cmems_mitgcm_var_day.py
Author: Sara Polselli
Date: 2025-02-27
Description:
    This script is used to create side by side maps of the required variable for comparing CMEMES Reanalysis and MITgcm-BFM datasets at given date.
    It generates maps of the data (using depth 0 for CMEMES dataset and values linearly interpolated between depth 0 and 1 for MITgcm-BFM dataset).
    
    Features:
    For each dataset (c-rean and m):
    - Reads NetCDF data (time, variable, depth, and coordinates)
    - Creates side by side maps using matplotlib. Tested with temp (thetao) and salinity (so)
    - Saves output figure file (.png)
    
Usage:
    python map_cmems_mitgcm_var_day.py 20130101 temp
    python map_cmems_mitgcm_var_day.py 20130101 so
    or interactively via VSCode or Jupyter and insert the date and variable when prompted
"""

# %% [markdown]
## Imports and setup
# %%
import matplotlib.pyplot as plt
from IPython import get_ipython
import sys
from pathlib import Path

# %% 
## Get current working directory
# cwd = my_sys_utilities.get_cwd()
try:
    get_ipython()  # Jupyter or IPython environment
    cwd = Path.cwd()  # interactive window
    if sys.stdin and sys.stdin.isatty():
        cwd = str(Path(__file__).resolve().parent.parent)  # command line
        sys.path.append(cwd)
except NameError:
    cwd = str(Path(__file__).resolve().parent.parent)  # command line

# %% [markdown]
### Import local settings and libraries
#%%
import spitbran_config
from lib import my_sys_utilities
from lib import my_nc_utilities
from lib import my_plot_utilities


#%% [markdown]
### Reload modules (comment for performance, uncomment for development i.e. when editing the modules)
import importlib
importlib.reload(spitbran_config)
importlib.reload(my_sys_utilities)
importlib.reload(my_plot_utilities)
importlib.reload(my_nc_utilities)

#%% [markdown]
## Get target date and variable and set defaults
# %%
target_date = my_sys_utilities.get_target_date(
    "20130101",
    "YYYYMMDD",
)
target_var = my_sys_utilities.get_target_var(
    "temp",
)

#%% [markdown]
### For each type of data (c-rean or m) 
#   - load netCDF file and get the values for var
#   - plot the maps
#%%
c_rean_ds = my_nc_utilities.get_values_map_specific_day(
    "c-rean",
    spitbran_config.cfg_data_base_dirs["c-rean"],
    target_date,
    spitbran_config.cfg_var_filename_map[target_var]["c-rean"],
)

# Load MITgcm-BFM output file
m_ds = my_nc_utilities.get_values_map_specific_day(
    "m",
    spitbran_config.cfg_data_base_dirs["m"],
    target_date,
    spitbran_config.cfg_var_filename_map[target_var]["m"],
)

# %%
# Extract var data at the target time and depth indices 0 and 1
# print(c_ds.variables.keys())
# print(m_ds.variables[spitbran_config.cfg_var_name[target_var][data_type]].dimensions)
c_rean_var = c_rean_ds.variables[spitbran_config.cfg_var_name[target_var]["c-rean"]][0, 0, :, :]  # ('time', 'depth', 'latitude', 'longitude')
# print(m_ds.variables[spitbran_config.cfg_var_name[target_var][data_type]].dimensions)

# MITgcm: 3-hourly outputs so need to take average of the 8 values per day
# First and second layer
m_var_d0 = m_ds.variables[spitbran_config.cfg_var_name[target_var]["m"]][:, 0, :, :].mean(axis=0)
m_var_d1 = m_ds.variables[spitbran_config.cfg_var_name[target_var]["m"]][:, 1, :, :].mean(axis=0)
# m_ds.variables[spitbran_config.cfg_var_name[target_var][data_type]].dimensions
# units = m_ds.variables[spitbran_config.cfg_var_name[target_var][data_type]].units

# Interpolate data of MITgcm output between depth 0 and depth 1
#   m_ds.variables['depth'][:]
#   0.75 m (first layer i.e. with depth index 0) and
#   2.25 m (second layer i.e. with depth index 1)
#   assuming linear interpolation
depth_0 = 0.75
depth_1 = 2.25
int_factor = (1.01 - depth_0) / (depth_1 - depth_0)
m_var_d0_int = (1 - int_factor) * m_var_d0 + int_factor * m_var_d1

# %%
# Compute element-wise comparison of m var at first and second layer
# m_var_d0_m_var_d1 = m_var_d0 == m_var_d1
# Save to a text file
# np.savetxt("m_var_d0_m_var_d1.txt", m_var_d0_m_var_d1, fmt='%s')

# Extract latitude and longitude
c_rean_lat = c_rean_ds.variables['latitude'][:]
c_rean_lon = c_rean_ds.variables['longitude'][:]

m_lat = m_ds.variables['latitude'][:]
m_lon = m_ds.variables['longitude'][:]

# Determine the range for the color bar scale 
#   During development phase take min values across layers to gather the significant range after which values are set to fixed values in the config file (spitbran_config)
#   Prefer fixed values so that different plots at differnt times can be compared against the same range
# var_min_across_layers = math.floor(min(var_d0.min(), var_d1.min()))
# var_max_across_layers = math.ceil(max(var_d0.max(), var_d1.max()))
var_min = spitbran_config.cfg_var_min_max[target_var]["c-rean"][0]
var_max = spitbran_config.cfg_var_min_max[target_var]["c-rean"][1]

# Create a figure and axes (two subplots)
fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
fig.suptitle(f"{target_var} - {target_date} - day average")

# Plot the first dataset (c Rean var - daily)
c_rean_im = my_plot_utilities.plot_map_minmax_nocb(
    axs[0],
    "CMEMS Reanalysis\n(depth 0 i.e. mt=1.01)",
    c_rean_var,
    target_var,
    c_rean_lon, c_rean_lat,
    var_min, var_max,
)

# Plot the second dataset (m var daily averaged)
m_im = my_plot_utilities.plot_map_minmax_nocb(
    axs[1],
    "MITgcm\n(depth linearly interpolated btw 0 and 1 i.e. 0.75 and 2.25)",
    m_var_d0_int,
    target_var,
    m_lon, m_lat,
    var_min, var_max,
)

for ax in axs:
    ax.set_aspect(1)

# Add a single colorbar
cbar = fig.colorbar(
    c_rean_im, 
    ax=axs, 
    orientation="vertical", 
    label=f"{target_var} ({m_ds.variables[spitbran_config.cfg_var_name[target_var]['c-rean']].units})", 
    shrink=0.8
)

# Save image
fig.savefig(rf"{cwd}/IMAGES/{target_date}--{var_min}-{var_max}--d0.png", dpi=300, bbox_inches='tight')

# Display the plots
plt.show()
