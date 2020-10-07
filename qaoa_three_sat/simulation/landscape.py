"""Sample simulation script

Author: Vivek Katial
"""

from math import pi

from scipy.optimize import minimize
import numpy as np
import pandas as pd

# Import Custom Modules
from qaoa_three_sat.instance.three_sat import QAOAInstance3SAT
from qaoa_three_sat.utils.qc_helpers import load_raw_instance, clean_instance
from qaoa_three_sat.rotation.rotations import Rotations


def build_landscape(
    instance_filename, classical_opt_alg, optimisation_opts, write_csv=False, disp=False
):
    """This function generates a landscape for an instance problem. Currently the functions only work on ``n_rounds=1``

    :param instance_filename: Instance filename
    :type instance_filename: str
    :param classical_opt_alg: Name of Classical Optmisation Algorithm
    :type classical_opt_alg: str
    :param optimisation_opts: Optimisation Algorithm Parameters
    :type optimisation_opts: dict
    :param write_csv: Set to True to write results to ``csv`` file, defaults to False
    :type write_csv: bool, optional
    :param write_csv: Set to True to print landscape iteration messages, defaults to False
    :type disp: bool, optional
    :returns: Pandas Dataframe for the instance landscape
    :rtype: pandas.DataFrame
    """

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
                n_rounds=1,
                classical_opt_alg="nelder-mead",
                optimiser_opts=optimisation_opts,
            )

            # Build Quantum Circuit
            instance.build_circuit()
            iteration += 1

            # Print the circuit being experimented on
            # print(instance.quantum_circuit)
            instance.simulate_circuit()
            instance.measure_energy()
            # Kick-off run
            if disp:
                print(
                    "Landscape Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
                    % (iteration, instance.alpha[0], instance.beta[0], instance.energy)
                )

            sim_dict = {"alpha": alp, "beta": bet, "energy": instance.energy}
            energy_ls.append(sim_dict)

        # Run Optimisation
        # energy_0 = instance.energy

    df = pd.DataFrame(energy_ls)

    # Write data out if required
    if write_csv:
        outfile = "data/processed/%s.csv" % instance_filename
        df.to_csv(outfile)

    return df


if __name__ == "__main__":

    instance_filename = "sample_instance"

    # Instance File
    optimisation_opts = {
        "xtol": 0.001,
        "disp": True,
        "adaptive": True,
        "simplex_area_param": 0.1,
        "classical_opt_alg": "nelder-mead",
    }

    build_landscape(
        instance_filename=instance_filename,
        classical_opt_alg="nelder-mead",
        optimisation_opts=optimisation_opts,
        write_csv=True,
    )
