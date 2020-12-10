"""
Helper functions for project on QAOA

Author: Vivek Katial
"""

import math
import json
import numpy as np
from scipy import sparse

####################################################
# Pauli Matrices
####################################################


def pauli_identity():
    """Pauli I"""
    return np.array([[1, 0], [0, 1]])


def sparse_pauli_identity():
    """Sparse Pauli I"""
    return sparse.csr_matrix(np.array([[1, 0], [0, 1]]))


def pauli_x():
    """Pauli X"""
    return np.array([[0, 1], [1, 0]])


def sparse_pauli_x():
    """Sparse Pauli I"""
    return sparse.csr_matrix(np.array([[0, 1], [1, 0]]))


def pauli_x_act_on_i(i, state):
    """Pauli X acting on qubit i"""
    state[i] = np.dot(pauli_x(), state[i])
    return state


def pauli_y():
    """Pauli Y"""
    return np.array([[0, complex(0, -1)], [complex(0, 1), 0]])


def pauli_y_act_on_i(i, state):
    """Pauli Y operating on qubit i"""
    state[i] = np.dot(pauli_y(), state[i])
    return state


def pauli_z():
    """Pauli Z"""
    return np.array([[1, 0], [0, -1]])


def pauli_z_acton_i(i, state):
    """Pauli Z operating on qubit i"""
    state[i] = np.dot(pauli_z(), state[i])
    return state


def pauli_h():
    """Hadamard Matrix"""
    return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])


def zero_state():
    """|0> State"""
    return np.array([[1], [0]])


def one_state():
    """|1> State"""
    return np.array([[0], [1]])


def plus_state():
    """|+> State"""
    return np.dot(pauli_h(), zero_state())


def minus_state():
    """|-> State"""
    return np.dot(pauli_h(), one_state())


def pauli_t():
    """Function for pauli t state"""
    return np.array([[1, 0], [0, math.e ** (complex(0, 1) * math.pi / 4)]])


####################################################
# Simulation Helpers
####################################################


def load_raw_instance(filename):
    """Function to load JSON instance file as a python `dict()`

    Parameters
    ----------
    filename : str
        instance filename

    Returns
    -------
    instance : dict
    """
    with open(filename) as instance_file:
        instance = json.load(instance_file)
        instance = json.loads(instance[0])
    return instance


def clean_instance(raw_instance):
    """Function to extract different qubit rotations from instance.

    :param raw_instance: The raw instance as a dictionary
    :type raw_instance: dict
    :returns: n_qubits, single_rotations, double_rotations, triple_rotations
    :rtype: {int, Rotation, Rotation, Rotation}
    """
    n_qubits = raw_instance["n_qubits"]
    single_rotations = raw_instance["single_qubit"]["rotations"][0]
    double_rotations = raw_instance["double_qubit"]["rotations"][0]
    triple_rotations = raw_instance["triple_qubit"]["rotations"][0]
    sat_assgn = raw_instance["sat_assgn"]

    return n_qubits, single_rotations, double_rotations, triple_rotations, sat_assgn


def calculate_rotation_angle_theta(alpha, r_coeff):
    """A function to calculate the rotation angle theta for the circuit

    Parameters
    ----------
    alpha : float
        Angle theta found by classical optimiser
    r_coeff : float
        Coefficient for pauli terms

    Returns
    -------
    angle : float
        Angle theta for rotation to apply
    """
    theta = -2 * alpha * r_coeff
    return theta


def calculate_p_success(pdf, n_qubits, sat_assgn):
    """Calculate the probability of success for the satisfying assignment

    :param pdf: Probability distribution as a list
    :type pdf: list
    :param n_qubits: Number of qubits
    :type n_qubits: int
    :param sat_assgn: Satisfying assignment
    :type sat_assgn: str
    """

    # Create variable formating for binary string
    format_str = "{0:0%sb}" % (n_qubits)
    instance_space = [format_str.format(i) for i in range(2 ** n_qubits)]
    return pdf[instance_space.index(sat_assgn)]
