import sys
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

# Check if python script is running in interactive mode or by command line
if hasattr(sys, "ps1"):   # Command line
    default_value = "20130101"
    cwd = Path.cwd()
    requested_date = input("Enter the requested date in format YYYYMMDD: ") or default_value
else:                                  # Interactive window
    cwd = str(Path(__file__).resolve().parent.parent)
    if len(sys.argv) == 2:
        requested_date = sys.argv[1]
    else:
        sys.exit("Missing argument date in format YYYMMDD")

# Add the parent directory of the script to sys.path to work in command line execution
sys.path.append(cwd)
from lib import my_functions

# Check if requested date is a valid date
try:
    requested_date_dobj = datetime.strptime(requested_date, "%Y%m%d")
    requested_date_year = str(requested_date_dobj.year)
except Exception as e:
    print(f"{requested_date} is not a valid date: need YYYYMMDD")
    sys.exit()

# %% 
# Load CMEMS data
#   Check if data for requested date is found
#   It selects first file with requested data found
c_data_base_dir = fr"/OCEANASTORE/database/CMEMS/rean-d"
c_data_search_dir = fr"/OCEANASTORE/database/CMEMS/rean-d/{requested_date_year}"

c_filepath = ""
try:
    for c_item in sorted(Path(c_data_search_dir).iterdir()):
        c_item_name = c_item.name
        if (
            c_item.is_file() 
            and c_item.stem.endswith(requested_date)
            and "_tem-" in c_item_name
            ):
            c_filepath = fr"{c_data_search_dir}/{c_item_name}"
            break
except Exception as e:
    sys.exit(f"{c_data_search_dir} not found")

# # c_product = "med-cmcc-tem-rean-d" # Reanalysis
# # c_var = "thetao"
# # c_extent = "6.08E-12.12E_41.90N-44.48N"
# # c_d = "1.02m"
# # c_filepath = fr"{c_data_basedir}/{c_product}_{c_var}_{c_extent}_{c_d}_{c_s_date}-{c_e_date}.nc"
# # c_filepath = rf"DATA/CMEMS/med-cmcc-tem-rean-d_thetao_6.08E-12.12E_41.90N-44.48N_1.02m_2012-11-01-2012-11-30.nc"
c_ds = nc.Dataset(c_filepath, 'r')

# Load MITgcm output file
# # m_filepath = r"DATA/MITgcm/20121101_h-OGS--TEMP-MITgcmBFM-pilot8-b20121031_fc-v01.nc"
m_data_basedir = r"/OCEANASTORE/progetti/spitbran2"
m_data_search_dir = fr"{m_data_basedir}/{requested_date_year}"
# Assuming output cycle is 2 days:
#   Set default date subdir to previous day
#   If date subdir exists with same date as requested date override default value
m_previous_day = (requested_date_dobj - timedelta(days=1)).strftime("%Y%m%d")
m_data_search_subdir = fr"{m_data_search_dir}/{m_previous_day}"
for m_data_search_dir_file in sorted(Path(m_data_search_dir).iterdir()): 
    m_date_subdir = m_data_search_dir_file.name
    if m_date_subdir == requested_date:
        m_data_search_subdir = fr"{m_data_search_dir}/{m_date_subdir}"
        break

m_filepath = ""
try:
    for m_item in sorted(Path(m_data_search_subdir).iterdir()):
        m_item_name = m_item.name
        if (
                m_item.is_file() 
                and m_item.stem.startswith(requested_date) 
                and "OGS--TEMP-MITgcmBFM" in m_item_name
            ):
            m_filepath = fr"{m_data_search_subdir}/{m_item_name}"
            break
except Exception as e:
    sys.exit(f"{m_data_search_dir} not found")

m_ds = nc.Dataset(m_filepath, 'r')

# %%
# Extract SST data of the target time and depth 
# print(m_filepath)
# print(c_ds.variables.keys())
c_sst = c_ds.variables['thetao'][0, 0, :, :]  # ('time', 'depth', 'latitude', 'longitude')
# print(m_ds.variables['thetao'].dimensions)

m_sst = m_ds.variables['thetao'][:, 0, :, :].mean(axis=0)  # MITgcm: 3-hourly outputs so need to take avarage of the 8 values per day
m_sst_d1 = m_ds.variables['thetao'][:, 1, :, :].mean(axis=0) # Second layer
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
c_im = my_functions.plot_map_minmax_nocb(
    axs[0],
    "CMEMS",
    c_sst,
    c_lon.min(), c_lon.max(), 
    c_lat.min(), c_lat.max(),
    sst_min, sst_max,
)

# Plot the second dataset (m SST daily avaraged)
m_im = my_functions.plot_map_minmax_nocb(
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
c_im_d1 = my_functions.plot_map_minmax_nocb(
    axs_d1[0],
    "CMEMS",
    c_sst,
    c_lon.min(), c_lon.max(), 
    c_lat.min(), c_lat.max(),
    sst_min, sst_max,
)

# Plot the second dataset (m SST daily avaraged)
m_im_d1 = my_functions.plot_map_minmax_nocb(
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
