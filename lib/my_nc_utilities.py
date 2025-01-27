import spitbran_config
import netCDF4 as nc
import numpy as np
from datetime import datetime, timedelta
from lib import my_sys_utilities
from pathlib import Path
import spitbran_config


# def get_c_data(
#     p_c_data_base_dir,
#     p_target_date,
#     p_latitude,
#     p_longitude,
#     p_depth_index,
#     p_c_var,
# ):
#     """
#     Searches the CMEMS data directory for files related to the target month and extracts the variable values for the given depth, lat, and lon.
       
#     Parameters
#     ----------
#     p_c_data_base_dir :         str
#                                 String corresponding to the path where data files are located.
#     p_target_date :             str
#                                 Target date in the format YYYYMM.
#     p_latitude :                float
#                                 Degrees North latitude.
#     p_longitude :               float
#                                 Degrees East longitude.
#     p_c_var :                   str
#                                 Varibale to extract from the data files.

#     Returns
#     -------
#     c_x :                       list
#                                 The values to plot on the x-axis.
#     c_y :                       list
#                                 The values to plot on the y-axis.
#     """

#     c_filepath = ""
#     c_x = []
#     c_y = []
#     c_base_time = datetime(1900, 1, 1, 0, 0, 0)

#     target_date_year = my_sys_utilities.get_target_date_obj(p_target_date, "YYYYMM").year
#     c_data_search_dir = fr"{p_c_data_base_dir}/{target_date_year}"
    
#     c_fn = 0
#     for c_item in sorted(Path(c_data_search_dir).iterdir()):
#         c_item_name = c_item.name
#         c_time_conditions = {
#             "get_by_month":  lambda c_item_name, p_target_date: c_item.stem[: -2].endswith(p_target_date),
#         }
#         if (
#                 c_item.is_file() 
#                 and c_time_conditions["get_by_month"](c_item_name, p_target_date)
#                 #and c_item.stem[: -2].endswith(p_target_date)
#                 and f"_{spitbran_config.cfg_var_filename_map[p_c_var]['c']}-" in c_item_name
#             ):
#             c_filepath = fr"{c_data_search_dir}/{c_item_name}"
#             with nc.Dataset(c_filepath, "r") as c_ds:
#                 if c_fn == 0:
#                     # Find nearest latitude and longitude cell indices
#                     c_lat_idx, c_lon_idx = get_lat_lon_idx(c_ds, p_latitude, p_longitude)

#                 c_time = c_ds.variables['time'][:]
#                 # Format times (x-axis)  
#                 c_new_time = [c_base_time + timedelta(minutes=int(t)) for t in c_time]
#                 c_x.extend(c_new_time)

#                 # Extract variable values for the given depth, lat, and lon (cell)
#                 c_var_units = c_ds.variables[p_c_var].units
#                 c_var_long_name = c_ds.variables[p_c_var].long_name
#                 c_var_values = c_ds.variables[p_c_var][:, p_depth_index, c_lat_idx, c_lon_idx]
#                 c_y.append(c_var_values)

#                 c_fn += 1
#     return c_x, c_y, c_var_long_name, c_var_units


# def get_m_data(
#     p_m_data_base_dir,
#     p_target_date,
#     p_latitude,
#     p_longitude,
#     p_depth_index,
#     p_m_var,
#     p_m_var_d=False
# ):
#     """
#     Searches the MITgcm-BFM data directory for files related to the target month and extracts the variable values for the given depth, lat, and lon.
       
#     Parameters
#     ----------
#     p_m_data_base_dir :         str
#                                 String corresponding to the path where data files are located.
#     p_target_date :             str
#                                 Target date in the format YYYYMM.
#     p_latitude :                float
#                                 Degrees North latitude.
#     p_longitude :               float
#                                 Degrees East longitude.
#     p_m_var :                   str
#                                 Varibale to extract from the data files.

#     Returns
#     -------
#     m_x :                       list
#                                 The values to plot on the x-axis.
#     m_y :                       list
#                                 The values to plot on the y-axis.
#     """
#     m_filepath = ""
#     m_x = []
#     m_y = []
#     m_base_time = datetime(1970, 1, 1, 0, 0, 0)
#     m_y_d = []

#     target_date_year = my_sys_utilities.get_target_date_obj(p_target_date, "YYYYMM").year
#     m_data_search_dir = fr"{p_m_data_base_dir}/{target_date_year}"
#     m_fn = 0
#     for m_data_search_dir_item in sorted(Path(m_data_search_dir).iterdir()): 
#         m_data_search_dir_date_subdir_name = m_data_search_dir_item.name
#         if m_data_search_dir_date_subdir_name[:6] == p_target_date:
#             for (m_item) in sorted(Path(f"{m_data_search_dir}/{m_data_search_dir_date_subdir_name}").iterdir()):
#                 m_item_name = m_item.name
#                 if (
#                         m_item.is_file() 
#                         and m_item.stem.startswith(p_target_date) 
#                         and f"OGS--{spitbran_config.cfg_var_filename_map[p_m_var]['m']}-MITgcmBFM" in m_item_name
#                     ):
#                     m_filepath = fr"{m_data_search_dir}/{m_data_search_dir_date_subdir_name}/{m_item_name}"
#                     with nc.Dataset(m_filepath, "r") as m_ds:
#                         if m_fn == 0:
#                             # Find nearest latitude and longitude cell indices
#                             m_lat_idx, m_lon_idx = get_lat_lon_idx(m_ds, p_latitude, p_longitude)

#                         m_time = m_ds.variables['time'][:]
#                         # Format times (x-axis) 
#                         m_new_time = [m_base_time + timedelta(seconds=int(t)) for t in m_time]
#                         m_x.extend(m_new_time)
                        
#                         # Extract variable values for the given depth, lat, and lon (cell)
#                         m_var_values = m_ds.variables[p_m_var][:, p_depth_index, m_lat_idx, m_lon_idx]
#                         m_y.extend(m_var_values)

#                         # Compute avarage daily variable values
#                         if (p_m_var_d == True):
#                             m_var_d = m_ds.variables[p_m_var][:, p_depth_index, m_lat_idx, m_lon_idx].mean(axis=0)
#                             m_y_d.append(m_var_d)

#                         m_fn =+ 1
#     return m_x, m_y, m_y_d


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
    base_time = datetime.strptime(time_units['base'], "%Y-%m-%d")

    return base_time, time_units['unit']


# def get_time(p_ds, p_base_time, p_time_unit):
#     """
#     Extracts the times from the dataset.
       
#     Parameters
#     ----------
#     p_ds :                      netCDF4.Dataset
#                                 Dataset object.

#     Returns
#     -------
#     times :                     Array
#                                 Array of times.
#     """           

#     time = p_ds.variables['time'][:]
#     # Calculate the dates for x axis  
#     for t in time:
#         match p_time_unit:
#             case "days":
#                 formatted_time = p_base_time + timedelta(days=int(t))
#             case "hours":
#                 formatted_time = p_base_time + timedelta(hours=int(t))
#             case "minutes":
#                 formatted_time = p_base_time + timedelta(minutes=int(t))
#             case "seconds":
#                 formatted_time = p_base_time + timedelta(seconds=int(t))
#             case _:
#                 raise ValueError(f"Unsupported time unit: {p_time_unit}")

#     return formatted_time


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


def get_values_of_point_in_time(
    p_ds_type,
    p_target_date,
    p_var,
    p_var_d=False
):
    """
    Searches the MITgcm-BFM data directory for files related to the target date (a month if format YYYYMM) and extracts the variable time series values for the given depth, lat, and lon.
       
    Parameters
    ----------
    p_ds_type :                 str
                                String corresponding to the type of dataset (c for CMEMS, m for MITgcm-BFM).
    p_target_date :             str
                                Target date in the format YYYYMM.
    p_var :                     str
                                Varibale to extract from the data files.

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
            spitbran_config.cfg_data_base_dirs[p_ds_type], 
            p_ds_type,
            p_var,
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
                    spitbran_config.cfg_latitude, 
                    spitbran_config.cfg_longitude
                )
            time = ds.variables['time'][:]
            print(ds.variables['time'].units)

            if p_ds_type == "c":
                # Format times (x-axis)
                base_time = datetime(1900, 1, 1, 0, 0, 0)
                new_time = [base_time + timedelta(minutes=int(t)) for t in time]
                var_units = ds.variables[p_var].units
                var_long_name = ds.variables[p_var].long_name
            elif p_ds_type == "m":
                # Format times (x-axis)
                base_time = datetime(1970, 1, 1, 0, 0, 0)
                new_time = [base_time + timedelta(seconds=int(t)) for t in time]
            x.extend(new_time)
                        
            # Extract variable values for the given depth, lat, and lon (cell)
            var_values = ds.variables[p_var][:, spitbran_config.cfg_depth_index, lat_idx, lon_idx]
            y.extend(var_values)

            # Compute avarage daily variable values
            if (p_var_d == True):
                var_d = ds.variables[p_var][:, spitbran_config.cfg_depth_index, lat_idx, lon_idx].mean(axis=0)
                y_d.append(var_d)

        i += 1

    if p_ds_type == "c":
        return x, y, var_long_name, var_units
    elif p_ds_type == "m":
        return x, y, y_d