#!/bin/bash

# ./get_gg_cmems_obs.sh "2024-04-01" "2024-04-02"
dstart=$1
dend=$2

giorno=$dstart

$HOME/SPITBRAN/scripts/get_cmems_obs.sh $giorno

while [[ $giorno<=$dend ]]; do
  giorno=$(date -d "$giorno +1 day" +"%Y-%m-%d")
  echo $giorno
  $HOME/SPITBRAN/scripts/get_cmems_obs.sh $giorno
done

