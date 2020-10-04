"""Sample simulation script

Author: Vivek Katial
"""

from math import pi
from instance import QAOAInstance3SAT
from qc_helpers import load_raw_instance, clean_instance
from rotations import Rotations
from scipy.optimize import minimize
import numpy as np
import pandas as pd


def main():
    """ Simulate Function"""

    # Sample Instance
    instance_file = "data/raw/sample_instance-usa.json"

    # Instance File
    optimisation_opts = {
        "xtol": 0.001,
        "disp": True,
        "adaptive": True,
        "simplex_area_param": 0.1,
    }

    # Load instance into environment
    raw_instance = load_raw_instance(instance_file)

    # Construct rotation objects
    n_qubits, single_rotations, double_rotations, triple_rotations = clean_instance(
        raw_instance
    )

    single_rotations = Rotations(single_rotations, n_qubits)
    double_rotations = Rotations(double_rotations, n_qubits)
    triple_rotations = Rotations(triple_rotations, n_qubits)

    # Create a grid of alpha and beta
    alphas = np.arange(start=-pi, stop=pi, step=0.1)
    betas = np.arange(start=-pi, stop=pi, step=0.1)

    energy_ls = []
    iteration = 1

    for alp in alphas:
        for bet in betas:

            # Initatiate Instance Class for problem
            instance = QAOAInstance3SAT(
                n_qubits=n_qubits,
                single_rotations=single_rotations,
                double_rotations=double_rotations,
                triple_rotations=triple_rotations,
                alpha=[alp],
                beta=[bet],
                n_rounds = 1,
                classical_opt_alg="nelder-mead",
                optimiser_opts=optimisation_opts
            )

            # Build Quantum Circuit
            instance.initiate_circuit()
            instance.add_single_rotations()
            instance.add_double_rotations()
            instance.add_triple_rotations()
            instance.close_round()
            iteration += 1

            # Print the circuit being experimented on
            # print(instance.quantum_circuit)
            instance.simulate_circuit()
            instance.measure_energy()
            # Kick-off run
            print(
                "Landscape Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
                % (iteration, instance.alpha[0], instance.beta[0], instance.energy)
            )
            sim_dict = {"alpha": alp, "beta": bet, "energy": instance.energy}
            energy_ls.append(sim_dict)

        # Run Optimisation
        # energy_0 = instance.energy

    df = pd.DataFrame(energy_ls)
    df.to_csv("data/sim_sample_usa.csv")

if __name__ == "__main__":
    main()
