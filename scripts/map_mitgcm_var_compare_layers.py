import sys
import matplotlib.pyplot as plt
from pathlib import Path
import math

import numpy as np

# %% 
## Get current working directory
if hasattr(sys, "ps1"):
    cwd = Path.cwd() # interactive window
else:
    cwd = str(Path(__file__).resolve().parent.parent) # command line
# Add the script parent directory to sys.path to allow importing lib in command line execution mode
if str(cwd) not in sys.path:
    sys.path.append(str(cwd))


# %%
## Import local settings and liabraries
import spitbran_config
from lib import my_sys_utilities
from lib import my_nc_utilities
from lib import my_plot_utilities

## Reload modules (uncomment this when editing the modules as it picks up the changes)
import importlib
importlib.reload(spitbran_config)
importlib.reload(my_sys_utilities)
importlib.reload(my_plot_utilities)
importlib.reload(my_nc_utilities)

#%% 
## Get target date and variable and set defaults
target_date = my_sys_utilities.get_target_date(
    "20130101",
    "YYYYMMDD",
)
target_var = my_sys_utilities.get_target_var(
    "thetao",
)


#%%
## Map the target variable to corresponding variable names in CMEMS and MITgcm-BFM files
target_var_fn_mapped = {}
target_var_fn_mapped['m'] = spitbran_config.cfg_var_filename_map[target_var]["m"]


# Load MITgcm-BFM output file
m_ds = my_nc_utilities.get_values_map_specific_day(
    "m",
    spitbran_config.cfg_data_base_dirs['m'],
    target_date,
    target_var_fn_mapped['m'],
)




# %%
# Extract var data at the target time and depth indecies
# print(c_ds.variables.keys())
# print(m_ds.variables['thetao'].dimensions)
#c_var = c_ds.variables['thetao'][0, 0, :, :]  # ('time', 'depth', 'latitude', 'longitude')
# print(m_ds.variables[target_var].dimensions)

# MITgcm: 3-hourly outputs so need to take avarage of the 8 values per day
# First and second layer
m_var_d0 = m_ds.variables['thetao'][:, 0, :, :].mean(axis=0)
m_var_d1 = m_ds.variables['thetao'][:, 1, :, :].mean(axis=0)
# m_ds.variables['thetao'].dimensions

# Interpolate data of MITgcm output between depth 0 and depth 1
#   m_ds.variables['depth'][:]
#   0.75 m (first layer i.e. with depth index 0) and
#   2.25 m (second layer i.e. with depth index 1)
#   assuming linear interpolation
# itp_factor = (1.01 - 0.75) / (2.25 - 0.75)
# m_var_itp = (1 - itp_factor) * m_var_d0 + itp_factor * m_var_d1


# Extract latitude and longitude
# c_lat = c_ds.variables['latitude'][:]
# c_lon = c_ds.variables['longitude'][:]

m_lat = m_ds.variables['latitude'][:]
m_lon = m_ds.variables['longitude'][:]

# Determine the range for the color bar scale
# sst_min = min(c_sst.min(), m_sst.min())
# sst_max = max(c_sst.max(), m_sst.max())
#   (Prefer fixed values so that different plots at differnt times can be compared against the same range)
# sst_min = 8 
# sst_max = 21

m_var_min_across_layers = math.floor(min(m_var_d0.min(), m_var_d1.min()))
m_var_max_across_layers = math.ceil(max(m_var_d0.max(), m_var_d1.max()))

min_value = m_var_d0.min()
print("min value: ", min_value)
# Find the indices of the minimum value
min_indices = np.where(m_var_d0 == min_value)
print(min_indices)
min_lats = m_lat[min_indices[0]]  # Adjust dimension for your dataset
min_lons = m_lon[min_indices[1]]
print(f"Coordinates of minimum value: {list(zip(min_lats, min_lons))}")



# Create a figure and axes (two subplots)
fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
fig.suptitle(f"{target_var} - {target_date} - Depth 0/1 comparison - day avarage")

# Plot the dataset at first layer
m_img_d0 = my_plot_utilities.plot_map_minmax_nocb(
    axs[0],
    "MITgcm-BFM (Depth 0)",
    m_var_d0,
    target_var,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    m_var_min_across_layers, m_var_max_across_layers,
)

# Plot the second dataset (m SST daily avaraged)
m_img_d1 = my_plot_utilities.plot_map_minmax_nocb(
    axs[1],
    "MITgcm-BFM (Depth 1)",
    m_var_d1,
    target_var,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    m_var_min_across_layers, m_var_max_across_layers,
)

# Add a single colorbar
cbar = fig.colorbar(
    m_img_d1, 
    ax=axs, 
    orientation="vertical", 
    label=f"{target_var} ({m_ds.variables[target_var].units})", 
    shrink=0.8
)

# Save image
fig.savefig(rf"{cwd}/IMAGES/{target_var}-{target_date}--{m_var_min_across_layers}-{m_var_max_across_layers}--d0-d1.png", dpi=300, bbox_inches='tight')
# Display the plots
fig.show()



fig_m_d0, axs_m_d0 = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)

# Plot the dataset at first layer
m_img_d0_single = my_plot_utilities.plot_map_minmax_nocb(
    axs_m_d0,
    "",
    m_var_d0,
    target_var,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    m_var_min_across_layers, m_var_max_across_layers,
)

# Add a single colorbar
m_img_d0_single_cb = fig_m_d0.colorbar(
    m_img_d0_single, 
    ax=axs_m_d0, 
    orientation="vertical", 
    label=f"{target_var} ({m_ds.variables[target_var].units})", 
    shrink=0.8
)
# Save image
fig_m_d0.savefig(rf"{cwd}/IMAGES/{target_var}-{target_date}--{m_var_min_across_layers}-{m_var_max_across_layers}--d0.png", dpi=300, bbox_inches='tight')


fig_m_d1, axs_m_d1 = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)

# Plot the dataset at first layer
m_img_d1_single = my_plot_utilities.plot_map_minmax_nocb(
    axs_m_d1,
    "",
    m_var_d0,
    target_var,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    m_var_min_across_layers, m_var_max_across_layers,
)

# Add a single colorbar
m_img_d1_single_cb = fig_m_d1.colorbar(
    m_img_d1_single, 
    ax=axs_m_d1, 
    orientation="vertical", 
    label=f"{target_var} ({m_ds.variables[target_var].units})", 
    shrink=0.8
)
# Save image
fig_m_d1.savefig(rf"{cwd}/IMAGES/{target_var}-{target_date}--{m_var_min_across_layers}-{m_var_max_across_layers}--d1.png", dpi=300, bbox_inches='tight')



# %%
# Compute element-wise comparison of m var at first and second layer
m_var_m_d0_d1 = m_var_d0 == m_var_d1
# Save to a text file
np.savetxt(f"m_var_m_d0_d1_{target_date}.txt", m_var_m_d0_d1, fmt='%s')

m_var_m_d0_d1_diff = m_var_d0 - m_var_d1
np.savetxt(f"m_var_m_d0_d1_diff_{target_date}.txt", m_var_m_d0_d1_diff, fmt='%s')

fig_m_d0_d1_diff, axs_m_d0_d1_diff = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)
# Plot the dataset at first layer
m_img_d0_d1_diff = my_plot_utilities.plot_map_minmax_nocb(
    axs_m_d0_d1_diff,
    "",
    m_var_m_d0_d1_diff,
    target_var,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    -1, 1,
)

m_img_d0_d1_diff_cb = fig_m_d0_d1_diff.colorbar(
    m_img_d0_d1_diff, 
    ax=axs_m_d0_d1_diff, 
    orientation="vertical", 
    label=f"{target_var} ({m_ds.variables[target_var].units})", 
    shrink=0.8
)
# Save image
fig_m_d0_d1_diff.savefig(rf"{cwd}/IMAGES/{target_var}-{target_date}--{m_var_min_across_layers}-{m_var_max_across_layers}--d0-d1-diff.png", dpi=300, bbox_inches='tight')

