#!/bin/bash
# Usage: ./get_cmems_insitu.sh mediterrane 2012/* (to download all data referring to Geographical Area Mediterranean Sea and Temporal Extent year 2012)
# If requesting a temporal extent that is smaller than a year input an expression similar to the following: 2012/*20120101* (for day 20120101)

#module load python3/3.11.8-01

# dir_file=$SCRATCH"/cmems_data/phy/"
dir_file=$HOME"/SPITBRAN/DATA/CMEMS/insitu/"

# dataset="cmems_obs-ins_glo_phy-temp-sal_my_cora_irr"
dataset="cmems_obs-ins_glo_phy-temp-sal_my_easycora_irr"
geoarea=$1
temporal_extent=$2

echo "Geographical Area: "$1" - Temporal Extension: "$2
# file=$dir_file"cmems_tem-l4_rep_obs_"$dd".nc"

# Download:
#   - Geographical area: Mediterranean Sea
#   - Temporal Extent: 2012
yes | 
copernicusmarine get \
    --dataset-id $dataset \
    --dataset-version 202411 \
    --filter "*"$geoarea"/"$temporal_extent \
    --log-level ERROR \
    -o $dir_file \
    # -f $file
