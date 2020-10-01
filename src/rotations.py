"""
Rotations Class for representing rotations on qubits

Author: Vivek Katial
"""

import numpy as np
from qc_helpers import pauli_z, pauli_identity


class Rotations:
    """This object represents the rotations that can exist on a set of qubits

    Attributes:
        rotations (:obj:`list`): A list of rotations

    """

    def __init__(self, rotations, n_qubits):
        """
        Initialisation method on the class for rotations

        Args:
            rotations (list): A list of dict()
            interactions (int): The number of interactions
        """
        self.rotations = rotations
        self.n_qubits = n_qubits
        self.interactions = self.get_interactions()
        self.hamiltonian = None

    def get_interactions(self):
        """Gets the number of  interaction terms in the QC Circuit

        Returns:
            (int) The number of interaction terms for qubits
        """
        interactions = len(self.rotations[0]["qubits"])
        return interactions

    def build_hamiltonian(self):
        """
        A function for building Hamiltonians
        """

        # Initialise empty hamiltonian
        hamiltonian = np.zeros((2 ** self.n_qubits, 2 ** self.n_qubits))

        for rotation in self.rotations:
            # Initialise current Ham
            curr = 1
            # Loop through qubits
            for term in range(self.n_qubits):
                # If Z-rotation operating on qubit i apply Z operation
                if term in rotation["qubits"]:
                    curr = np.kron(curr, pauli_z())
                # Else leave alone
                else:
                    curr = np.kron(curr, pauli_identity())

            hamiltonian += curr * rotation["coefficient"]

        self.hamiltonian = hamiltonian
