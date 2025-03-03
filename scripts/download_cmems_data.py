import sys
from pathlib import Path
import copernicusmarine
from datetime import datetime

# Check if python script is running in interactive mode
if getattr(sys, "ps1", None) is None:
    if len(sys.argv) == 3:
        start_date_str = sys.argv[1]
        end_date_str = sys.argv[2]
    else:
        exit("Missing arguments (start date, end date or both)")
else:
    start_date_str = input("Enter the start date in format YYYYMMDD")
    end_date_str = input("Enter the end date in format YYYYMMDD")

start_date = datetime.strptime(start_date_str, "%Y%m%d")
end_date = datetime.strptime(end_date_str, "%Y%m%d")

data_dir = rf"{Path(__file__).parent.parent}/DATA/CMEMS/TEST/TO-FROM"

copernicusmarine.subset(
    dataset_id="med-cmcc-tem-rean-d",
    # variables=["thetao"],
    minimum_longitude=6.083333,
    maximum_longitude=12.16667,
    minimum_latitude=41.89583,
    maximum_latitude=44.53,
    start_datetime=f"{start_date}T00:00:00",
    end_datetime=f"{end_date}T23:00:00",
    # minimum_depth=1.0182366371154785,
    # maximum_depth=1.0182366371154785,
    output_directory=data_dir,
    output_filename=f"cmems_tem-rean_d_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.nc",
)