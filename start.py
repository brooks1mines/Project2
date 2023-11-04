from qiskit.circuit.library import EfficientSU2
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SPSA
from qiskit.primitives import Estimator
from qiskit.quantum_info import Pauli, Operator
import random

def generate_k_local_hamiltonian(num_qubits, k, num_terms=3):
    paulis = ['I', 'X', 'Y', 'Z']
    hamiltonian = 0

    for _ in range(num_terms):
        # Randomly generate a k-local term
        term = ''.join(random.choice(paulis if i < k else 'I') for i in range(num_qubits))
        # Add this term to the Hamiltonian with a random coefficient
        hamiltonian += Operator(Pauli(term)) * random.uniform(-1, 1)

    return hamiltonian

num_qubits = 4  # Total number of qubits in the system
k = 2  # We want to create a 2-local Hamiltonian
hamiltonian = generate_k_local_hamiltonian(num_qubits, k)
#print(hamiltonian)

# This function works well for circuit generation but others could be explored
# https://qiskit.org/documentation/stubs/qiskit.circuit.library.EfficientSU2.html
ansatz = EfficientSU2(num_qubits=num_qubits, entanglement='linear')

# Set up the optimizer, maxiter hasn't been adjusted to test performance.
# https://qiskit.org/documentation/stubs/qiskit.algorithms.optimizers.SPSA.html 
optimizer = SPSA(maxiter=250)

# Create the Estimator
estimator = Estimator()

# VQE or Variational Quantum Eigensolver finds the ground state eigenvalue but this is just setup
# https://qiskit.org/ecosystem/algorithms/stubs/qiskit_algorithms.VQE.html#qiskit_algorithms.VQE.estimator
vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)

# Finds the minimum eigenvalue for the provided Hamiltonian
result = vqe.compute_minimum_eigenvalue(hamiltonian)

# Output the result
print('Ground state energy:', result.eigenvalue.real)
