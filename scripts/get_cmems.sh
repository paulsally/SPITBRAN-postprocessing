#!/bin/bash
# ./get_cmems.sh "2024-01-01"

#module load python3/3.11.8-01

data=$1
echo 'data: '$data

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

# dir_file=$SCRATCH'/cmems_data/phy/'
dir_file=$HOME'/SPITBRAN/DATA/CMEMS/rean-d/'


day=$(date -d "$data" +"%Y-%m-%dT00:00:00")
dd=$(date -d "$data" +"%Y%m%d")

# dataset_cur='cmems_mod_med_phy-cur_anfc_4.2km_P1D-m'
dataset_cur='med-cmcc-cur-rean-d'
cur_file=$dir_file'cmems_cur-rean_d_'$dd'.nc'
# dataset_tem='cmems_mod_med_phy-tem_anfc_4.2km_P1D-m'
dataset_tem='med-cmcc-tem-rean-d'
tem_file=$dir_file'cmems_tem-rean_d_'$dd'.nc'
# dataset_sal='cmems_mod_med_phy-sal_anfc_4.2km_P1D-m'
dataset_sal='med-cmcc-sal-rean-d'
sal_file=$dir_file'cmems_sal-rean_d_'$dd'.nc'
# dataset_ssh='cmems_mod_med_phy-ssh_anfc_4.2km_P1D-m'
dataset_ssh='med-cmcc-ssh-rean-d'
ssh_file=$dir_file'cmems_ssh-rean_d_'$dd'.nc'

rm $cur_file
rm $tem_file
rm $sal_file
rm $ssh_file

# currents
yes | copernicusmarine subset --dataset-id $dataset_cur --dataset-version 202012 --variable uo --variable vo --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $cur_file

# temperature
yes | copernicusmarine subset --dataset-id $dataset_tem --dataset-version 202012 --variable thetao --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $tem_file

# salinity
yes | copernicusmarine subset --dataset-id $dataset_sal --dataset-version 202012 --variable so --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax --minimum-depth $depthmin --maximum-depth $depthmax -o $dir_file -f $sal_file

# ssh
yes | copernicusmarine subset --dataset-id $dataset_ssh --dataset-version 202012 --variable zos --start-datetime $day --end-datetime $day --minimum-longitude $lonmin --maximum-longitude $lonmax --minimum-latitude $latmin --maximum-latitude $latmax -o $dir_file -f $ssh_file

