# This code contains work to implement a QC instance of Exact Cover on QAOA
#
# Author: Vivek Katial

# importing Qiskit
from qiskit import Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

from math import pi


def calculate_rotation_angle_theta(alpha, r_coeff):
    """A function to calculate the rotation angle theta for the circuit

    :param alpha: Angle theta found by classical optimiser
    :type alpha: float
    :param r_coeff: Coefficient for pauli terms
    :type r_coeff: float
    ...
    :return: Angle theta for rotation to apply
    :rtype: float
    """
    theta = -2*alpha*r_coeff
    return theta
    

def initiate_circuit(n_qubits):
    """A function to initiate circuit as a qiskit QC circuit object.

    :param n_qubits: Number of qubits in system, defaults to 3
    :type n_qubits: int
    ...
    :return: An initialised quantum circuit with hadmards across all qubits
    :rtype: qiskit.circuit.quantumcircuit.QuantumCircuit
    """
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.barrier()
    return qc

def build_qc_circuit(instance, alpha, beta, init=True, qc=None):
    """ This function takes an instance of 3SAT-Exact Cover and builds the associated Quantum Circuit.
    
    :param instance: A JSON-dictionary which consists of a representation for the circuit for each instance.
    :type instance: dict
    :param alpha: An angle \alpha for which to apply the Pauli-Gate rotations
    :type alpha:  float
    :param beta: An angle \beta for which to apply each qubit
    :type beta:  float
    :param init: True if we are initialising a circuit, False otherwise
    :type init: Bool
    :param qc: A quantum circuit object
    :type qc: qiskit.circuit.quantumcircuit.QuantumCircuit
    ...
    :return: A quantum circuit for the instance of 3SAT
    :rtype: qiskit.circuit.quantumcircuit.QuantumCircuit
    """
    
    if init:
        qc = initiate_circuit(instance['n_qubits'])

    # Apply single qubit rotations
    for qubit in instance['single_qubit']['rotations']:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        qc.rz(theta, qubit['qubit'])


    # Apply Two qubit rotations
    for qubit in instance['double_qubit']['rotations']:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        # Apply on Gate Z_1 Z_2
        qc.cx(qubit['qubit'][0],qubit['qubit'][1])
        qc.rz(theta, qubit['qubit'][1])
        qc.cx(qubit['qubit'][0],qubit['qubit'][1])

    # Apply 3 qubit rotations
    for qubit in instance['triple_qubit']['rotations']:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        qc.cx(qubit['qubit'][0],qubit['qubit'][1])
        qc.cx(qubit['qubit'][1],qubit['qubit'][2])
        qc.rz(theta, qubit['qubit'][2])
        qc.cx(qubit['qubit'][1],qubit['qubit'][2])
        qc.cx(qubit['qubit'][0],qubit['qubit'][1])

    qc.barrier()
    
    # Apply X rotations
    qc.rx(beta, range(instance['n_qubits']))
    qc.barrier()
    return qc