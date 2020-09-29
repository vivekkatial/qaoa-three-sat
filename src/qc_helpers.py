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
import json

import numpy as np
import math
import cmath

####################################################
# Pauli Matrices
####################################################

def pI():
    '''Pauli I'''
    return np.array([[1, 0], [0, 1]])

def sparse_pI():
    '''Sparse Pauli I'''
    return sparse.csr_matrix(np.array([[1, 0], [0, 1]]))

def pX():
    '''Pauli X'''
    return np.array([[0, 1],
                    [1, 0]])

def sparse_pX():
    '''Sparse Pauli I'''
    return sparse.csr_matrix(np.array([[0, 1], [1, 0]]))

def pXi(i,state):
    '''Pauli X acting on qubit i'''
    state[i] = np.dot(pX(),state[i])
    return state

def pY():
    '''Pauli Y'''
    return np.array([[0, complex(0,-1)],
                    [complex(0,1), 0]])

def pYi(i,state):
    '''Pauli Y operating on qubit i'''
    state[i] = np.dot(pY(),state[i])
    return state

def pZ():
    '''Pauli Z'''
    return np.array([[1, 0],
                    [0, -1]])

def pZi(i,state):
    '''Paulis Z operating on qubit i'''
    state[i] = np.dot(pZ(),state[i])
    return state

def pH():
    '''Hadamard Matrix'''
    return (1/np.sqrt(2))*np.array([[1, 1],
                                    [1, -1]])


def s0():
    '''|0> State'''
    return np.array([[1],[0]])
def s1():
    '''|1> State'''
    return np.array([[0],[1]])
def plus():
    '''|+> State'''
    return np.dot(pH(),s0())
def minus():
    '''|-> State'''
    return np.dot(pH(),s1())

def pT():
    return np.array([[1, 0],
                    [0, math.e**(complex(0,1)*math.pi/4)]])

####################################################
# Simulation Helpers
####################################################

def load_raw_instance(instance_file):
    with open(instance_file) as instance_file:
        instance = json.load(instance_file)
    return instance

def clean_instance(raw_instance):

    n_qubits = raw_instance["n_qubits"]
    single_rotations = raw_instance["single_qubit"]["rotations"][0]
    double_rotations = raw_instance["double_qubit"]["rotations"][0]
    triple_rotations = raw_instance["triple_qubit"]["rotations"][0]

    return n_qubits, single_rotations, double_rotations, triple_rotations



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
    for qubit in instance['single_qubit']['rotations'][0]:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        qc.rz(theta, qubit['qubits'][0])

    # Apply Two qubit rotations
    for qubit in instance['double_qubit']['rotations'][0]:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        # Apply on Gate Z_1 Z_2
        qc.cx(qubit['qubits'][0],qubit['qubits'][1])
        qc.rz(theta, qubit['qubits'][1])
        qc.cx(qubit['qubits'][0],qubit['qubits'][1])

    # Apply 3 qubit rotations
    for qubit in instance['triple_qubit']['rotations'][0]:
        theta = calculate_rotation_angle_theta(alpha, qubit['coefficient'])
        qc.cx(qubit['qubits'][0],qubit['qubits'][1])
        qc.cx(qubit['qubits'][1],qubit['qubits'][2])
        qc.rz(theta, qubit['qubits'][2])
        qc.cx(qubit['qubits'][1],qubit['qubits'][2])
        qc.cx(qubit['qubits'][0],qubit['qubits'][1])

    qc.barrier()
    
    # Apply X rotations
    qc.rx(beta, range(instance['n_qubits']))
    qc.barrier()
    return qc