# %%
# Libraries imports
from  datetime import datetime, timedelta
import matplotlib
# print(f"Current backend: {matplotlib.get_backend()}")  # Confirm the backend being used
# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'webAgg' depending on your environment

import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%% 
# Get target date and variable
target_date = "201301"

c_path = "/OCEANASTORE/database/CMEMS/rean-d/2013/cmems_tem-rean_d_20130101.nc"
m_path = "/OCEANASTORE/progetti/spitbran2/2013/20130101/20130101_h-OGS--TEMP-MITgcmBFM-pilot8-b20130101_fc-v01.nc"

c_ds = nc.Dataset(c_path, "r")
m_ds = nc.Dataset(m_path, "r")

c_time = c_ds.variables['time'][:]
m_time = m_ds.variables['time'][:]

c_temp = c_ds.variables['thetao'][:, 0, 0, 0]
m_temp = m_ds.variables['thetao'][:, 0, 0, 0]

c_base_time = datetime.strptime("1900-01-01", "%Y-%m-%d")
c_datetime = [c_base_time + timedelta(minutes=int(t)) for t in c_time]
m_base_time = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
m_datetime = [m_base_time + timedelta(seconds=int(t)) for t in m_time]

# Disable automatic browser opening
matplotlib.rcParams['webagg.open_in_browser'] = False
# Reset any previous settings
plt.rcdefaults()
plt.close('all')

# %%
# Plot the temperature curves
fig = plt.figure(num=1, figsize=(10, 6), dpi=100)
fig.clf()
ax = fig.add_subplot(111)  
line1, = ax.plot(c_datetime, c_temp, marker=".", linestyle="solid", color=f"r", label="CMEMS SST")
line2, = ax.plot(m_datetime, m_temp, marker=".", linestyle="solid", color=f"g", label="MITgcm-BFM")
#line3, = ax.plot(c_dates, m_temperatures_d, marker=".", linestyle="solid", color=f"{spitbran_config.cfg_colours['model_avg']}", label="MITgcm-BFM - Daily Avg")

# Format the x-axis to show one date per day
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
# ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Add title, labels, and grid
fig.suptitle(f"Temperature Curve (Thetao) for the Month")
# ax.autoscale()  # Reset axes to fit the data
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.grid(True)


# Add an interactive legend
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
lines = [line1, line2]

# Debug: Check if the event connection works
print("Event connections established. Ready to show the plot.")
print("Figure size:", fig.get_size_inches())
print("Figure DPI:", fig.get_dpi())

# Rotate the date labels for better readability
plt.xticks(rotation=45)

# Tight layout to avoid clipping of legend
plt.tight_layout()

#images_store_path = f"{cwd}/IMAGES"
# Save image
#plt.savefig(rf"{images_store_path}/{target_date}--{spitbran_config.cfg_latitude}-{spitbran_config.cfg_longitude}--sst.png", dpi=300, bbox_inches="tight")

# Show the plot
plt.show()