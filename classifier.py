###################################################################################################
# Implementing a distance-based classifier with a quantum interference circuit
# Based on the paper by the same name
###################################################################################################
# {License_info}
###################################################################################################
# Author: {Zaman Tekin}
# Credits: [Maria Schuld et el; see "arXiv:1703.10793v2"]
## Email: {email@zamantekin.com}
## Status: {Constructing}
###################################################################################################

"""Creating the functions of the Quantum Circuit and the ML Algoirthm
This class cointains the following fucntions:
1. Naming and creating the quantum and classical registers
2. The quantum circuits - rotations gates need to be changed according to the test and training vectors defined in 3.
3. Getting the the rotation for the gates in 2.
4. Simualtion function (noiseless)
5. Evaluating the results of the simualtion/quantum computation to find the the input class
    """


class QuantumCompML:

    def make_registers(self):
        "Create and define the regiisters to be used the the  quantum circuit"

        # Reigters are initialised
        self.quantum = QuantumRegister(4)
        self.classical = ClassicalRegister(4)

        # Naming the reigisters as found in above paper, page 8
        self.ancilla_q = self.quantum[0]
        self.index_q = self.quantum[1]
        self.data_q = self.quantum[2]
        self.class_q = self.quantum[3]

    def make_circuit(self, rotations):
        "Create the quantum circuit defined in the paper"
        "Returns the quantum circuit, qc"
        "Uses functions: make_registers; rotations"

        # Creating the qunatum circuit: 4 classical,for meaurment, and 4 quantum registers
        qc = QuantumCircuit(self.quantum, self.classical)

        # The step labeling will follow that of the paper's from page 4 and 9

        # STEP A
        # Hadamard on both ancilla and index qubit
        qc.h(self.ancilla_q)
        qc.h(self.index_q)

        # STEP B
        # Roation dependant on the Iris data point that needs classification
        qc.cx(self.ancilla_q, self.data_q)
        qc.u3(-rotations[0], 0, 0, self.data_q)
        qc.cx(self.ancilla_q, self.data_q)
        qc.u3(rotations[0], 0, 0, self.data_q)
        qc.barrier()  # wasn't working well without this barrier

        # STEP C
        # Done as defined on page 9
        qc.x(self.ancilla_q)
        qc.barrier()

        # STEP D
        # Done as defined on page 9
        qc.ccx(self.ancilla_q, self.index_q, self.data_q)
        qc.barrier()  # To prevent merging

        qc.x(self.index_q)
        qc.barrier()  # To prevent merging

        qc.ccx(self.ancilla_q, self.index_q, self.data_q)

        qc.cx(self.index_q, self.data_q)
        qc.u3(rotations[1], 0, 0, self.data_q)
        qc.cx(self.index_q, self.data_q)
        qc.u3(-rotations[1], 0, 0, self.data_q)

        qc.ccx(self.ancilla_q, self.index_q, self.data_q)

        qc.cx(self.index_q, self.data_q)
        qc.u3(-rotations[1], 0, 0, self.data_q)
        qc.cx(self.index_q, self.data_q)
        qc.u3(rotations[1], 0, 0, self.data_q)

        qc.barrier()

        # STEP E
        # MAJOR HACK: Found correction online. Paper was wrong
        qc.cx(self.index_q, self.class_q)
        qc.barrier()

        # STEP F
        # Done as defined on page 9
        qc.h(self.ancilla_q)
        qc.barrier()

        # Measure and write on classsical register
        qc.measure(self.quantum, self.classical)

        return qc

    def which_rotation(self, test_vector, training_vectors):
        "Funtion defines which roation is required for the specific vectors defined in the paper"
        "Returns the rotations of the quantum circuits involved, rotations"
        "Needs inputs: test_vector; training_vectors"

        rotations = []

        if test_vector == [-0.549, 0.836]:  # x'
            rotations.append(2.152)
        elif test_vector == [0.053, 0.999]:  # x''
            rotations.append(1.518)
        else:
            print('Fail_1')

        if training_vectors[0] == [0, 1] and training_vectors[1] == [0.789, 0.615]:
            rotations.append(0.331)
        else:
            print('Fail_2')

        return rotations

    def simulate(self, quantum_circuit):
        "Qiskit simulation"
        "Returns the simulation results, simulate_job.result()"
        "Needs inputs: quantum_circuit"

        # Noiseless simulation
        backend_noiseless = Aer.get_backend('qasm_simulator')

        # Executing the simulation job, bit of a hack, execute is not as good as other commands
        # Shots defined in paper
        simulate_job = execute(quantum_circuit, backend_noiseless, shots=8192)

        # Retrieve the results from the simulation
        return simulate_job.result()

    def quantum_computer(self, quantum_circuit):
        "Quantum computer implimentation"
        "Returns the quantum computations results, quantum_job.result()"
        "Needs inputs: quantum_circuit"

        # Initializing the quantum computer
        IBMQ.load_account()  # Load account from disk
        IBMQ.providers()    # List all available providers

        # Getting the provider
        provider = IBMQ.get_provider('ibm-q')

        # Choosing the quantum computer
        qcomp = provider.get_backend('ibmq_16_melbourne')

        # Executing the job on the QC
        quantum_job = execute(quantum_circuit, backend=qcomp,
                              shots=3)  # Shots defined as 8192

        # Retrieve the results from the simulation
        return quantum_job.result()

    def postselect_results(self, result_counts):
        "Postselecting results in order to define the class of the obhect: either 1 or 2"
        "Returns the probablities of class qubit either being |0> or |1>, prob_0, prob_1"
        "Needs inputs: result_counts"

        # Calulating total number of samples in results
        total_samples = sum(result_counts.values())

        # define lambda function that retrieves only results where the ancilla is in the |0> state
        def post_select(counts): return [
            (state, occurences) for state, occurences in counts.items() if state[-1] == '0']

        # perform the postselection
        postselection = dict(post_select(result_counts))
        postselected_samples = sum(postselection.values())

        print(
            f'Ancilla post-selection probability was found to be {postselected_samples/total_samples}')

        def retrieve_class(binary_class): return [
            occurences for state, occurences in postselection.items() if state[0] == str(binary_class)]

        prob_0 = sum(retrieve_class(0))/postselected_samples
        prob_1 = sum(retrieve_class(1))/postselected_samples

        print(f'Probability for class 0 is {prob_0}')
        print(f'Probability for class 1 is {prob_1}')

        return prob_0, prob_1
