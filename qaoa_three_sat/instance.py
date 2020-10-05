"""
This code contains the main Instance Class for QAOA 3SAT

Author: Vivek Katial
"""

# External Modules
import numpy as np
from qiskit import Aer, IBMQ
from qiskit import QuantumCircuit, execute

# Custom Modules
from rotations import Rotations
from qc_helpers import calculate_rotation_angle_theta
from optimiser.nelder_mead import NelderMead


class QAOAInstance3SAT:
    """This class is a generic class for an instance of QAOA 3SAT and
    it consists of all the base methods needed for our circuit evolution

    Attributes
    ----------
        n_qubits : int
            The number of qubits
        n_rounds : int
            The number of rounds the QAOA circuit is built for
        single_rotations : list
            `Rotations` Object for Single Qubit Rotations
        double_rotations : list
            `Rotations` Object for Double Qubit Rotations
        triple_rotations : list
            `Rotations` Object for Triple Qubit Rotations
        classical_opt_alg : str
            The classical optimisation algorithm being utilised to calc angles
        optimiser_opts : dict
            A dictionary with optimisation algorithm parameters
        optimiser : object
            Optimiser Object
        classical_iter : int
            Number of iterations done on the classical optimisation algorithm
        circuit_init : bool
            Boolean on whether or not circuit initiated
        alpha : list
            A list of angle values alpha
        beta : list
            A list of angle values for beta
        backend : object
            An object representing where the simulation will run (e.g. `Aer.get_backend('statevector_simulator'))
        statevector : list
            An array of complex numbers representing the 2^n state vector
        hamiltonian : np.array()
            A `numpy` array containing the problem Hamiltonian
        quantum_circuit : object
            A `qiskit` quantum circuit object
        energy : float
            The energy cost function value being minimised
    """

    def __init__(
        self,
        n_qubits,
        n_rounds,
        single_rotations,
        double_rotations,
        triple_rotations,
        alpha,
        beta,
        classical_opt_alg,
        optimiser_opts,
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
        self.n_rounds = n_rounds
        self.circuit_init = False
        self.alpha = alpha
        self.beta = beta
        self.backend = backend
        self.statevector = None
        self.hamiltonian = None

        # Metric settings

        self.quantum_circuit = None
        self.energy = 0

    @property
    def n_qubits(self):
        """ Get n_qubits"""
        return self._n_qubits

    @n_qubits.setter
    def n_qubits(self, value):
        if not isinstance(value, int):
            raise TypeError("n_qubits must be an integer")
        if value <= 0:
            raise ValueError("n_qubits must be positive")
        self._n_qubits = value

    @property
    def single_rotations(self):
        """ Get Single Qubit Rotations"""
        return self._single_rotations

    @single_rotations.setter
    def single_rotations(self, value):
        if not isinstance(value, Rotations):
            raise TypeError("single_rotations must be a Rotations Object")
        self._single_rotations = value

    @property
    def double_rotations(self):
        """ Get Double Qubit Rotations"""
        return self._double_rotations

    @double_rotations.setter
    def double_rotations(self, value):
        if not isinstance(value, Rotations):
            raise TypeError("double_rotations must be a Rotations Object")
        self._double_rotations = value

    @property
    def triple_rotations(self):
        """ Get Triple Qubit Rotations"""
        return self._triple_rotations

    @triple_rotations.setter
    def triple_rotations(self, value):
        if not isinstance(value, Rotations):
            raise TypeError("triple_rotations must be a Rotations Object")
        self._triple_rotations = value

    @property
    def alpha(self):
        """ Get Alpha Rotation Angles"""
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if not isinstance(value, list):
            raise TypeError("alpha must be a list")
        if len(value) != self.n_rounds:
            raise ValueError(
                "Insufficient alpha parameters passed. Should be %s - User passed %s"
                % (self.n_rounds, len(value))
            )
        self._alpha = value

    @property
    def beta(self):
        """ Get Beta Rotation Angles"""
        return self._beta

    @beta.setter
    def beta(self, value):
        if not isinstance(value, list):
            raise TypeError("beta must be a list")
        if len(value) != self.n_rounds:
            raise ValueError(
                "Insufficient beta parameters passed. Should be %s - User passed %s"
                % (self.n_rounds, len(value))
            )
        self._beta = value

    @property
    def classical_opt_alg(self):
        """ Get Classical Optimisation Algo"""
        return self._classical_opt_alg

    @classical_opt_alg.setter
    def classical_opt_alg(self, value):
        if not isinstance(value, str):
            raise TypeError("classical_opt_alg must be a string")
        # Add optimisers here as implemented
        if value not in ["nelder-mead"]:
            raise ValueError("classical_opt_alg currently not implemented")
        self._classical_opt_alg = value

    @property
    def optimiser_opts(self):
        """ Get Optimiser Option"""
        return self._optimiser_opts

    @optimiser_opts.setter
    def optimiser_opts(self, value):
        if not isinstance(value, dict):
            raise TypeError("optimiser_opts must be a `dict()`")
        if value["classical_opt_alg"] != self.classical_opt_alg:
            raise ValueError(
                "Optimiser options not consistent with Optimiser:%s"
                % self.classical_opt_alg
            )
        self._optimiser_opts = value

    def initiate_circuit(self):
        """A function to initiate circuit as a qiskit QC circuit object.
        ...
        :return: An initialised quantum circuit with hadmards across all qubits
        :rtype: qiskit.circuit.quantumcircuit.QuantumCircuit
        """
        self.circuit_init = True
        self.quantum_circuit = QuantumCircuit(self.n_qubits, self.n_qubits)
        self.quantum_circuit.h(range(self.n_qubits))
        self.quantum_circuit.barrier()
        return self.quantum_circuit

    def add_single_rotations(self, n_round):
        """ Adding single qubit rotations to circuit"""
        # Apply single qubit rotations
        for qubit in self.single_rotations.rotations:
            theta = calculate_rotation_angle_theta(
                self.alpha[n_round], qubit["coefficient"]
            )
            self.quantum_circuit.rz(theta, qubit["qubits"][0])

    def add_double_rotations(self, n_round):
        """ Adding two qubit rotations to circuit"""

        # Apply double qubit rotations
        for qubit in self.double_rotations.rotations:
            theta = calculate_rotation_angle_theta(
                self.alpha[n_round], qubit["coefficient"]
            )
            # Apply on Gate Z_i Z_j
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])
            self.quantum_circuit.rz(theta, qubit["qubits"][1])
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])

    def add_triple_rotations(self, n_round):
        """Adding three qubit rotation terms into circuit"""

        # Apply 3 qubit rotations
        for qubit in self.triple_rotations.rotations:
            theta = calculate_rotation_angle_theta(
                self.alpha[n_round], qubit["coefficient"]
            )
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])
            self.quantum_circuit.cx(qubit["qubits"][1], qubit["qubits"][2])
            self.quantum_circuit.rz(theta, qubit["qubits"][2])
            self.quantum_circuit.cx(qubit["qubits"][1], qubit["qubits"][2])
            self.quantum_circuit.cx(qubit["qubits"][0], qubit["qubits"][1])

    def close_round(self, n_round):
        """
        Closing the round of a quantum circuit (then measuring)
        """
        self.quantum_circuit.barrier()
        # Apply X rotations
        self.quantum_circuit.rx(self.beta[n_round], range(self.n_qubits))
        self.quantum_circuit.barrier()
        # self.quantum_circuit.measure(range(self.n_qubits), range(self.n_qubits))

    def build_circuit(self):
        """
        Class method to build the quantum circuit.
        """

        # Initiate Quantum Circuit
        self.initiate_circuit()

        for i in range(self.n_rounds):
            self.add_single_rotations(n_round=i)
            self.add_double_rotations(n_round=i)
            self.add_triple_rotations(n_round=i)
            self.close_round(i)

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
            % (
                self.classical_iter,
                angles[0 : self.n_rounds],
                angles[self.n_rounds :],
                self.energy,
            )
        )

        self.alpha = angles[0 : self.n_rounds].tolist()
        self.beta = angles[self.n_rounds :].tolist()

        # Rebuild Circuit
        self.quantum_circuit = None
        self.build_circuit()

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

        if self.quantum_circuit is None:
            raise AttributeError("Please Build Circuit before Optimization")

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
            raise ValueError("Please Specify an Algorithm")

        # Optimise Instance & Circuit
        self.optimiser.optimise()
