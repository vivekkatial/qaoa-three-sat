"""

Author: Vivek Katial
"""
from instance import QAOAInstance3SAT
from qc_helpers import calculate_rotation_angle_theta, load_raw_instance, clean_instance
from rotations import Rotations


def main():

    instance_file = "data/raw/sample_instance.json"

    raw_instance = load_raw_instance(instance_file)

    n_qubits, single_rotations, double_rotations, triple_rotations = clean_instance(
        raw_instance
    )

    single_rotations = Rotations(single_rotations, n_qubits)
    double_rotations = Rotations(double_rotations, n_qubits)
    triple_rotations = Rotations(triple_rotations, n_qubits)

    instance = QAOAInstance3SAT(
        n_qubits=n_qubits,
        single_rotations=single_rotations,
        double_rotations=double_rotations,
        triple_rotations=triple_rotations,
    )

    instance.initiate_circuit()

    instance.add_single_rotations()
    instance.add_double_rotations()
    instance.add_triple_rotations(instance.alpha[0])
    instance.close_round(instance.beta[0])

    print(instance.quantum_circuit)
    instance.simulate_circuit()
    print(instance.statevector)
    X = single_rotations.build_hamiltonian()


if __name__ == "__main__":
    main()
