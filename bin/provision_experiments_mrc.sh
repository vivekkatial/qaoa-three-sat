#!/bin/bash
export CLUSTER_URI="/home/ubuntu/qaoa-three-sat"
export HOST_NAME="ubuntu@115.146.92.101"
export RELATIVE_RUN_PATH="/params/ready"
export RELATIVE_INST_PATH="/data/raw"
export VM_PEM_FILE_PATH="~/.ssh/mlflow-experimentr-vm.pem"

echo "Moving experiment files to MRC VM"

dir=params/ready
for f in $dir/*
do
  local_run_path=$f
  echo "SCP file: $local_run_path to $HOST_NAME"
  scp -i $VM_PEM_FILE_PATH $local_run_path $HOST_NAME:$CLUSTER_URI$RELATIVE_RUN_PATH
done


inst_dir=data/raw
for f in $inst_dir/*
do
  local_run_path=$f
  echo $local_run_path
    scp -i $VM_PEM_FILE_PATH $local_run_path $HOST_NAME:$CLUSTER_URI$RELATIVE_INST_PATH
done