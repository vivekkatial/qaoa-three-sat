"""Sample simulation script

Author: Vivek Katial
"""

from math import pi

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
):
    """ Simulate Function"""

    # Load instance into environment
    instance_file = "data/raw/%s.json" % instance_filename
    raw_instance = load_raw_instance(instance_file)

    # Construct rotation objects
    n_qubits, single_rotations, double_rotations, triple_rotations = clean_instance(
        raw_instance
    )

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
        disp=disp,
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

    instance_filename = "sample_instance"
    # Classical Optimisation Parameters
    optimisation_opts = {
        "classical_opt_alg": "nelder-mead",
        "xtol": 0.001,
        "disp": True,
        "adaptive": True,
        "simplex_area_param": 0.1,
    }

    classical_opt_alg = "nelder-mead"

    alpha_trial = [0]
    beta_trial = [1]
    n_rounds = 1
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
