#!/bin/bash

set -e

classical_opt_dir=params/ready
instance_dir=data/raw

for inst in $instance_dir/*
do
    for classical in $classical_opt_dir/*
    do
      local_run_path=$classical
    #  echo $local_run_path
      echo -e "Submitting job: \n Instance: \t $inst \n Run File: \t $local_run_path"

      # Define run_file and log_file
      classical_prefix="params/ready/"
      instance_prefix="instance_dir"
      export log_file=logs/${local_run_path#"$classical_prefix"}_${inst#"$instance_prefix"}.log

      echo -e "Logging results: \t $log_file"

      # Identify number of qubits
      # N_QUBITS=$(echo $local_run_path | grep -oP '(?<=n_qubits)[0-9]+')

      NodeMemory=10GB
      echo "Allocating node $NodeMemory memory for experiment $local_run_path"

      # Run experiment as an instance of the singularity container
      # sbatch --mem $NodeMemory --output=$log_file bin/run-experiments.slurm $local_run_path
    done
done