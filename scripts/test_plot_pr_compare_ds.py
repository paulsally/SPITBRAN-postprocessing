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
test_ds_w_c_rean = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/rean-d/cmems_tem-rean_d_20120101.nc", 'r')
test_ds_s_c_rean = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/rean-d/cmems_tem-rean_d_20120701.nc", 'r')
test_ds_w_m = nc.Dataset("/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs/20120101/20120101_h-OGS--TEMP-MITgcmBFM-pilot8-b20120101_fc-v01.nc", 'r')
test_ds_s_m = nc.Dataset("/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs/20120701/20120701_h-OGS--TEMP-MITgcmBFM-pilot8-b20120701_fc-v01.nc", 'r')
test_ds_w_c_insitu = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/insitu/INSITU_GLO_PHY_TS_DISCRETE_MY_013_001/cmems_obs-ins_glo_phy-temp-sal_my_easycora_irr_202411/mediterrane/2012/ECO_DMQCGL01_20120101_PR_CT.nc", 'r')
test_ds_s_c_insitu = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/insitu/INSITU_GLO_PHY_TS_DISCRETE_MY_013_001/cmems_obs-ins_glo_phy-temp-sal_my_easycora_irr_202411/mediterrane/2012/ECO_DMQCGL01_20120701_PR_CT.nc", 'r')


# Fixed time, lat, lon
depth_w_c_rean = test_ds_w_c_rean.variables['depth'][:]
depth_w_c_insitu = test_ds_w_c_insitu.variables['DEPH'][0, :]
depth_s_c_insitu = test_ds_s_c_insitu.variables['DEPH'][0, :]
depth_w_m = test_ds_w_m.variables['depth'][:]

time = 0

lat_idx_c_rean, lon_idx_c_rean = my_nc_utilities.get_lat_lon_idx(test_ds_w_c_rean, spitbran_config.cfg_latitude, spitbran_config.cfg_longitude)
thetao_w_c_rean_profile = test_ds_w_c_rean.variables['thetao'][time, :, lat_idx_c_rean, lon_idx_c_rean]
thetao_s_c_rean_profile = test_ds_s_c_rean.variables['thetao'][time, :, lat_idx_c_rean, lon_idx_c_rean]

lat_idx_c_insitu, lon_idx_c_insitu = my_nc_utilities.get_lat_lon_idx(test_ds_w_c_insitu, spitbran_config.cfg_latitude, spitbran_config.cfg_longitude)
print("depth ", test_ds_w_c_insitu.variables['DEPH'].dimensions)
print("temp ", test_ds_w_c_insitu.variables['TEMP'].dimensions)

thetao_w_c_insitu_profile = test_ds_w_c_insitu.variables['TEMP'][1, :]
thetao_s_c_insitu_profile = test_ds_s_c_insitu.variables['TEMP'][1, :]

lat_idx_m, lon_idx_m = my_nc_utilities.get_lat_lon_idx(test_ds_w_m, spitbran_config.cfg_latitude, spitbran_config.cfg_longitude)
thetao_w_m_profile = test_ds_w_m.variables['thetao'][:, :, lat_idx_m, lon_idx_m].mean(axis=0)
thetao_s_m_profile = test_ds_s_m.variables['thetao'][:, :, lat_idx_m, lon_idx_m].mean(axis=0)

# Extract units from dataset attributes
depth_w_m_units = test_ds_w_m.variables['depth'].units
thetao_w_m_units = test_ds_w_m.variables['thetao'].units

#plt.figure(figsize=(12, 6))

fig, ax1 = plt.subplots(figsize=(6, 8))


ax1.plot(
    thetao_w_c_rean_profile, 
    depth_w_c_rean,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_datasets["c-rean"]["colour"]["seasonal"]["winter"],
    label="C Rean Winter",
)
ax1.plot(
    thetao_s_c_rean_profile, 
    depth_w_c_rean,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_datasets["c-rean"]["colour"]["seasonal"]["summer"],
    label="C Rean Summer",
)
ax1.invert_yaxis()


ax2 = ax1.twinx()
ax2.plot(
    thetao_w_c_insitu_profile, 
    depth_w_c_insitu,
    marker=",", 
    linestyle="solid", 
    # color=spitbran_config.cfg_datasets["c-rean"]["colour"]["seasonal"]["winter"],
    color="y",
    label="C Insitu Winter",
)
ax2.plot(
    thetao_s_c_insitu_profile, 
    depth_s_c_insitu,
    marker=",", 
    linestyle="solid", 
    # color=spitbran_config.cfg_datasets["c-rean"]["colour"]["seasonal"]["summer"],
    color="r",
    label="C Insitu Summer",
)

ax1.plot(
    thetao_w_m_profile, 
    depth_w_m,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_datasets["m"]["colour"]["seasonal"]["winter"],
    label="M Winter",
)
ax1.plot(
    thetao_s_m_profile, 
    depth_w_m,
    marker=",", 
    linestyle="solid", 
    color=spitbran_config.cfg_datasets["m"]["colour"]["seasonal"]["summer"],
    label="M Summer",
)

plt.gca().invert_yaxis()


# **Set labels dynamically using dataset units**
# ax1.set_xlabel(f"Temperature ({thetao_w_m_units})")
# ax1.set_ylabel(f"Depth ({depth_w_m_units})")
plt.xlabel(f"Temperature ({thetao_w_m_units})")
plt.ylabel(f"Depth ({depth_w_m_units})")

# Add title and legend
plt.title("Temperature Profile from NetCDF Data")
# plt.legend()
# Get handles and labels from both axes
lines_ax1, labels_ax1 = ax1.get_legend_handles_labels()
lines_ax2, labels_ax2 = ax2.get_legend_handles_labels()

# Combine legends and add to the plot
plt.legend(lines_ax1 + lines_ax2, labels_ax1 + labels_ax2, loc="lower right")


# Show grid
plt.grid()

# Show plot
plt.show()