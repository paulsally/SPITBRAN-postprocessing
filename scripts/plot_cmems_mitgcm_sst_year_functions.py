import sys
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

# Check if python script is running in interactive mode or by command line
if hasattr(sys, "ps1"):
    default_value = "2012"
    cwd = Path.cwd()
    requested_date = input("Enter the requested year in format YYYY: ") or default_value
else:                                  # Interactive window
    cwd = str(Path(__file__).resolve().parent.parent)
    if len(sys.argv) == 2:
        requested_date = sys.argv[1]
    else:
        sys.exit("Missing argument date in format YYYY")

# Add the parent directory of the script to sys.path to allow working in command line mode
sys.path.append(cwd)
from lib import my_sys_utilities

# Check if requested date is a valid date
try:
    requested_date_dobj = datetime.strptime(requested_date, "%Y")
    requested_date_year = str(requested_date_dobj.year)
except Exception as e:
    print(f"{requested_date} is not a valid date: need YYYY")
    sys.exit()

# Location and depth
latitude = 44.0
longitude = 9.0
# lat_idx = 250
# lon_idx = 380
depth_index = 0

# Load CMEMS data
# c_data_base_dir = fr"/OCEANASTORE/database/CMEMS/rean-d"
c_data_base_dir = Path(fr"~/SPITBRAN/DATA/CMEMS/rean-d").expanduser()
# c_data_search_dir = fr"{c_data_base_dir}/{requested_date_year}"
c_data_search_dir = c_data_base_dir

# Initialize lists for dates and temperatures
c_dates = []
c_temperatures = []
# Search CMEMS data for files concerning required year
matches_c = my_sys_utilities.get_files_by_keystring_in_fn("c-rean", c_data_search_dir, "tem", requested_date)
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
matches_m = my_sys_utilities.get_files_by_keystring_in_fn("m", m_data_search_dir, "TEMP", requested_date)
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
plt.plot(c_dates, c_temperatures, marker='o', linestyle='-', color='b', label="CMEMS SST")
plt.plot(c_dates, m_temperatures, marker='x', linestyle='--', color='g', label="MITgcm-BFM")

# Add title, labels, and grid
plt.title(f"Temperature Curve (Thetao) for the Year {requested_date}")
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
plt.savefig(rf"{cwd}/IMAGES/{requested_date}--{latitude}-{longitude}--sst.png", dpi=300, bbox_inches='tight')

# Show the plot
plt.show()