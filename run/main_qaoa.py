"""Script to simulate QAOA circuit and track results on MLFlow

This script is a default run script for running an experiment of QAOA

Author: Vivek Katial
"""

from math import pi
from os import path
import argparse
import yaml
import json
import mlflow

from qaoa_three_sat.simulation.simulate import simulate_circuit
from qaoa_three_sat.utils.exp_utils import str2bool, make_temp_directory
from qaoa_three_sat.utils.qc_helpers import *



if __name__ == "__main__":

    # Parsing arguments from CLI
    parser = argparse.ArgumentParser()
    # Adding command line argument
    parser.add_argument(
        "-i", "--instance", type=str, help="Name of the instance file being produced"
    )
    parser.add_argument(
        "-p", "--params_file", type=str, help="Parameter file for QAOA run"
    )
    parser.add_argument(
        "-T",
        "--track_mlflow",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="Activate MlFlow Tracking.",
    )
    # Parse your arguments
    args = parser.parse_args()
    run_path = path.join("params", "ready", args.params_file)
    instance_filename = args.instance
    mlflow_tracking = args.track_mlflow

    # Read in parameter file
    with open(run_path) as file:
        params = json.load(file)

    # MlFlow Configuration
    if mlflow_tracking:
        mlflow.set_tracking_uri(params["experiment"]["tracking-uri"])
        mlflow.set_experiment(params["experiment"]["name"])

    # Optimisation parameters
    opt_params = params["classical_optimisation"]

    # Parse params
    classical_opt_alg = opt_params["classical_opt_alg"]
    optimisation_opts = eval(opt_params["optimisation_opts"])
    alpha_trial = json.loads(opt_params["alpha_trial"])
    beta_trial = json.loads(opt_params["beta_trial"])
    n_rounds = int(opt_params["n_rounds"])
    track_optimiser = True

    if mlflow_tracking:
        # Log initial angle
        mlflow.log_param("alpha_init", alpha_trial)
        mlflow.log_param("beta_init", beta_trial)

    instance = simulate_circuit(
        instance_filename=instance_filename,
        classical_opt_alg=classical_opt_alg,
        optimisation_opts=optimisation_opts,
        alpha_trial=alpha_trial,
        beta_trial=beta_trial,
        n_rounds=n_rounds,
        track_optimiser=track_optimiser,
        mlflow=mlflow_tracking,
        disp=True,
    )

    instance.calculate_pdf()

    # Log parameters and metrics
    if mlflow_tracking:
        mlflow.log_param("instance", args.instance)
        mlflow.log_param("params_file", args.params_file)
        mlflow.log_param("n_qubits", instance.n_qubits)
        mlflow.log_param("budget", optimisation_opts["budget"])
        mlflow.log_param("alpha_final", instance.alpha)
        mlflow.log_param("beta_final", instance.beta)
        mlflow.log_metric("energy", instance.energy)
        mlflow.log_metric("classical_iter", instance.classical_iter)
        mlflow.log_metric(
            "p_success",
            calculate_p_success(instance.pdf, instance.n_qubits, instance.sat_assgn),
        )

    # Build artifacts in a tmp directory
    with make_temp_directory() as temp_dir:
        # Write circuit to file and save
        circuit_path = path.join(temp_dir, "qc.png")
        instance.quantum_circuit.draw("mpl", filename=circuit_path)
        if mlflow_tracking:
            mlflow.log_artifact(circuit_path)
            mlflow.log_artifact(run_path)
