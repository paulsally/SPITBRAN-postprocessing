import netCDF4 as nc
from datetime import datetime, timedelta


test_ds = nc.Dataset("/OCEANASTORE/progetti/spitbran2/2013/20130131/20130131_h-OGS--TEMP-MITgcmBFM-pilot8-b20130131_fc-v01.nc", 'r')

c_time = test_ds.variables['time'][0]

test_ds_2 = nc.Dataset("/OCEANASTORE/progetti/spitbran2/2013/20130101/20130101_h-OGS--TEMP-MITgcmBFM-pilot8-b20130101_fc-v01.nc", 'r')
test_ds_2.variables.keys()
c_time_2 = test_ds_2.variables['time'][0]


test_ds_3 = nc.Dataset("/OCEANASTORE/progetti/spitbran2/flood_2012/20121101/20121101_h-OGS--TEMP-MITgcmBFM-pilot8-b20121101_fc-v01.nc", 'r')
test_ds_3.variables.keys()
c_time = test_ds_3.variables['time'][:]
c_depth = test_ds_3.variables['depth'][:]
c_latitude = test_ds_3.variables['latitude'][:]
c_longitude = test_ds_3.variables['longitude'][:]
c_thetao = test_ds_3.variables['thetao'][:]