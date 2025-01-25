# %%
## Import libraries
import sys
import matplotlib
# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'webAgg' depending on environment
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


# %% 
## Get current working directory
if hasattr(sys, "ps1"):
    cwd = Path.cwd() # interactive window
else:
    cwd = str(Path(__file__).resolve().parent.parent) # command line


# %%
## Import local settings and liabraries
# Add the script parent directory to sys.path to allow importing lib in command line execution mode
if str(cwd) not in sys.path:
    sys.path.append(str(cwd))

# print(f"cwd: {cwd}")
# print(f"sys.path: {sys.path}")

import spitbran_config
from lib import my_sys_utilities
from lib import my_plot_utilities
from lib import my_nc_utilities
import importlib

## Reload modules (comment out once done with modifying the modules)
importlib.reload(spitbran_config)
importlib.reload(my_sys_utilities)
importlib.reload(my_plot_utilities)
importlib.reload(my_nc_utilities)

#%% 
## Get target date and variable
target_date = my_sys_utilities.get_target_date(
    "201301",
    "YYYYMM",
)
target_var = my_sys_utilities.get_target_var(
    "thetao",
)

# %% 
## Search data directories for files related to target month
# CMEMS
c_time, c_var, c_var_long_name, c_var_units = my_nc_utilities.get_c_data(
    spitbran_config.cfg_data_base_dirs['c'],
    target_date,
    spitbran_config.cfg_latitude,
    spitbran_config.cfg_longitude,
    spitbran_config.cfg_depth_index,
    target_var
)
# MITgcm-BFM
m_time, m_var, m_var_d = my_nc_utilities.get_m_data(
    spitbran_config.cfg_data_base_dirs['m'],
    target_date,
    spitbran_config.cfg_latitude,
    spitbran_config.cfg_longitude,
    spitbran_config.cfg_depth_index,
    target_var,
    True,
)

# %%
## Reset settinngs and close any previous plots
plt.rcdefaults()
plt.close('all')
# Disable automatic browser opening
matplotlib.rcParams['webagg.open_in_browser'] = False

# %%
## Plot the temperature curves
fig = plt.figure(num=1, figsize=(10, 6), dpi=100)
fig.clf()
ax = fig.add_subplot(111)  
line1, = ax.plot(c_time, c_var, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['ref']}", label="CMEMS")
line2, = ax.plot(m_time, m_var, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['model']}", label="MITgcm-BFM")
if m_var_d:
    line3, = ax.plot(c_time, m_var_d, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['model_avg']}", label="MITgcm-BFM - Daily Avg")

# Format the x-axis times
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Add title, labels, and grid
fig.suptitle(f"Curve for var {c_var_long_name} ({c_var_units}) for the Month {target_date}")
# ax.autoscale()  # Reset axes to fit the data
ax.set_xlabel("Date")
ax.set_ylabel(f"{target_var} ({c_var_units})")
ax.grid(True)

# %%
## Add an interactive legend
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
lines = [line1, line2]
print("lines: ", len(legend.get_lines()))

if m_var_d:
    lines.append(line3)
# Enable picking on legend items
for legend_line in legend.get_lines():
    legend_line.set_picker(True)
    print(f"Legend item picker enabled: {legend_line.get_label()}")
# Connect the pick event to the toggle function
fig.canvas.mpl_connect('pick_event', lambda event: my_plot_utilities.on_pick(event, lines, legend, fig))
# Debug: Check if the event connection works
print("Event connections established. Ready to show the plot.")
print("Figure size:", fig.get_size_inches())
print("Figure DPI:", fig.get_dpi())

# %%
## Adjust layout
# Rotate the date labels for better readability
plt.xticks(rotation=45)
# Tight layout to avoid clipping of legend
plt.tight_layout()

# %%
# Save image and show the plot
images_store_path = fr"{cwd}/IMAGES"
plt.savefig(rf"{images_store_path}/{target_date}--{spitbran_config.cfg_latitude}-{spitbran_config.cfg_longitude}--sst.png", dpi=300, bbox_inches="tight")
# Show the plot
plt.show()