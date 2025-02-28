#!/bin/bash

# Script Name: get_gg_cmems.sh
# Author: Maria Fattorini
# Date: 2024-05-08
# Description: 
#     This script retrieves data from the CMEMS dataset for a given date range.
# Usage:
#     ./get_gg_cmems.sh "YYYY-MM-DD" "YYYY-MM-DD"
# Notes:
#     - Ensure you have the necessary input data and permissions.
#     - Modify dir_file to change the data storage path.

# Example:
# To retrieve data for a specific date range, run the following command:
# ./get_gg_cmems.sh "2024-01-01" "2024-01-02"

#module load python3/3.11.8-01

dstart=$1
dend=$2

giorno=$dstart

$HOME/SPITBRAN/scripts/get_cmems.sh $giorno

while [[ $giorno<=$dend ]]; do
  giorno=$(date -d "$giorno +1 day" +"%Y-%m-%d")
  echo $giorno
  $HOME/SPITBRAN/scripts/get_cmems.sh $giorno
done

