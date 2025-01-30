# %%
## Import libraries
import sys
import matplotlib
# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'webAgg' depending on environment
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

import spitbran_config
from lib import my_sys_utilities
from lib import my_nc_utilities
from lib import my_plot_utilities

## Reload modules (uncomment this when editing the modules as it picks up the changes)
# import importlib
# importlib.reload(spitbran_config)
# importlib.reload(my_sys_utilities)
# importlib.reload(my_plot_utilities)
# importlib.reload(my_nc_utilities)

#%% 
## Get target date and variable and set defaults
target_date = my_sys_utilities.get_target_date(
    "201301",
    "YYYYMM",
)
target_var = my_sys_utilities.get_target_var(
    "so",
)


#%%
## Map the target variable to corresponding variable names in CMEMS and MITgcm-BFM files
target_var_fn_mapped = {}
target_var_fn_mapped['c'] = spitbran_config.cfg_var_filename_map[target_var]["c"]
target_var_fn_mapped['m'] = spitbran_config.cfg_var_filename_map[target_var]["m"]


# %% 
## Search data directories for files related to target month
# CMEMS
c_time, c_var, c_var_long_name, c_var_units = my_nc_utilities.get_values_in_point_with_time(
    "c",
    spitbran_config.cfg_data_base_dirs['c'],
    target_date,
    target_var,
    target_var_fn_mapped['c'],
    spitbran_config.cfg_latitude,
    spitbran_config.cfg_longitude,
    spitbran_config.cfg_depth_index,
)
# MITgcm-BFM
m_time, m_var, m_var_d = my_nc_utilities.get_values_in_point_with_time(
    "m",
    spitbran_config.cfg_data_base_dirs['m'],
    target_date,
    target_var,
    target_var_fn_mapped['m'],
    spitbran_config.cfg_latitude,
    spitbran_config.cfg_longitude,
    spitbran_config.cfg_depth_index,
    True,
)


# %%
## Reset settinngs and close any previous plots
plt.rcdefaults()
plt.close('all')
# Disable automatic browser opening
matplotlib.rcParams['webagg.open_in_browser'] = False


# %%
## Plot the curves
fig = plt.figure(num=1, figsize=(10, 6), dpi=100)
fig.clf()
ax = fig.add_subplot(111)  
line1, = ax.plot(c_time, c_var, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['ref']}", label="CMEMS")
line2, = ax.plot(m_time, m_var, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['model']}", label="MITgcm-BFM")
if m_var_d:
    line3, = ax.plot(c_time, m_var_d, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['model_avg']}", label="MITgcm-BFM - Daily Avg")

# Format the x-axis dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Add title, labels, and grid
fig.suptitle(f"Curve for var {c_var_long_name} ({c_var_units}) for the Month {target_date}")

ax.set_xlabel("Date")
ax.set_ylabel(f"{target_var} ({c_var_units})")
ax.grid(True)


# %%
## Add an interactive legend
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
lines = [line1, line2]
if m_var_d:
    lines.append(line3)
# Enable picking on legend items
for legend_line in legend.get_lines():
    legend_line.set_picker(True)
    # print(f"Legend item picker enabled: {legend_line.get_label()}")

# Connect the pick event to the toggle function
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