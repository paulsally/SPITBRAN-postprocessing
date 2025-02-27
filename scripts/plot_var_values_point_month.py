"""
Script Name: plot_var_values_point_month.py
Author: Sara Polselli
Date: 2025-02-27
Description:
    This script is used to see how a variable at a given point changes with time in the 3 datasets (CMEMS Reanalysis, CMEMS Observation, MITgcm output).
    Lat, lon and depth index are fixed (set in config file).
    
    Features:
    For each dataset (c-rean, c-obs and m):
    - Reads NetCDF data (time and variable values at given depth and coordinates for given month)
    - Creates time curves using matplotlib. Tested with temp (thetao) and salinity (so)
    - Using webAgg backend, provides a link to localhost address for interactive legend to toggle visibility of curves
    - Saves output figure file (.png)
    
Usage:
    python plot_var_values_point_month.py 20130101 temp
    python plot_var_values_point_month.py 20130101 so
    or interactively via VSCode or Jupyter and insert the date and variable when prompted
"""
# %%
## Import libraries
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# %%
## Import local settings and local libraries
import spitbran_config
from lib import my_sys_utilities
from lib import my_nc_utilities
from lib import my_plot_utilities

# %% 
## Reload modules (comment for performance, uncomment for development, i.e. when editing the modules)
import importlib
importlib.reload(spitbran_config)
importlib.reload(my_sys_utilities)
importlib.reload(my_plot_utilities)
importlib.reload(my_nc_utilities)

# %%
# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'webAgg' depending on environment
# Disable automatic browser opening
matplotlib.rcParams['webagg.open_in_browser'] = False

# %% 
## Get target date and variable (and set defaults)
target_date = my_sys_utilities.get_target_date(
    "201211",
    "YYYYMM",
)
target_var = my_sys_utilities.get_target_var(
    "temp",
)

# %% 
## Get the values of .nc file corresponding to given month
var_time = {}
var_time_d = {}
var_values = {}
var_long_name = {}
var_units = {}
var_daily_values = {}
for data_type in spitbran_config.cfg_datasets.keys():
    if not(data_type == "c-obs" and target_var == "so"):
        var_time[data_type], var_values[data_type], var_daily_values[data_type], var_long_name[data_type], var_units[data_type] = my_nc_utilities.get_values_in_point_with_time_given_month(
            data_type,
            spitbran_config.cfg_data_base_dirs[data_type],
            target_date,
            spitbran_config.cfg_var_name[target_var][data_type],
            spitbran_config.cfg_var_filename_map[target_var][data_type],
            spitbran_config.cfg_latitude,
            spitbran_config.cfg_longitude,
            spitbran_config.cfg_depth_index,
            spitbran_config.cfg_var_d_values_flag[target_var][data_type],
        )

# %%
## Reset settings and close any previous plots
plt.rcdefaults()
plt.close('all')

## Plot the curves
fig = plt.figure(num=1, figsize=(10, 6), dpi=100)
fig.clf()
ax = fig.add_subplot(111)  

lines = []
for data_type, label in spitbran_config.cfg_datasets.items():
    if not(data_type == "c-obs" and target_var == "so"):
        line, = ax.plot(
            var_time[data_type], var_values[data_type],
            marker=".", linestyle="solid",
            color=spitbran_config.cfg_colours[data_type],
            label=label
        )
        lines.append(line)

## Check if daily values should be plotted
if spitbran_config.cfg_var_d_values_flag[target_var]["m"]:
    var_time["m-d"] = var_time["c-rean"]
    line, = ax.plot(
        var_time["m-d"], var_daily_values["m"],
        marker=".", linestyle="solid",
        color=spitbran_config.cfg_colours["m_avg"],
        label="MITgcm-BFM - Daily Avg"
    )
    lines.append(line)

## Format the x-axis dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

## Add title, labels, and grid
fig.suptitle(f"Curve for var {target_var} ({var_units['c-rean']}) for the Month {target_date} at point {spitbran_config.cfg_latitude}, {spitbran_config.cfg_longitude}")

ax.set_xlabel("Date")
ax.set_ylabel(f"{target_var} ({var_units['c-rean']})")
ax.grid(True)

# %%
## Add an interactive legend
for line in lines:
    line.set_picker(True)
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
## Enable picking on legend items
for legend_line in legend.get_lines():
    legend_line.set_picker(True)
    # print(f"Legend item picker enabled: {legend_line.get_label()}")

# Connect the pick event to the toggle function
# print("Connecting pick event...")
fig.canvas.mpl_connect('pick_event', lambda event: my_plot_utilities.on_pick(event, lines, legend, fig))
# Debug: Check if the event connection works
# print("Event connections established. Ready to show the plot.")
# print("Figure size:", fig.get_size_inches())
# print("Figure DPI:", fig.get_dpi())

# %%
## Adjust layout
# Rotate the date labels for better readability
plt.xticks(rotation=45)
# Tight layout to avoid clipping of legend
plt.tight_layout()

# %%
# Save image and show the plot
images_store_path = fr"{cwd}/IMAGES"
plt.savefig(rf"{images_store_path}/{target_date}--{spitbran_config.cfg_latitude}-{spitbran_config.cfg_longitude}--{target_var}.png", dpi=300, bbox_inches="tight")
plt.show()