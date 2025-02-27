import netCDF4 as nc
import matplotlib.pyplot as plt


test_ds = nc.Dataset("/OCEANASTORE/progetti/spitbran2/2013/20130101/20130101_h-OGS--TEMP-MITgcmBFM-pilot8-b20130101_fc-v01.nc", 'r')
# test_ds = nc.Dataset("/OCEANASTORE/progetti/spitbran2/MITgcm_products/outputs/20130101/20130101_h-OGS--TEMP-MITgcmBFM-pilot8-b20130101_fc-v01.nc", 'r')
# c_time = test_ds.variables['time'][0]

# test_ds_2 = nc.Dataset("/OCEANASTORE/progetti/spitbran2/2013/20130131/20130131_h-OGS--TEMP-MITgcmBFM-pilot8-b20130131_fc-v01.nc", 'r')

# test_ds_2.variables.keys()
# c_time_2 = test_ds_2.variables['time'][0]


# test_ds_3 = nc.Dataset("/OCEANASTORE/progetti/spitbran2/flood_2012/20121101/20121101_h-OGS--TEMP-MITgcmBFM-pilot8-b20121101_fc-v01.nc", 'r')
# test_ds_3.variables.keys()

# time = test_ds.variables['time'][:]
# depth = test_ds.variables['depth'][:]
latitude = test_ds.variables['latitude'][:]
longitude = test_ds.variables['longitude'][:]
# thetao = test_ds.variables['thetao'][0, 0, :, :]
thetao = test_ds.variables['thetao'][4, 0, :, :]

# fig, axs = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)
# fig.suptitle("Test 2")
lat_min, lat_max = 42, 44
lon_min, lon_max = 6, 12
# ds_image = axs.imshow(
#     thetao, 
#     extent=[
#         lon_min, lon_max,
#         lat_min, lat_max,
#     ],
#     origin='lower', 
#     cmap='coolwarm', 
#     vmin=11, 
#     vmax=17
# )
# # Adjust aspect ratio
# axs.set_aspect(abs((lon_max - lon_min) / (lat_max - lat_min)))  # Maintain aspect ratio

fig, axs = plt.subplots(figsize=(12, 6), constrained_layout=True)
mesh = axs.pcolormesh(
    longitude, 
    latitude, 
    thetao, 
    cmap="coolwarm", 
    vmin=11, vmax=17

)
plt.colorbar(mesh, ax=axs)
axs.set_title("Thetao")
axs.set_xlabel("Longitude")
axs.set_ylabel("Latitude")
plt.show()