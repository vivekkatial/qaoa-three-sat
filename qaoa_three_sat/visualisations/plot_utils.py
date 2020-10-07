"""
This code contains plotting utility functions 

Author: Vivek Katial
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_state_vector(pdf, n_qubits, sat_assign=None):
    """Function to plot probability distribution function for a given state vector

    :param pdf: Probability distribution function
    :type pdf: numpy.array
    :param n_qubits: Number of qubits
    :type n_qubits: int
    :param sat_assign: List of satisfying assignments, defaults to None
    :type sat_assign: list, optional
    :returns: Plot of PDF
    :rtype: {matplotlib.plot}
    :raises: TypeError, ValueError
    """

    if not isinstance(n_qubits, int):
        raise TypeError("n_qubits must be an integer")
    if n_qubits <= 0:
        raise ValueError("n_qubits must be positive")

    # Create variable formating for binary string
    format_str = "{0:0%sb}" % (n_qubits)
    xlabs = [format_str.format(i) for i in range(2 ** n_qubits)]

    # Produce plots
    xbars = plt.bar(np.arange(len(pdf)), pdf)

    # Color according to best
    if sat_assign is not None:
        for ans in sat_assign:
            xbars[ans].set_color("#DC143C")

    plt.xticks(range(8), xlabs, rotation="vertical")
    return plt
