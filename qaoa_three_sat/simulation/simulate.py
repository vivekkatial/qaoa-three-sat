""" Simulation script



Author: Vivek Katial
"""

from math import pi
import argparse
import yaml
import json

# Import Custom Modules
from qaoa_three_sat.instance.three_sat import QAOAInstance3SAT
from qaoa_three_sat.utils.qc_helpers import load_raw_instance, clean_instance
from qaoa_three_sat.rotation.rotations import Rotations


def simulate_circuit(
    instance_filename,
    classical_opt_alg,
    optimisation_opts,
    alpha_trial,
    beta_trial,
    n_rounds,
    track_optimiser,
    disp=False,
    mlflow=False,
):
    """This function simulates an instance of 3SAT on QAOA

    :param instance_filename: Instance filename
    :type instance_filename: str
    :param classical_opt_alg: Name of Classical Optmisation Algorithm
    :type classical_opt_alg: str
    :param optimisation_opts: Optimisation Algorithm Parameters
    :type optimisation_opts: dict
    :param alpha_trial: Initial Guess for alpha
    :type alpha_trial: list
    :param beta_trial: Initial Guess for beta
    :type beta_trial: list
    :param n_rounds: Number of rounds to build QAOA Circuit
    :type n_rounds: int
    :param track_optimiser: Set True, to track classical optimisation metrics on Instance object
    :type track_optimiser: bool
    :param disp: Set True, to display classical optimisation steps for algorithm and print circuit, defaults to False
    :type disp: bool, optional
    :param mlflow: Set True, to track results on an MLFlow server, defaults to False
    :type disp: bool, optional
    :returns: Instance Object
    :rtype: {qaoa_three_sat.QAOAInstance3SAT}
    """

    # Load instance into environment
    instance_file = "data/raw/%s.json" % instance_filename
    raw_instance = load_raw_instance(instance_file)

    # Construct rotation objects
    (
        n_qubits,
        single_rotations,
        double_rotations,
        triple_rotations,
        sat_assgn,
    ) = clean_instance(raw_instance)

    single_rotations = Rotations(single_rotations, n_qubits)
    double_rotations = Rotations(double_rotations, n_qubits)
    triple_rotations = Rotations(triple_rotations, n_qubits)

    # Initatiate Instance Class for problem
    instance = QAOAInstance3SAT(
        n_qubits=n_qubits,
        single_rotations=single_rotations,
        double_rotations=double_rotations,
        triple_rotations=triple_rotations,
        alpha=alpha_trial,
        beta=beta_trial,
        n_rounds=n_rounds,
        classical_opt_alg=classical_opt_alg,
        optimiser_opts=optimisation_opts,
        track_optimiser=track_optimiser,
        sat_assgn=sat_assgn,
        disp=disp,
        mlflow=mlflow,
    )

    instance.build_circuit()

    # Print the circuit being experimented on
    if disp:
        print(instance.quantum_circuit)
    # Kick-off run
    if disp:
        print(
            "Circuit Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
            % (instance.classical_iter, instance.alpha, instance.beta, instance.energy)
        )

    # Optimise
    instance.optimise_circuit()

    return instance


if __name__ == "__main__":
    """ Example run for a simulation """

    # Parsing arguments from CLI
    parser = argparse.ArgumentParser()
    # Adding command line argument
    parser.add_argument(
        "-i", "--instance", type=str, help="Name of the instance file being produced"
    )
    parser.add_argument(
        "-p", "--params_file", type=str, help="Parameter file for QAOA run"
    )
    # Parse your arguments
    args = parser.parse_args()
    run_path = "params/ready/" + args.params_file
    instance_filename = args.instance

    print("\nReading yaml file\n")
    with open(run_path) as file:
        params = yaml.load(file, Loader=yaml.FullLoader)

    # Optimisation parameters
    opt_params = params["classical_optimisation"]

    # Parse params
    classical_opt_alg = opt_params["classical_opt_alg"]
    optimisation_opts = eval(opt_params["optimisation_opts"])
    alpha_trial = json.loads(opt_params["alpha_trial"])
    beta_trial = json.loads(opt_params["beta_trial"])
    n_rounds = int(opt_params["n_rounds"])
    track_optimiser = True

    simulate_circuit(
        instance_filename=instance_filename,
        classical_opt_alg=classical_opt_alg,
        optimisation_opts=optimisation_opts,
        alpha_trial=alpha_trial,
        beta_trial=beta_trial,
        n_rounds=n_rounds,
        track_optimiser=track_optimiser,
        disp=True,
    )
