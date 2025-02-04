import sys
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
        if len(sys.argv) > 2:
            target_date = sys.argv[1]
            print(target_date)
        else:
            sys.exit(f"Some arguments are missing. Date format is: {p_default_format}")
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
        if len(sys.argv) > 2:
            target_var = sys.argv[2]
        else:
            sys.exit(f"Some arguments are missing.")
    return target_var


def get_files_by_keystring_in_fn(p_root_dir, p_ds_type, p_var_fn_mapped, p_key_date_string):
    """
    Searches for files in the root directory that contain the key string in the file name.

    Parameters
    ----------
    p_root_dir :                str
                                Root directory to search for files.
    p_ds_type :                 str
                                Dataset type (c for CMEMS, m for MITgcm).
    p_var_fn_mapped :           str
                                Mapped variable name as per the config file.
    p_key_date_string :         str
                                Key string to search for in the file name.
    
    Returns
    -------
    matches :                   list
                                List of files that contain the key string in the file name.
    """

    root_path = Path(p_root_dir)
    year_pattern = re.compile(r"^\d{4}$")
    skip_subdir = True
    if p_ds_type == "c":
        pattern = re.compile(fr"^[^\d]{{5}}_{p_var_fn_mapped}-.*_{p_key_date_string}[^()]*\.nc$")
    elif p_ds_type == "m":
        skip_subdir = False
        pattern = re.compile(fr"^{p_key_date_string}\d{{2}}_.*--{p_var_fn_mapped}[^()]*\.nc$")
    #matches = [item for item in root_path.rglob("*") if pattern.match(item.name)]

    matches = []
    for item in root_path.rglob("*"):
        if skip_subdir:
            if pattern.match(item.name):
                matches.append(item)
        else:
            # Check if the item is a directory and its name corresponds to 4 digits (year). This serves the purpose of discarding data contained in backup or other directories. 
            if (item.is_dir and year_pattern.match(item.name)):  
                for subitem in item.rglob("*"):
                    if pattern.match(subitem.name):
                        matches.append(subitem)
    return matches