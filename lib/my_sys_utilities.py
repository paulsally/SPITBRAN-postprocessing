import spitbran_config
import sys
from datetime import datetime
from pathlib import Path
import re


def get_target_date (
    p_default_value,
    p_default_format,
):
    """
    Gets the target date in both, interactive and command line, execution modes.
        
    Parameters
    ----------
    p_default_value :           str
                                Default value for the requested date.
    p_default_format :          str
                                Default string format for requested date

    Returns
    -------
    target_date:                str
                                Target date we want to analyse data for
    """
    if hasattr(sys, "ps1"):
        target_date = input(f"Enter the target date in format {p_default_format} (def {p_default_value}): ") or p_default_value
    else:
        if len(sys.argv) == 2:
            target_date = sys.argv[1]
        else:
            sys.exit(f"Missing argument date in format  {p_default_format}")
    return target_date


def get_target_var (
    p_default_value,
):
    """
    Gets the target var in both, interactive and command line, execution modes.
        
    Parameters
    ----------
    p_default_value :           str
                                Default value for the requested variable (see config file).

    Returns
    -------
    target_var:                 str
                                Target var we want to analyse data for
    """
    if hasattr(sys, "ps1"):
        target_var = input(f"Enter the target var (def {p_default_value}): ") or p_default_value
    else:
        if len(sys.argv) == 2:
            target_var = sys.argv[1]
        else:
            sys.exit(f"Missing argument var")
    return target_var


# def get_target_date_obj(
#         p_target_date,
#         p_target_date_format,
# ):
#     """
#     Checks if the target date is a valid date.
        
#     Parameters
#     ----------
#     p_target_date :             str
#                                 Target date we want to analyse data for
#     p_target_date_format :      str
#                                 Target date format

#     Returns
#     -------
#     target_date_dobj:           datetime
#                                 Target date we want to analyse data for as datetime object
#     target_date_year:           str
#                                 Target date year
#     """

#     date_format_mapping = {
#         "YYYYMM": "%Y%m",
#         "YYYYMMDD": "%Y%m%d",
#     }
#     try:
#         target_date_dobj = datetime.strptime(p_target_date, date_format_mapping[p_target_date_format])
#         return target_date_dobj
#     except Exception as e:
#         raise(f"Error while processing: {e}. {p_target_date} is not a valid date: need {p_target_date_format}")
    

# def get_ref_date(p_ds):
#     """
#     Gets the reference date for the dataset.
        
#     Parameters
#     ----------
#     p_ds :                      str
#                                 Name of the dataset e.g. CMEMS or MITgcm.

#     Returns
#     -------
#     ref_date[p_ds]:             datetime
#                                 Reference date for the dataset as datetime object
#     """
#     return datetime.strptime(spitbran_config.ref_dates[p_ds], "%Y-%m-%d")


def get_files_by_keystring_in_fn(p_root_dir, p_ds_type, p_var, p_keydatestring):
    """
    Searches for files in the root directory that contain the key string in the file name.

    Parameters
    ----------
    p_root_dir :                str
                                Root directory to search for files.
    p_ds_type :                 str
                                Dataset type (c for CMEMS, m for MITgcm).
    p_var :                     str
                                Variable name (see spitbran_config file).
    p_keydatestring :           str
                                Key string to search for in the file name.
    
    Returns
    -------
    matches :                   list
                                List of files that contain the key string in the file name.
    """
    root_path = Path(p_root_dir)
    if p_ds_type == "c":
        pattern = re.compile(fr"^[^\d]{{5}}_{spitbran_config.cfg_var_filename_map[p_var]['c']}-.*_{p_keydatestring}[^()]*\.nc$")
    elif p_ds_type == "m":
        pattern = re.compile(fr"^{p_keydatestring}\d{{2}}_.*--{spitbran_config.cfg_var_filename_map[p_var]['m']}[^()]*\.nc$")
    matches = [item for item in root_path.rglob("*") if pattern.match(item.name)]
    return matches