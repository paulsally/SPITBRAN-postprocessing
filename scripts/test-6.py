"""
water column profile
"""
import netCDF4 as nc
import matplotlib.pyplot as plt


import spitbran_config
# from lib import my_sys_utilities
from lib import my_nc_utilities
# from lib import my_plot_utilities


# test_ds_w_m = nc.Dataset("/OCEANASTORE/progetti/spitbran2/2013/20130101/20130101_h-OGS--TEMP-MITgcmBFM-pilot8-b20130101_fc-v01.nc", 'r')
test_ds_w_c = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/rean-d/cmems_tem-rean_d_20120101.nc", 'r')
test_ds_s_c = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/rean-d/cmems_tem-rean_d_20120701.nc", 'r')
test_ds_w_m = nc.Dataset("/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs/20120101/20120101_h-OGS--TEMP-MITgcmBFM-pilot8-b20120101_fc-v01.nc", 'r')
test_ds_s_m = nc.Dataset("/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs/20120701/20120701_h-OGS--TEMP-MITgcmBFM-pilot8-b20120701_fc-v01.nc", 'r')


# Fixed time, lat, lon
depth_w_c = test_ds_w_c.variables['depth'][:]
depth_w_m = test_ds_w_m.variables['depth'][:]

time = 0

lat_idx_c, lon_idx_c = my_nc_utilities.get_lat_lon_idx(test_ds_w_c, spitbran_config.cfg_latitude, spitbran_config.cfg_longitude)
thetao_w_c_profile = test_ds_w_c.variables['thetao'][time, :, lat_idx_c, lon_idx_c]
thetao_s_c_profile = test_ds_s_c.variables['thetao'][time, :, lat_idx_c, lon_idx_c]

lat_idx_m, lon_idx_m = my_nc_utilities.get_lat_lon_idx(test_ds_w_m, spitbran_config.cfg_latitude, spitbran_config.cfg_longitude)
thetao_w_m_profile = test_ds_w_m.variables['thetao'][:, :, lat_idx_m, lon_idx_m].mean(axis=0)
thetao_s_m_profile = test_ds_s_m.variables['thetao'][:, :, lat_idx_m, lon_idx_m].mean(axis=0)

# Extract units from dataset attributes
depth_w_m_units = test_ds_w_m.variables['depth'].units
thetao_w_m_units = test_ds_w_m.variables['thetao'].units

plt.figure(figsize=(12, 6))
plt.plot(
    thetao_w_c_profile, 
    depth_w_c,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_colours["c-rean"]["seasonal"]["winter"],
    label="C Rean Winter",
)
plt.plot(
    thetao_s_c_profile, 
    depth_w_c,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_colours["c-rean"]["seasonal"]["summer"],
    label="C Rean Summer",
)
plt.plot(
    thetao_w_m_profile, 
    depth_w_m,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_colours["m"]["seasonal"]["winter"],
    label="M Winter",
)
plt.plot(
    thetao_s_m_profile, 
    depth_w_m,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_colours["m"]["seasonal"]["summer"],
    label="M Summer",
)

plt.gca().invert_yaxis()


# **Set labels dynamically using dataset units**
plt.xlabel(f"Temperature ({thetao_w_m_units})")
plt.ylabel(f"Depth ({depth_w_m_units})")

# Add title and legend
plt.title("Temperature Profile from NetCDF Data")
plt.legend()

# Show grid
plt.grid()

# Show plot
plt.show()