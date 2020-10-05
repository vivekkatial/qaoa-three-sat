"""Sample simulation script

Author: Vivek Katial
"""

from math import pi
from instance import QAOAInstance3SAT
from qc_helpers import load_raw_instance, clean_instance
from rotations import Rotations
from scipy.optimize import minimize
import numpy as np


def main():
    """ Simulate Function"""

    # Sample Instance
    instance_file = "data/raw/sample_instance.json"

    # Load instance into environment
    raw_instance = load_raw_instance(instance_file)

    # Construct rotation objects
    n_qubits, single_rotations, double_rotations, triple_rotations = clean_instance(
        raw_instance
    )

    single_rotations = Rotations(single_rotations, n_qubits)
    double_rotations = Rotations(double_rotations, n_qubits)
    triple_rotations = Rotations(triple_rotations, n_qubits)

    # Classical Optimisation Parameters
    optimisation_opts = {
        "classical_opt_alg": "nelder-mead",
        "xtol": 0.001,
        "disp": True,
        "adaptive": True,
        "simplex_area_param": 0.1
    }

    # Initatiate Instance Class for problem
    instance = QAOAInstance3SAT(
        n_qubits=n_qubits,
        single_rotations=single_rotations,
        double_rotations=double_rotations,
        triple_rotations=triple_rotations,
        alpha=[0, 0],
        beta=[0, 0],
        n_rounds=2,
        classical_opt_alg="nelder-mead",
        optimiser_opts=optimisation_opts,
    )

    
    #instance.build_circuit()

    # Print the circuit being experimented on
    # print(instance.quantum_circuit)
    # # Kick-off run
    # print(
    #     "Circuit Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
    #     % (instance.classical_iter, instance.alpha[0], instance.beta[0], instance.energy)
    # )

    # # Run Optimisation
    # energy_0 = instance.energy
    # # Initial Iteration
    # instance.optimise_circuit()


if __name__ == "__main__":
    main()
