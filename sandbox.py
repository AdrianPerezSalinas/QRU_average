from scipy.stats.qmc import LatinHypercube
from circuits_IC import single_qubit_and_entangling
from qibo.hamiltonians import TFIM
from IC_aux import sample_function, compute_steps, compute_IC, find_eps_max
import numpy as np

import matplotlib.pyplot as plt


eps_max = []

qubits_list = list(range(2,12,2))
for nqubits in qubits_list:
    nlayers = 12

    circuit = single_qubit_and_entangling(nqubits, nlayers)

    circuit.create_PQC()


    X, y = sample_function(energy, len(circuit.PQepsilons[np.argmax(IC_s)]C.get_parameters()), n=2)

    diff = compute_steps(X, y)


    print(diff)
    IC_s = []

    epsilons = np.logspace(-4, 4, 50)

    for eps in epsilons:
        IC_s.append(compute_IC(diff, eps))

    plt.plot(epsilons, IC_s)
    plt.xscale('log')

    plt.savefig('IC_demo_%s.pdf'%nqubits)

    eps_max.append(find_eps_max(diff))

plt.close()

plt.plot(qubits_list, eps_max)
plt.yscale('log')

plt.savefig('epsilon_max.pdf')