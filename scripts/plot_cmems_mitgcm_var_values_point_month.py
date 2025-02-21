# %%backend
## Import libraries
import matplotlib
# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'webAgg' depending on environment
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# %%
## Import local settings and liabraries
import spitbran_config
from lib import my_sys_utilities
from lib import my_nc_utilities
from lib import my_plot_utilities

# %% 
## Get current working directory
cwd = my_sys_utilities.get_cwd()

## Reload modules (comment for performance, uncomment for development, i.e. when editing the modules)
import importlib
importlib.reload(spitbran_config)
importlib.reload(my_sys_utilities)
importlib.reload(my_plot_utilities)
importlib.reload(my_nc_utilities)

#%% 
## Get target date and variable and set defaults
target_date = my_sys_utilities.get_target_date(
    "201211",
    "YYYYMM",
)
target_var = my_sys_utilities.get_target_var(
    "temp",
)


# %% 
## Search data directories for files related to target month
# # CMEMS
# c_rean_time, c_rean_var, c_rean_var_long_name, c_rean_var_units = my_nc_utilities.get_values_in_point_with_time_given_month(
#     "c-rean",
#     spitbran_config.cfg_data_base_dirs["c-rean"],
#     target_date,
#     spitbran_config.cfg_var_name["temp"]["c-rean"],
#     spitbran_config.cfg_var_filename_m[target_var]["c-rean"],
#     spitbran_config.cfg_latitude,
#     spitbran_config.cfg_longitude,
#     spitbran_config.cfg_depth_index,
# )

# c_obs_time, c_obs_var, c_obs_var_long_name, c_obs_var_units = my_nc_utilities.get_values_in_point_with_time_given_month(
#     "c-obs",
#     spitbran_config.cfg_data_base_dirs["c-obs"],
#     target_date,
#     spitbran_config.cfg_var_name["temp"]["c-obs"],
#     spitbran_config.cfg_var_filename_map[target_var]["c-obs"],
#     spitbran_config.cfg_latitude,
#     spitbran_config.cfg_longitude,
#     spitbran_config.cfg_depth_index,
# )
# # MITgcm-BFM
# m_time, m_var, m_var_d = my_nc_utilities.get_values_in_point_with_time_given_month(
#     "m",
#     spitbran_config.cfg_data_base_dirs["m"],
#     target_date,
#     target_var,
#     spitbran_config.cfg_var_filename_map[target_var]["m"],
#     spitbran_config.cfg_latitude,
#     spitbran_config.cfg_longitude,
#     spitbran_config.cfg_depth_index,
#     True,
# )


# Disable automatic browser opening
matplotlib.rcParams['webagg.open_in_browser'] = False

# %%
## Reset settinngs and close any previous plots
plt.rcdefaults()
plt.close('all')


## Plot the curves
fig = plt.figure(num=1, figsize=(10, 6), dpi=100)
fig.clf()
ax = fig.add_subplot(111)  

var_time = {}
var_time_d = {}
var_values = {}
var_long_name = {}
var_units = {}
var_daily_values = {}

for data_type in spitbran_config.cfg_data_base_dirs.keys():
    # print(
    #     data_type,
    #     spitbran_config.cfg_data_base_dirs[data_type],
    #     target_date,
    #     spitbran_config.cfg_var_name[target_var][data_type],
    #     spitbran_config.cfg_var_filename_map[target_var][data_type],
    #     spitbran_config.cfg_latitude,
    #     spitbran_config.cfg_longitude,
    #     spitbran_config.cfg_depth_index,
    #     calclulate_day_avg
    # )

    #var_time, var_values, var_long_name, var_units = my_nc_utilities.get_values_in_point_with_time_given_month(
    var_time[data_type], var_values[data_type], var_daily_values[data_type], var_long_name[data_type], var_units[data_type] = my_nc_utilities.get_values_in_point_with_time_given_month(
        data_type,
        spitbran_config.cfg_data_base_dirs[data_type],
        target_date,
        spitbran_config.cfg_var_name[target_var][data_type],
        spitbran_config.cfg_var_filename_map[target_var][data_type],
        spitbran_config.cfg_latitude,
        spitbran_config.cfg_longitude,
        spitbran_config.cfg_depth_index,
        spitbran_config.cfg_var_d_values[target_var][data_type],
    )

    # if calclulate_day_avg:
    #     var_time[data_type], var_values[data_type], var_daily_values[data_type] = result
    # else:
    #     var_time[data_type], var_values[data_type], var_long_name[data_type], var_units[data_type] = result
    # var_time[data_type], var_values[data_type], var_daily_values[data_type], var_long_name[data_type], var_units[data_type] = result


lines = []
for key, label in spitbran_config.cfg_datasets.items():
    line, = ax.plot(
        var_time[key], var_values[key],
        marker=".", linestyle="solid",
        color=spitbran_config.cfg_colours[key],
        label=label
    )
    lines.append(line)

# Check if daily values should be plotted
if spitbran_config.cfg_var_d_values_flag[target_var][data_type]:
    var_time["m-d"] = var_time["c-rean"]
    line, = ax.plot(
        var_time["m-d"], var_daily_values["m"],
        marker=".", linestyle="solid",
        color=spitbran_config.cfg_colours["m_avg"],
        label="MITgcm-BFM - Daily Avg"
    )
    lines.append(line)

# Format the x-axis dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Add title, labels, and grid
fig.suptitle(f"Curve for var {target_var} ({var_units['c-rean']}) for the Month {target_date} at point {spitbran_config.cfg_latitude}, {spitbran_config.cfg_longitude}")

ax.set_xlabel("Date")
# ax.set_ylabel(f"{target_var} ({c_rean_var_units})")
ax.set_ylabel(f"{var_units['c-rean']}")
ax.grid(True)


# %%

# # Enable picking on the actual plotted lines

# OR (if lines is a list)
for line in lines:
    line.set_picker(True)
## Add an interactive legend
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
# Enable picking on legend items
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