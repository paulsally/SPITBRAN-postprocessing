import sys
from pathlib import Path
import copernicusmarine

# Check if python script is running in interactive mode
if getattr(sys, "ps1", None) is None:
    if len(sys.argv) == 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    else:
        exit("Missing arguments (start date, end date or both)")
else:
    start_date = input("Enter the start date in format YYYY-MM-DD")
    end_date = input("Enter the end date in format YYYY-MM-DD")

data_dir = rf"{Path(__file__).parent.parent}/DATA/CMEMS"

copernicusmarine.subset(
    dataset_id="med-cmcc-tem-rean-d",
    variables=["thetao"],
    minimum_longitude=6.066406,
    maximum_longitude=12.12891,
    minimum_latitude=41.88515,
    maximum_latitude=44.50234,
    start_datetime=f"{start_date}T00:00:00",
    end_datetime=f"{end_date}T23:00:00",
    minimum_depth=1.0182366371154785,
    maximum_depth=1.0182366371154785,
    output_directory=data_dir,
)