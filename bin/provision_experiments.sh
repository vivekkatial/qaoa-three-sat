#!/bin/bash
export CLUSTER_URI=/data/gpfs/projects/punim1074/qaoa-three-sat
export HOST_NAME=vivekkatial@spartan.hpc.unimelb.edu.au
export RELATIVE_RUN_PATH=/params/ready
export RELATIVE_INST_PATH=/data/raw

echo "Moving run file to SPARTAN"
#local_run_path="params/ready/t_step0.100000__time_T10__instance_index100.000000__n_qubits9.000000__graph_typeunique_soln.yml"
#local_run_path="_main_.py"
#scp $local_run_path $HOST_NAME:$CLUSTER_URI$RELATIVE_RUN_PATH
#scp $local_run_path $HOST_NAME:$CLUSTER_URI

dir=params/ready
for f in $dir/*
do
  local_run_path=$f
  echo $local_run_path
  scp $local_run_path $HOST_NAME:$CLUSTER_URI$RELATIVE_RUN_PATH
done


inst_dir=data/raw
for f in $inst_dir/*
do
  local_run_path=$f
  echo $local_run_path
  scp $local_run_path $HOST_NAME:$CLUSTER_URI$RELATIVE_INST_PATH
done