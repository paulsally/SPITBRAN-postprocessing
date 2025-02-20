import sys
from pathlib import Path
import re
from IPython import get_ipython

def get_cwd():
    """
    Gets the value of the Current Working Directory according to whether the script is run interactively or via command line

    Parameters
    ----------
    None

    Returns
    -------
    cwd:                        Path
                                Current Working Directory for script

    """
    # if hasattr(sys, "ps1"):
    #     cwd = Path.cwd() # interactive window
    # else:
    #     cwd = str(Path(__file__).resolve().parent.parent) # command line
    # # Add the script parent directory to sys.path to allow importing lib in command line execution mode
    # if str(cwd) not in sys.path:
    #     sys.path.append(str(cwd))
    try:
        get_ipython()  # Jupyter or IPython environment
        cwd = Path.cwd()  # interactive window
    except NameError:
        cwd = str(Path(__file__).resolve().parent.parent)  # command line
    return cwd


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


def get_files_by_keystring_in_fn(p_ds_type, p_root_dir, p_var_fn_mapped, p_key_date_string):
    """
    Searches for files in the root directory that contain the key string in the file name.

    Parameters
    ----------
    p_ds_type :                 str
                                Dataset type (c for CMEMS, m for MITgcm).
    p_root_dir :                Path
                                Root directory to search for files.    
    p_var_fn_mapped :           str
                                Mapped variable name as per the config file.
    p_key_date_string :         str
                                Date string to search for in the file name.
    
    Returns
    -------
    matches :                   list
                                List of files that contain the key string in the file name.
    """
    root_path = Path(p_root_dir).expanduser().resolve()
    # year_pattern = re.compile(r"^\d{4}$")
    if p_ds_type == "c-rean":
        # Test for file name 
        #   starting with 5 characters (cmems) excluding digits
        #   containing the target variable name
        pattern = re.compile(fr"^[^\d]{{5}}_{p_var_fn_mapped}-.*_{p_key_date_string}[^()]*\.nc$")
        # print(pattern)
    elif p_ds_type == "m":
        # Test for file name 
        #   starting with 6 digits which is the target date and may be 4 or 6 digits long
        #   containing the target variable name
        if len(p_key_date_string) == 6:
            pattern = re.compile(fr"^{p_key_date_string}\d{{2}}_.*--{p_var_fn_mapped}-[^()]*\.nc$")
        elif len(p_key_date_string) == 8:
            pattern = re.compile(fr"^{p_key_date_string}_.*--{p_var_fn_mapped}-[^()]*\.nc$")
        else:
            raise ValueError("Invalid date")
        # pattern = re.compile(fr"^{p_key_date_string}\d{{2}}|{p_key_date_string}\d{{0}}_.*--{p_var_fn_mapped}-[^()]*\.nc$")
        # print(pattern)
    else:
        raise ValueError("Invalid dataset type")

    # Check if key string is found in the file name and the filename is inside a directory corresponding to a year (i.e. all directories that contains other than 4 digits are discarded)
    matches = [
        item
        for item in root_path.rglob("*")
            if item.is_file() and pattern.match(item.name)
    ]
    # matches = [
    #     subitem
    #     for item in root_path.rglob("*")
    #         if item.is_dir() and year_pattern.match(item.name)
    #         # if item.is_dir()
    #             for subitem in item.rglob("*")
    #                 if subitem.is_file() and pattern.match(subitem.name)
    # ]
    # Loop through all items recursively in root_path
    # matches = []
    # for item in root_path.rglob("*"):
    #     # Check if the item is a directory and its name matches the year pattern
    #     # if item.is_dir() and year_pattern.match(item.name):
    #     if item.is_dir() and year_pattern.match(item.name):
    #         # Loop through all items in the matching directory
    #         for subitem in item.rglob("*"):
    #             # Check if the subitem's name matches the given pattern
    #             if subitem.is_file() and pattern.match(subitem.name):
    #                 # Add the matching subitem to the matches list
    #                 matches.append(subitem)
    #                 print(subitem)
    # print(f"matches: {sorted(matches)}")

    return sorted(matches)