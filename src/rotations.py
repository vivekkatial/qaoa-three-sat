import json
from qc_helpers import *


class Rotations(object):
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

    def get_interactions(self):
        """Gets the number of  interaction terms in the QC Circuit

        Returns:
            (int) The number of interaction terms for qubits
        """
        interactions = len(self.rotations[0]["qubits"])
        return interactions

    def build_hamiltonian(self):

        curr = 1
        #        for term in range(n_qubits):
        #            if term in self.n_qubits
        #                curr = p_I()

        H = "F"

        return H
