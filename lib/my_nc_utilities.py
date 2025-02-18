import netCDF4 as nc
import numpy as np
from datetime import timedelta
from dateutil.parser import parse
from lib import my_sys_utilities


def get_time_defaults(p_ds):
    """
    Extracts the time defaults from the dataset.
       
    Parameters
    ----------
    p_ds :                      netCDF4.Dataset
                                Dataset object.

    Returns
    -------
    time unit :                 str
                                Unit string (e.g. seconds, minnutes, ...).
    time since :                str
                                Since date string.
    """           

    time_units_keys = ['unit', 'base']
    time_units = dict(zip(time_units_keys, p_ds.variables['time'].units.split(" since ")))
    time_base = parse(time_units['base'])

    return time_base, time_units['unit']


def get_lat_lon_idx(p_ds, p_latitude, p_longitude):
    """
    Finds the nearest latitude and longitude indices.
       
    Parameters
    ----------
    p_ds :                      netCDF4.Dataset
                                Dataset object.
    p_latitude :                float
                                Degrees North latitude.
    p_longitude :               float
                                Degrees East longitude.

    Returns
    -------
    lat_idx :                   int
                                Nearest latitude index.
    lon_idx :                   int
                                Nearest longitude index.
    """           

    p_latitudes = p_ds.variables['latitude'][:]
    p_longitudes = p_ds.variables['longitude'][:]
    p_lat_idx = np.abs(p_latitudes - p_latitude).argmin()
    p_lon_idx = np.abs(p_longitudes - p_longitude).argmin()

    return p_lat_idx, p_lon_idx


def get_values_in_point_with_time_given_month(
    p_ds_type,
    p_data_base_dir,
    p_target_date,
    p_var,
    p_var_fn_mapped,
    p_latitude,
    p_longitude,
    p_depth_index,
    p_var_d=False,
):
    """
    Searches the MITgcm-BFM data directory for files related to the target date (a month in format YYYYMM) and extracts the variable time series values for the given depth, lat, and lon.
       
    Parameters
    ----------
    p_ds_type :                 str
                                String corresponding to the type of dataset (c for CMEMS, m for MITgcm-BFM).
    p_data_base_dir :           str
                                String corresponding to the path where data files are located.
    p_target_date :             str
                                Target date in the format YYYYMM.
    p_var :                     str
                                Varibale to extract from the data files.
    p_var_fn_mapped :           str
                                Mapped variable name as per the config file (as it shows in data filenames).
    p_latitude :                float
                                Degrees North latitude.
    p_longitude :               float
                                Degrees East longitude.
    p_depth_index :             int
                                Depth index (indicates the layer).
    p_var_d :                   bool
                                Flag to compute average daily variable values.


    Returns
    -------
    x :                         list
                                The values to plot on the x-axis.
    y :                         list
                                The values to plot on the y-axis.
    y_d :                       list
                                The average daily values to plot on the y-axis
    var_long_name :             str
                                The long name of the variable.
    var_units :                 str
                                The units of the variable.
    """

    x = []
    y = []
    y_d = []

    matches = sorted(
        my_sys_utilities.get_files_by_keystring_in_fn(
            p_ds_type,
            p_data_base_dir, 
            p_var_fn_mapped,
            p_target_date,
        )
    )

    i = 0
    for (item) in matches:
        with nc.Dataset(item, "r") as ds:
            if i == 0:
                # Find nearest latitude and longitude cell indices
                lat_idx, lon_idx = get_lat_lon_idx(
                    ds, 
                    p_latitude, 
                    p_longitude
                )
                # Get time defaults (base reference time and time unit)
                time_base, time_unit = get_time_defaults(ds)

            time = ds.variables['time'][:]
            new_time = [time_base + timedelta(**{time_unit: int(t)}) for t in time]
            x.extend(new_time)

            if p_ds_type == "c-rean":
                var_units = ds.variables[p_var].units
                var_long_name = ds.variables[p_var].long_name
              
            # Extract variable values for the given depth, lat and lon (cell)
            # print(ds.variables.keys())
            var_values = ds.variables[p_var][:, p_depth_index, lat_idx, lon_idx]
            y.extend(var_values)

            # Compute average daily variable values
            if (p_var_d == True):
                var_d = ds.variables[p_var][:, p_depth_index, lat_idx, lon_idx].mean(axis=0)
                y_d.append(var_d)

        i += 1

    if p_ds_type == "c-rean":
        return x, y, var_long_name, var_units
    elif p_ds_type == "m":
        return x, y, y_d

   
def get_values_map_specific_day(
    p_ds_type,
    p_data_base_dir,
    p_target_date,
    p_var_fn_mapped,
):
    """
    Searches the MITgcm-BFM data directory for files related to the target date (a month if format YYYYMM) and extracts the variable time series values for the given depth, lat, and lon.
       
    Parameters
    ----------
    p_ds_type :                 str
                                String corresponding to the type of dataset (c for CMEMS, m for MITgcm-BFM).
    p_data_base_dir :           str
                                String corresponding to the path where data files are located.
    p_target_date :             str
                                Target date in the format YYYYMM.
    p_var_fn_mapped :           str
                                Mapped variable name as per the config file (as it shows in data filenames).


    Returns
    -------
    ds :                        a netCDF4.Dataset object
                                The dataset object to plot.
    """

    match = my_sys_utilities.get_files_by_keystring_in_fn(
            p_ds_type,
            p_data_base_dir,
            p_var_fn_mapped,
            p_target_date,
    )
  
    try:
        fp = match[0]
    except IndexError:
        raise RuntimeError(f"No files found for the target date: {p_target_date} in {p_data_base_dir}")
    ds = nc.Dataset(fp, "r")
    return ds
