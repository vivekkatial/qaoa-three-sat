#!/bin/bash

set -e

classical_opt_dir=params/ready
instance_dir=data/raw

for inst in $instance_dir/*
do
    for classical in $classical_opt_dir/*
    do
      local_run_path=$classical
      echo -e "Submitting job: \n Instance: \t $inst \n Run File: \t $classical"

      # Define run_file and log_file
      classical_prefix="params/ready/"
      classical_no_prefix=${classical#"$classical_prefix"}
      
      inst_file=$(awk -F/ '{split($NF,temp,"."); print temp[1]}' <<<"$inst")
      printf "%s\n" "$inst_file"

      # Identify number of qubits
      # N_QUBITS=$(echo $local_run_path | grep -oP '(?<=n_qubits)[0-9]+')
      echo "Allocating node $NodeMemory memory for experiment $classical"

      exp_run_params="$inst_file:$classical_no_prefix:True"
      log_file="logs/$exp_run_params.log"
      # Run experiment as an instance of the singularity container
      echo $exp_run_params
      INSTANCE_FILENAME=$inst_file
      PARAMETER_FILE_FOR_QAOA=$classical_no_prefix
      MLFLOW_TRACKING="True"
      python run/main_qaoa.py --instance=$INSTANCE_FILENAME --params_file=$PARAMETER_FILE_FOR_QAOA --track_mlflow=$MLFLOW_TRACKING || True
    done
done