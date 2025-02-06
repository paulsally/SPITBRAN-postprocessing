import sys
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

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
# Load CMEMS output file
c_ds = my_nc_utilities.get_values_map_specific_day(
    "c",
    spitbran_config.cfg_data_base_dirs['c'],
    target_date,
    spitbran_config.mapped_var_fn['c'],
)

# Load MITgcm-BFM output file
m_ds = my_nc_utilities.get_values_map_specific_day(
    "m",
    spitbran_config.cfg_data_base_dirs['m'],
    target_date,
    spitbran_config.mapped_var_fn['m'],
)




# %%
# Extract var data at the target time and depth indecies
# print(c_ds.variables.keys())
# print(m_ds.variables['thetao'].dimensions)
c_var = c_ds.variables['thetao'][0, 0, :, :]  # ('time', 'depth', 'latitude', 'longitude')
# print(m_ds.variables['thetao'].dimensions)

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
int_factor = (1.01 - 0.75) / (2.25 - 0.75)
m_sst_int = (1 - int_factor) * m_sst + int_factor * m_sst_d1

# %%
# Compute element-wise comparison of m sst at first and second layer
# m_sst_m_sst_d1 = m_sst == m_sst_d1
# Save to a text file
# np.savetxt("m_sst_m_sst_d1.txt", m_sst_m_sst_d1, fmt='%s')

# Extract latitude and longitude
c_lat = c_ds.variables['latitude'][:]
c_lon = c_ds.variables['longitude'][:]

m_lat = m_ds.variables['latitude'][:]
m_lon = m_ds.variables['longitude'][:]

# Determine the range for the color bar scale
# sst_min = min(c_sst.min(), m_sst.min())
# sst_max = max(c_sst.max(), m_sst.max())
#   (Prefer fixed values so that different plots at differnt times can be compared against the same range)
sst_min = 8 
sst_max = 21

# Create a figure and axes (two subplots)
fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
fig.suptitle(f"SST - {requested_date} - depth 0 - day avarage")

# Plot the first dataset (c SST - daily)
c_im = my_plot_utilities.plot_map_minmax_nocb(
    axs[0],
    "CMEMS",
    c_sst,
    c_lon.min(), c_lon.max(), 
    c_lat.min(), c_lat.max(),
    sst_min, sst_max,
)

# Plot the second dataset (m SST daily avaraged)
m_im = my_plot_utilities.plot_map_minmax_nocb(
    axs[1],
    "MITgcm",
    m_sst,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    sst_min, sst_max,
)

# Add a single colorbar
cbar = fig.colorbar(
    c_im, 
    ax=axs, 
    orientation="vertical", 
    label="SST (°C)", 
    shrink=0.8
)

# Create a figure and axes (two subplots)
fig_d1, axs_d1 = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
fig_d1.suptitle(f"SST - {requested_date} - Depth 1 - Day avarage")

# Plot the first dataset (c SST - daily)
c_im_d1 = my_plot_utilities.plot_map_minmax_nocb(
    axs_d1[0],
    "CMEMS",
    c_sst,
    c_lon.min(), c_lon.max(), 
    c_lat.min(), c_lat.max(),
    sst_min, sst_max,
)

# Plot the second dataset (m SST daily avaraged)
m_im_d1 = my_plot_utilities.plot_map_minmax_nocb(
    axs_d1[1],
    "MITgcm",
    m_sst_d1,
    m_lon.min(), m_lon.max(), 
    m_lat.min(), m_lat.max(),
    sst_min, sst_max,
)

# Add a single colorbar
cbar_d1 = fig_d1.colorbar(
    c_im_d1, 
    ax=axs_d1, 
    orientation="vertical", 
    label="SST (°C)", 
    shrink=0.8
)

# Save image
fig.savefig(rf"{cwd}/IMAGES/{requested_date}--{sst_min}-{sst_max}--d0.png", dpi=300, bbox_inches='tight')
fig_d1.savefig(rf"{cwd}/IMAGES/{requested_date}--{sst_min}-{sst_max}--d1.png", dpi=300, bbox_inches='tight')

# Display the plots
plt.show()

# %%
