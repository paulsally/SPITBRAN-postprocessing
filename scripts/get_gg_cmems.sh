#!/bin/bash

# ./get_gg_cmems.sh "2024-04-01" "2024-04-02"
dstart=$1
dend=$2

giorno=$dstart

$HOME/cmems/get_cmems.sh $giorno

while [[ $giorno<=$dend ]]; do
  giorno=$(date -d "$giorno +1 day" +"%Y-%m-%d")
  echo $giorno
  $HOME/SPITBRAN/scripts/get_cmems.sh $giorno
done

