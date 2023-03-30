"""Simulating the ML Algoirthm

1. Use x' and x'' . seperatly
2. Print circuits
3. Print Histograms of outputs
4. Sort results for table"""

# x' Simulation:
# initiate an instance of the distance-based classifier
classifier = QuantumCompML()
x_prime = [-0.549, 0.836]  # x' in publication
# training set must contain tuples: (vector, class)
training_set = [
    ([0, 1], 0),  # class 0 training vector
    ([0.789, 0.615], 1)  # class 1 training vector
]
# extract training vectors
training_vectors = [tuple_[0] for tuple_ in training_set]

# initialize the Q and C registers
classifier.make_registers()

# get the angles needed to load the data into the quantum state
rotations = classifier.which_rotation(
    test_vector=x_prime,
    training_vectors=training_vectors
)

# create the quantum circuit
qc = classifier.make_circuit(rotations=rotations)
qc.draw(output='mpl')

# simulate and get the results
result = classifier.simulate(qc)
plot_histogram(result.get_counts(qc))

prob_0, prob_1 = classifier.postselect_results(result.get_counts(qc))
print(f"prob_class0 {prob_0}")
print(f"prob_class1 {prob_1}")

x = -1

if prob_0 > prob_1:
    x = 0
    print(f"x' = 0")
elif prob_0 < prob_1:
    x = 1
    print(f"x' = 1")
else:
    print('inconclusive. 50/50 results')

print(
    f"Simulating the Classification of x' = {x_prime} on the Aer simulator -- no noise")
print(f"Test vector x' was classified as class {x}\n")

# x'' Simulation:

# initiate an instance of the distance-based classifier
classifier = QuantumCompML()
x_double_prime = [0.053, 0.999]  # x' in publication

# training set must contain tuples: (vector, class)
training_set = [
    ([0, 1], 0),  # class 0 training vector
    ([0.789, 0.615], 1)  # class 1 training vector
]
# extract training vectors
training_vectors = [tuple_[0] for tuple_ in training_set]

# initialize the Q and C registers
classifier.make_registers()

# get the angles needed to load the data into the quantum state
rotations = classifier.which_rotation(
    test_vector=x_double_prime,
    training_vectors=training_vectors
)

# create the quantum circuit
qc = classifier.make_circuit(rotations=rotations)
qc.draw(output='mpl')

# simulate and get the results
result = classifier.simulate(qc)
plot_histogram(result.get_counts(qc))

prob_0, prob_1 = classifier.postselect_results(result.get_counts(qc))
print(f"prob_class0 {prob_0}")
print(f"prob_class1 {prob_1}")

x = -1

if prob_0 > prob_1:
    x = 0
    print(f"x' = 0")
elif prob_0 < prob_1:
    x = 1
    print(f"x' = 1")
else:
    print('inconclusive. 50/50 results')

print(
    f"Simulating the Classification of x' = {x_double_prime} on the Aer simulator -- no noise")
print(f"Test vector x' was classified as class {x}\n")

"""## Initiating the ML Algoirthm on QC

1. Use x' and x'' . seperatly
2. Print circuits
3. Print Histograms of outputs
4. Sort results for table"""

# x' on quantum computer

x_prime = [-0.549, 0.836]  # x' in publication
# training set must contain tuples: (vector, class)
training_set = [
    ([0, 1], 0),  # class 0 training vector
    ([0.789, 0.615], 1)  # class 1 training vector
]
# extract training vectors
training_vectors = [tuple_[0] for tuple_ in training_set]

# initialize the Q and C registers
classifier.make_registers()

# get the angles needed to load the data into the quantum state
rotations = classifier.which_rotation(
    test_vector=x_prime,
    training_vectors=training_vectors
)

# create the quantum circuit
qc = classifier.make_circuit(rotations=rotations)
qc.draw(output='mpl')

# Initializing the quantum computer
IBMQ.load_account()  # Load account from disk
IBMQ.providers()    # List all available providers

# Getting the provider
provider = IBMQ.get_provider('ibm-q')

# Choosing the quantum computer
qcomp = provider.get_backend('ibmq_16_melbourne')

# Executing the job on the QC
quantum_job = execute(qc, backend=qcomp, shots=50)  # Shots defined as 8192

# simulate and get the results
result = quantum_job.result()

plot_histogram(result.get_counts(qc))

x_double_prime = [0.053, 0.999]  # x'' in publication


def quantum_classify(self, test_vector, training_set):
    """
    Classifies the `test_vector` with the
    distance-based classifier using the `training_vectors`
    as the training set.
    This functions combines all other functions of this class
    in order to execute the quantum classification.
    """

    # extract training vectors
    training_vectors = [tuple_[0] for tuple_ in training_set]

    # initialize the Q and C registers
    self.make_registers(num_registers=4)

    # get the angles needed to load the data into the quantum state
    angles = self.get_angles(
        test_vector=test_vector,
        training_vectors=training_vectors
    )

    # create the quantum circuit
    qc = self.make_circuit(angles=angles)

    # simulate and get the results
    result = self.quantum_computer(qc)

    prob_class0, prob_class1 = self.interpret_results(result.get_counts(qc))

    if prob_class0 > prob_class1:
        return 0
    elif prob_class0 < prob_class1:
        return 1
    else:
        return 'inconclusive. 50/50 results'
