# David Omrai
# 28.11.2022
# This script runs and collects the data
# of both probsat and gsat algorithm
# 
# It sets the MAX_FLIPS parameter and 
# each instance runs for 500 times
# 
# There will be 1000 instances for each uf
# for uf75 only 100 instances
# 
# All used instances are stored in the data folder

# Data location
data_loc="./data/final_data"

# Create new output file
mkdir results 2> /dev/null
out_name="./results/fdata_res"

# Number of repeats
repeats_num=500

par_loop_probsat() {
  ins_name=$(basename $1)
  for INSTANCE in $1/*; do
    for i in $(seq 1 $repeats_num); do
      ./probsat.py -i $INSTANCE -f 1600 2>> "${out_name}_${ins_name}_probsat.log" > /dev/null
    done
  done
}

par_loop_gsat() {
    ins_name=$(basename $1)
    for INSTANCE in $1/*; do
      for i in $(seq 1 $repeats_num); do
        ./gsat2 -r time $INSTANCE -i 1600 2>> "${out_name}_${ins_name}_gsat2.log" > /dev/null
      done
    done
}

# loop function to get paralized

for SET in $data_loc/*; do 
    par_loop_probsat $SET &
    par_loop_gsat $SET &
done


