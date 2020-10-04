"""
This code contains the main Instance Class for QAOA 3SAT

Author: Vivek Katial
"""

# Standard Modules
from math import pi

# External Modules
import numpy as np
from qiskit import Aer, IBMQ
from qiskit import QuantumCircuit, execute

# Custom Modules
from rotations import Rotations
from qc_helpers import calculate_rotation_angle_theta, load_raw_instance, clean_instance
from optimiser.nelder_mead import NelderMead


class QAOAInstance3SAT:
    """This class is a generic class for an instance of QAOA 3SAT and
    it consists of all the base methods needed for our circuit evolution

    Attributes:
        n_qubits (int): The number of qubits
        single_rotations (list:dict): A list of dictionaries containing single qubit rotations
        double_rotations (list:dict): A list of dictionaries containing double qubit rotations
        triple_rotations (list:dict): A list of dictionaries containing triple qubit rotations
        classical_opt_alg (str): The classical optimisation algorithm being utilised to optimise angles
        optimiser_opts (dict): A dictionary with optimisation algorithm parameters
        optimiser (obj): Optimiser Object
        classical_iter (int): Number of iterations done on the classical optimisation algorithm
        circuit_init (bool): Boolean on whether or not circuit initiated
        alpha (list:float): A list of angle values \alpha
        beta (list:float): A list of angle values for \beta
        n_rounds (int): The number of rounds experiment runs for
        backend (object): An object representing where the simulation will run
        statevector (list:complex): An array of complex numbers representing the 2^n state vector
        hamiltonian (obj): A `numpy` array containing the problem Hamiltonian
        quantum_circuit (obj): A `qiskit` quantum circuit object
        energy (float): The energy cost

    Todo:
        - Add functionality for multiple rounds (need to parmaterise more alpha/beta)
        - Add test that opt-algo matches opt-algo-options

    """

    def __init__(
        self,
        n_qubits,
        single_rotations,
        double_rotations,
        triple_rotations,
        alpha,
        beta,
        classical_opt_alg,
        optimiser_opts,
        n_rounds=1,
        backend=Aer.get_backend("statevector_simulator"),
    ):

        self.n_qubits = n_qubits
        self.single_rotations = single_rotations
        self.double_rotations = double_rotations
        self.triple_rotations = triple_rotations

        # Optimization settings
        self.classical_opt_alg = classical_opt_alg
        self.optimiser_opts = optimiser_opts
        self.optimiser = None
        self.classical_iter = 0

        # Quantum SubRoutine Settings
        self.circuit_init = False
        self.alpha = alpha
        self.beta = beta
        self.n_rounds = n_rounds
        self.backend = backend
        self.statevector = None
        self.hamiltonian = None

        # Metric settings

        self.quantum_circuit = None
        self.energy = 0

    def initiate_circuit(self):
        """A function to initiate circuit as a qiskit QC circuit object.

        :param n_qubits: Number of qubits in system, defaults to 3
        :type n_qubits: int
        ...
        :return: An initialised quantum circuit with hadmards across all qubits
        :rtype: qiskit.circuit.quantumcircuit.QuantumCircuit
        """
        self.circuit_init = True
        self.quantum_circuit = QuantumCircuit(self.n_qubits, self.n_qubits)
        self.quantum_circuit.h(range(self.n_qubits))
        self.quantum_circuit.barrier()
        return self.quantum_circuit

    def add_single_rotations(self):
        """ Adding single qubit rotations to circuit"""
        # Apply single qubit rotations
        for qubit in self.single_rotations.rotations:
            theta = calculate_rotation_angle_theta(self.alpha[0], qubit["coefficient"])
            self.quantum_circuit.rz(theta, qubit["qubits"][0])

    def add_double_rotations(self):
        """ Adding two qubit rotations to circuit"""

        # Apply double qubit rotations
        for qubit in self.double_rotations.rotations:
            theta = calculate_rotation_angle_theta(self.alpha[0], qubit["coefficient"])
            # Apply on Gate Z_i Z_j
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])
            self.quantum_circuit.rz(theta, qubit["qubits"][1])
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])

    def add_triple_rotations(self):
        """Adding three qubit rotation terms into circuit"""

        # Apply 3 qubit rotations
        for qubit in self.triple_rotations.rotations:
            theta = calculate_rotation_angle_theta(self.alpha[0], qubit["coefficient"])
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])
            self.quantum_circuit.cx(qubit["qubits"][1], qubit["qubits"][2])
            self.quantum_circuit.rz(theta, qubit["qubits"][2])
            self.quantum_circuit.cx(qubit["qubits"][1], qubit["qubits"][2])
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])

    def close_round(self):
        """
        Closing the round of a quantum circuit (then measuring)
        """
        self.quantum_circuit.barrier()
        # Apply X rotations
        self.quantum_circuit.rx(self.beta[0], range(self.n_qubits))
        self.quantum_circuit.barrier()
        # self.quantum_circuit.measure(range(self.n_qubits), range(self.n_qubits))

    def simulate_circuit(self):
        """
        Simulate the quantum circuit and get the corresponding statevector
        """
        self.statevector = (
            execute(self.quantum_circuit, self.backend).result().get_statevector()
        )

    def build_hamiltonian(self):
        """
        Calculate circuit energy
        """
        self.single_rotations.build_hamiltonian()
        self.double_rotations.build_hamiltonian()
        self.triple_rotations.build_hamiltonian()
        # Build circuit Hamiltonian
        self.hamiltonian = (
            self.single_rotations.hamiltonian
            + self.double_rotations.hamiltonian
            + self.triple_rotations.hamiltonian
        )

    def cost_function(self, angles):
        """Circuit Cost function, run the circuit and measure the energy

        :param angles: Angle theta found by classical optimiser
        ...
        :return: self.energy
        :rtype: float
        """

        # Update angles
        print(
            "Classical Optimization Iteration %s: \t alpha=%s \t beta=%s \t energy=%s"
            % (self.classical_iter, angles[0], angles[1], self.energy)
        )

        self.alpha = [angles[0]]
        self.beta = [angles[1]]

        # Rebuild Circuit
        self.quantum_circuit = None
        self.initiate_circuit()
        self.add_single_rotations()
        self.add_double_rotations()
        self.add_triple_rotations()
        self.close_round()

        self.classical_iter += 1
        # Run circuit
        self.simulate_circuit()
        self.measure_energy()

        return self.energy

    def measure_energy(self):
        """
        Calculate circuit energy
        """
        self.build_hamiltonian()
        ham_state = np.matmul(self.hamiltonian, self.statevector)
        energy = np.dot(ham_state, np.conjugate(self.statevector))
        self.energy = energy.real

    def optimise_circuit(self):
        """
        Method to optimise the circuit
        """

        # Construct n-d array for Nelder-Mead
        angles = [self.alpha, self.beta]
        angles = [angle for i in angles for angle in i]

        # Build Optimiser Class
        if self.classical_opt_alg == "nelder-mead":
            # Initialise Nelder Mead
            self.optimiser = NelderMead(
                vars_vec=angles,
                cost_function=self.cost_function,
                options=self.optimiser_opts,
            )
        else:
            # Raise Error if a valid algorithm not specified
            RaiseError("Please Specify an Algorithm")

        # Optimise valid
        self.optimiser.optimise()

        # Return Optimised Variable Vector
        print(self.optimiser.vars_vec)
