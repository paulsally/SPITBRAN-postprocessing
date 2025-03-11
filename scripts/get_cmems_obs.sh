#!/bin/bash
# ./get_cmems.sh "2024-01-01"

#module load python3/3.11.8-01

data=$1
echo "data: "$data

# lonmin=-1.0
lonmin=6.083333
# lonmax=16.50
lonmax=12.16667
# latmin=36.0
latmin=41.89583
# latmax=45.0
# latmax=44.52083
latmax=44.53
depthmin=0
depthmax=2841.841

# dir_file=$SCRATCH"/cmems_data/phy/"
dir_file=$HOME"/SPITBRAN/DATA/CMEMS/obs/TEST"

day=$(date -d "$data" +"%Y-%m-%dT00:00:00")
dd=$(date -d "$data" +"%Y%m%d")

dataset="cmems_SST_MED_SST_L4_REP_OBSERVATIONS_010_021"
file=$dir_file"cmems_sst-l4_rep_obs_"$dd".nc"

rm $file

# temperature
yes | 
copernicusmarine subset \
    --dataset-id $dataset \
    --dataset-version 202411 \
    --variable analysed_sst \
    --variable analysis_error \
    --variable mask \
    --variable sea_ice_fraction \
    --start-datetime $day \
    --end-datetime $day \
    --minimum-longitude $lonmin \
    --maximum-longitude $lonmax \
    --minimum-latitude $latmin \
    --maximum-latitude $latmax \
    --minimum-depth $depthmin \
    --maximum-depth $depthmax \
    --coordinates-selection-method strict-inside \
    --log-level ERROR \
    -o $dir_file \
