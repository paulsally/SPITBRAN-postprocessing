import os
import numpy as np
import netCDF4 as nc

# %%
# Load CMEMS Reanalysis files for SST (1 file with all values, e.g. a whole month, values daily averaged)
# Load the first dataset (daily averages)
c_filepath = r"DATA/CMEMS/med-cmcc-tem-rean-d_thetao_6.08E-12.12E_41.90N-44.48N_1.02m_2012-11-01-2012-11-30.nc"
c_ds = nc.Dataset(c_filepath, 'r')
c_sst = c_ds.variables['thetao'][:]
c_time = c_ds.variables['time'][:]
c_lat = c_ds.variables['latitude'][:]
c_lon = c_ds.variables['longitude'][:]


# %%
# Load MITgcm output files for SST (1 file per day, values every 3 hours)
# Adjust timestap to make them daily:
#   For each file
#       - Extract SST values (they should be 4)
#       - Sum all values and divide by 4 (daily avarage)

m_output_files_dir = r"DATA/MITgcm/"
prefix = "201211"
m_output_files = [
    mof 
    for mof in sorted(os.listdir(m_output_files_dir), key=str.casefold)
    if mof.startswith(prefix)
]

for m_file in m_output_files:
    # Load the 3-hourly data for a single day
    m_ds = nc.Dataset(m_file, 'r')
    m_sst = m_ds.variables['thetao'][:]  # Shape: (8, lat, lon) for 3-hourly data
    m_sst_daily_avg = np.mean(m_sst, axis=0)  # Average along the time dimension (axis 0)
    daily_avg_sst.append(daily_avg)
    ds_hourly.close()