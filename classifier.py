"""
IMPLEMENTING A DISTANCE_BASED CLASSIFIER WITH A QUANTUM INTERFERENCE CIRCUIT

This is a quantum algoirthm implimenting the ML quantum algoirthm found in the paper found in the name above.

Author: Zaman Tekin
"""

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, BasicAer
from qiskit import *
from qiskit.tools.visualization import plot_bloch_multivector
import matplotlib

# Initializing the registers: 4 quantum, 4 classical
circuit.q = QuantumRegister(4)
circuit.cl = ClassicalRegister(4)

# Naming the quantum registers in the circuit
circuit.ancilla_q = circuit.q[0]
circuit.index_q = circuit.q[1]
circuit.data_q = circuit.q[2]
circuit.class_q = circuit.q[3]

# Creating the circuit
qc = QuantumCircuit(circuit.q, circuit.cl)

# Step A: Hadamard the ancilla and index quibits
qc.h(circuit.ancilla_q)
qc.h(circuit.index_q)
qc.barrier()

# Step B:
x_prime = [-0.549, 0.836]  # x' in publication
x_double_prime = [0.053, 0.999]  # x'' in publication

qc.cx(circuit.ancilla_q, circuit.data_q)
qc.u3(-4.30417579487669/2, 0, 0, circuit.data_q)
qc.cx(circuit.ancilla_q, circuit.data_q)
qc.u3(3.0357101997648965/2, 0, 0, circuit.data_q)

qc.draw(output='mpl')
