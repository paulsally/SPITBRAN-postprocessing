#!/bin/bash
# ./get_cmems.sh "2024-01-01"

#module load python3/3.11.8-01

data=$1
echo 'data: '$data

lonmin=-1.0
lonmax=16.50
latmin=36.0
latmax=45.0
depthmin=0
depthmax=3650.0

# dir_file=$SCRATCH'/cmems_data/phy/'
dir_file=$HOME'/SPITBRAN/DATA/CMEMS/rean_d/'


day=$(date -d "$data" +"%Y-%m-%dT00:00:00")
dd=$(date -d "$data" +"%Y%m%d")

dataset_cur='cmems_mod_med_phy-cur_anfc_4.2km_P1D-m'
cur_file=$dir_file'cmems_cur-rean_d_'$dd'.nc'
dataset_tem='cmems_mod_med_phy-tem_anfc_4.2km_P1D-m'
tem_file=$dir_file'cmems_tem-rean_d_'$dd'.nc'
dataset_sal='cmems_mod_med_phy-sal_anfc_4.2km_P1D-m'
sal_file=$dir_file'cmems_sal-rean_d_'$dd'.nc'
dataset_ssh='cmems_mod_med_phy-ssh_anfc_4.2km_P1D-m'
ssh_file=$dir_file'cmems_ssh-rean_d_'$dd'.nc'

rm $cur_file
rm $tem_file
rm $sal_file
rm $ssh_file

copernicusmarine login

# currents
yes | copernicusmarine subset --dataset-id $dataset_cur --dataset-version 202411 --variable uo --variable vo --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $cur_file

# temperature
yes | copernicusmarine subset --dataset-id $dataset_tem --dataset-version 202411 --variable thetao --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $tem_file

# salinity
yes | copernicusmarine subset --dataset-id $dataset_sal --dataset-version 202411 --variable so --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $sal_file

# ssh
yes | copernicusmarine subset --dataset-id $dataset_ssh --dataset-version 202411 --variable zos --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax -o $dir_file -f $ssh_file

