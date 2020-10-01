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

    # Initatiate Instance Class for problem
    instance = QAOAInstance3SAT(
        n_qubits=n_qubits,
        single_rotations=single_rotations,
        double_rotations=double_rotations,
        triple_rotations=triple_rotations,
        alpha=[-1.5],
        beta=[-0.6],
        simplex_area_param=0.01,
    )

    # Build Quantum Circuit
    instance.initiate_circuit()
    instance.add_single_rotations()
    instance.add_double_rotations()
    instance.add_triple_rotations()
    instance.close_round()

    # Print the circuit being experimented on
    print(instance.quantum_circuit)
    # Kick-off run
    print(
        "Circuit Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
        % (instance.iter, instance.alpha[0], instance.beta[0], instance.energy)
    )

    # Run Optimisation
    energy_0 = instance.energy
    # Initial Iteration
    instance.optimise_circuit()


if __name__ == "__main__":
    main()
