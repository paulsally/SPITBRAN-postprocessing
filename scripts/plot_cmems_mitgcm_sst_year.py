import sys
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

# Check if python script is running in interactive mode or by command line
if hasattr(sys, "ps1"):
    default_value = "2013"
    cwd = Path.cwd()
    requested_date = input("Enter the requested year in format YYYY: ") or default_value
else:                                  # Interactive window
    cwd = str(Path(__file__).resolve().parent.parent)
    if len(sys.argv) == 2:
        requested_date = sys.argv[1]
    else:
        sys.exit("Missing argument date in format YYYY")

# Add the parent directory of the script to sys.path to allow working in command line execution
sys.path.append(cwd)
# from lib import my_functions

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

# %% 
# Load CMEMS data
#   Check if data for requested date is found
#   It selects first file with requested data found
c_data_base_dir = fr"/OCEANASTORE/database/CMEMS/rean-d"
c_data_search_dir = fr"/OCEANASTORE/database/CMEMS/rean-d/{requested_date_year}"

# Initialize lists for dates and temperatures
c_dates = []
c_temperatures = []

# Search CMEMS data for files concerning required month
c_filepath = ""
c_ds = []

for c_item in sorted(Path(c_data_search_dir).iterdir()):
    c_item_name = c_item.name
    if (
        c_item.is_file() 
        and c_item.stem[: -2].endswith(requested_date)
        and "_tem-" in c_item_name
        ):
        # Parse the date from the filename
        c_file_date = (datetime.strptime(c_item_name[-11:-3], "%Y%m%d")).date()
        c_dates.append(c_file_date)
        c_filepath = fr"{c_data_search_dir}/{c_item_name}"
        with nc.Dataset(c_filepath, 'r') as c_ds:
            # Find nearest latitude and longitude indices
            latitudes = c_ds.variables['latitude'][:]
            longitudes = c_ds.variables['longitude'][:]
            lat_idx = np.abs(latitudes - latitude).argmin()
            lon_idx = np.abs(longitudes - longitude).argmin()
            # Extract temperature for the given depth, lat, and lon
            thetao = c_ds.variables['thetao'][0, depth_index, lat_idx, lon_idx]
            c_temperatures.append(thetao)

# %% 
# Load MITgcm-BFM
m_data_basedir = r"/OCEANASTORE/progetti/spitbran2"
m_data_search_dir = fr"{m_data_basedir}/{requested_date_year}"

# Initialize list for temperatures
m_temperatures = []

# Search for files concerning required month
m_filepath = ""
m_ds = []
for m_data_search_dir_item in sorted(Path(m_data_search_dir).iterdir()): 
    m_data_search_dir_date_subdir_name = m_data_search_dir_item.name
    if m_data_search_dir_date_subdir_name[:6] == requested_date:
        for (m_item) in sorted(Path(f"{m_data_search_dir}/{m_data_search_dir_date_subdir_name}").iterdir()):
            m_item_name = m_item.name
            if (
                    m_item.is_file() 
                    and m_item.stem.startswith(requested_date) 
                    and "OGS--TEMP-MITgcmBFM" in m_item_name
                ):
                m_filepath = fr"{m_data_search_dir}/{m_data_search_dir_date_subdir_name}/{m_item_name}"
                with nc.Dataset(m_filepath, 'r') as m_ds:
                    # Find nearest latitude and longitude indices
                    latitudes = m_ds.variables['latitude'][:]
                    longitudes = m_ds.variables['longitude'][:]
                    lat_idx = np.abs(latitudes - latitude).argmin()
                    lon_idx = np.abs(longitudes - longitude).argmin()
                    # Extract temperature for the given depth, lat, and lon
                    thetao = m_ds.variables['thetao'][:, depth_index, lat_idx, lon_idx]
                    m_temperatures.append(thetao)

# Plot the temperature curves
plt.figure(figsize=(10, 6))
plt.plot(c_dates, c_temperatures, marker='o', linestyle='-', color='b', label="CMEMS SST")
plt.plot(c_dates, m_temperatures, marker='x', linestyle='--', color='g', label="MITgcm-BFM")

# Add title, labels, and grid
plt.title("Temperature Curve (Thetao) for the Month")
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