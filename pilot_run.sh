# David Omrai
# 28.11.2022
# This script runs and collects the data
# of both probsat and gsat algorithm
# 
# It sets the MAX_FLIPS parameter and 
# each instance runs for 100 times
# 
# There will be 100 instances for each uf
# 
# All used instances are stored in the data folder

# Data location
data_loc="./data/pilot_data"

# Create new output file
mkdir results 2> /dev/null
out_name="./results/pdata_res_$(date +"%Y_%m_%d_%I_%M")"

# Change the number of flips
flips_nums=("400" "800" "1600")

# Number of repeats
repeats_num=100

# loop function to get paralized
par_loop_probsat() {
  for SET in $data_loc/*; do 
    for INSTANCE in $SET/*; do
      for i in $(seq 1 $repeats_num); do
        ./probsat.py -i $INSTANCE -f $1 2>> "${out_name}_${1}_probsat.log" > /dev/null
      done
    done
  done
}

par_loop_gsat() {
  for SET in $data_loc/*; do 
    for INSTANCE in $SET/*; do
      for i in $(seq 1 $repeats_num); do
        ./gsat2 -r time $INSTANCE -i $1 2>> "${out_name}_${1}_gsat2.log" > /dev/null
      done
    done
  done
}

# loop throught each set
for flips_num in ${flips_nums[@]}; do 
  par_loop_probsat $flips_num  &
  par_loop_gsat $flips_num &
done
