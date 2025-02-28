import sys
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import netCDF4 as nc
from IPython import get_ipython

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
    "2012",
    "YYYY",
)
target_var = my_sys_utilities.get_target_var(
    "temp",
)


# Check if requested date is a valid date
try:
    target_date_dobj = datetime.strptime(target_date, "%Y")
    target_date_year = str(target_date_dobj.year)
except Exception as e:
    print(f"{target_date} is not a valid date: need YYYY")
    sys.exit()

# Location and depth
latitude = spitbran_config.cfg_latitude
longitude = spitbran_config.cfg_longitude
depth_index = spitbran_config.cfg_depth_index

# Load CMEMS data
# c_data_base_dir = fr"/OCEANASTORE/database/CMEMS/rean-d"
c_data_base_dir = Path(fr"~/SPITBRAN/DATA/CMEMS/rean-d").expanduser()
# c_data_search_dir = fr"{c_data_base_dir}/{target_date_year}"
c_data_search_dir = c_data_base_dir

# Initialize lists for dates and temperatures
c_dates = []
c_temperatures = []
# Search CMEMS data for files concerning required year
matches_c = my_sys_utilities.get_files_by_keystring_in_fn("c-rean", c_data_search_dir, "tem", target_date)
for c_item in sorted(matches_c):
    c_item_name = c_item.name
    with nc.Dataset(c_item, 'r') as c_ds:
        # Find nearest latitude and longitude indices
        latitudes = c_ds.variables['latitude'][:]
        longitudes = c_ds.variables['longitude'][:]
        lat_idx = np.abs(latitudes - latitude).argmin()
        lon_idx = np.abs(longitudes - longitude).argmin()
        c_time = c_ds.variables['time'][:]
        new_c_time = [datetime(1900, 1, 1) + timedelta(minutes=int(t)) for t in c_time]
        c_dates.extend(new_c_time)
        # Extract temperature for the given depth, lat, and lon
        c_thetao = c_ds.variables['thetao'][:, depth_index, lat_idx, lon_idx]
        c_temperatures.extend(c_thetao)


# %% 
# Load MITgcm-BFM data
m_data_basedir = r"/OCEANASTORE/progetti/spitbran2/output"
m_data_search_dir = m_data_basedir

# Initialize list for temperatures
m_dates = []
m_temperatures = []

# Search for output MITgcm files concerning required year
matches_m = my_sys_utilities.get_files_by_keystring_in_fn("m", m_data_search_dir, "TEMP", target_date)
for m_data_search_dir_item in matches_m: 
    with nc.Dataset(m_data_search_dir_item, 'r') as m_ds:
        # Find nearest latitude and longitude indices
        latitudes = m_ds.variables['latitude'][:]
        longitudes = m_ds.variables['longitude'][:]
        lat_idx = np.abs(latitudes - latitude).argmin()
        lon_idx = np.abs(longitudes - longitude).argmin()
        m_time = c_ds.variables['time'][:]
        new_m_time = [datetime(1970, 1, 1) + timedelta(seconds=int(t)) for t in m_time]
        m_dates.extend(new_m_time)
        # Extract temperature for the given depth, lat, and lon
        m_thetao = m_ds.variables['thetao'][:, depth_index, lat_idx, lon_idx].mean(axis=0)
        m_temperatures.append(m_thetao)

# Plot the temperature curves
plt.figure(figsize=(10, 6))
plt.plot(
    c_dates, 
    c_temperatures, 
    marker='.', 
    linestyle='-', 
    color=f"{spitbran_config.cfg_colours['c-rean']}", 
    label="CMEMS SST"
)
plt.plot(
    c_dates, 
    m_temperatures, 
    marker='.', 
    linestyle='-', 
    color=f"{spitbran_config.cfg_colours['m']}", 
    label="MITgcm-BFM SST")

# Add title, labels, and grid
plt.title(f"Temperature Curve (Thetao) for the Year {target_date}")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)

# Add legend
plt.legend(loc="upper right", bbox_to_anchor=(1, 1))

# Rotate the date labels for better readability
plt.xticks(rotation=45)

# Tight layout to avoid clipping of legend
plt.tight_layout()

# Save image
plt.savefig(rf"{cwd}/IMAGES/{target_date}--{latitude}-{longitude}--sst.png", dpi=300, bbox_inches='tight')

# Show the plot
plt.show()