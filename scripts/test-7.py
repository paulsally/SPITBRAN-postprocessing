"""
water column profile
"""
import netCDF4 as nc
import matplotlib.pyplot as plt


import spitbran_config
# from lib import my_sys_utilities
from lib import my_nc_utilities
# from lib import my_plot_utilities

test_ds_w_c_insitu = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/insitu/INSITU_GLO_PHY_TS_DISCRETE_MY_013_001/cmems_obs-ins_glo_phy-temp-sal_my_easycora_irr_202411/mediterrane/2012/ECO_DMQCGL01_20120103_PR_CT.nc", 'r')
test_ds_s_c_insitu = nc.Dataset("/home/polselli/SPITBRAN/DATA/CMEMS/insitu/INSITU_GLO_PHY_TS_DISCRETE_MY_013_001/cmems_obs-ins_glo_phy-temp-sal_my_easycora_irr_202411/mediterrane/2012/ECO_DMQCGL01_20120701_PR_CT.nc", 'r')

# Fixed time, lat, lon

depth_w_c_insitu = test_ds_w_c_insitu.variables['DEPH'][1, :]
depth_s_c_insitu = test_ds_s_c_insitu.variables['DEPH'][1, :]


thetao_w_c_insitu_profile = test_ds_w_c_insitu.variables['TEMP'][1, :]
thetao_s_c_insitu_profile = test_ds_s_c_insitu.variables['TEMP'][1, :]
print(thetao_s_c_insitu_profile[5:10])
print(depth_s_c_insitu)

# Extract units from dataset attributes
depth_w_c_insitu_unit = test_ds_w_c_insitu.variables['DEPH'].units
temp_s_c_insitu_unit = test_ds_s_c_insitu.variables['TEMP'].units

#plt.figure(figsize=(12, 6))

fig, ax = plt.subplots(figsize=(6, 8))

ax.plot(
    thetao_w_c_insitu_profile, 
    depth_w_c_insitu,
    marker=",", 
    linestyle="solid", 
    # color=spitbran_config.cfg_colours["c-rean"]["seasonal"]["winter"],
    color="y",
    label="C Insitu Winter",
)
ax.plot(
    thetao_s_c_insitu_profile, 
    depth_s_c_insitu,
    marker=",", 
    linestyle="solid", 
    # color=spitbran_config.cfg_colours["c-rean"]["seasonal"]["summer"],
    color="r",
    label="C Insitu Summer",
)


plt.gca().invert_yaxis()

plt.xlabel(f"Temperature ({temp_s_c_insitu_unit})")
plt.ylabel(f"Depth ({depth_w_c_insitu_unit})")

# Add title and legend
plt.title("Temperature Profile from NetCDF Data")
plt.legend()

# Show grid
plt.grid()

# Show plot
plt.show()