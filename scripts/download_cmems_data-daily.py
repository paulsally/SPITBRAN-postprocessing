import sys
from pathlib import Path
import copernicusmarine
from datetime import datetime, timedelta

# Problem with this method is there I couldn't find a way to overwrite filenames of downloaded files
# Check if python script is running in interactive mode
if getattr(sys, "ps1", None) is None:
    if len(sys.argv) == 3:
        start_date_str = sys.argv[1]
        end_date_str = sys.argv[2]
    else:
        exit("Missing arguments (start date, end date or both)")
else:
    start_date_str = input("Enter the start date in format YYYYMMDD") or "20130401"
    end_date_str = input("Enter the end date in format YYYYMMDD") or "20130403"

data_dir = rf"{Path(__file__).parent.parent}/DATA/CMEMS/TEST"

# Define start and end dates
start_date = datetime.strptime(start_date_str, "%Y%m%d")
end_date = datetime.strptime(end_date_str, "%Y%m%d")
# end_date = datetime.strptime("20230110", "%Y%m%d")
# Initialize the looping variable
current_date = start_date
step = timedelta(days=1)

# files = ["bio", "cur", "nut", "pft", "sal", "ssh", "tem"]
files = ["cur", "sal", "ssh", "tem"]
# files = ["ssh", "tem"]

while start_date <= current_date <= end_date:
    for var_fn in files:
        copernicusmarine.subset(
            dataset_id=f"med-cmcc-{var_fn}-rean-d",
            # variables=["thetao"],
            minimum_longitude=6.083333,
            maximum_longitude=12.16667,
            minimum_latitude=41.89583,
            maximum_latitude=44.53,
            start_datetime=f"{current_date}T00:00:00",
            end_datetime=f"{current_date}T23:00:00",
            # minimum_depth=1.0182366371154785,
            # maximum_depth=1.0182366371154785,
            output_directory=data_dir,
            output_filename=f"cmems_{var_fn}-rean_d_{current_date.strftime('%Y%m%d')}.nc",
        )
    current_date += step