from circuits_IC import *

from IC_aux import sample_parameters, sample_function
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('--nqubits', type=int, default=4)
parser.add_argument('--nlayers', type=int, default = 4)
parser.add_argument('--model', type=int, default = 2)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--extra_dim', type=int, default=2)
parser.add_argument('--data_size', type=int, default=10)

def main(nqubits, nlayers, model, seed, extra_dim, data_size):
    if model == 1:
        circuit = single_qubit(nqubits, nlayers)

    elif model == 2:
        circuit = single_qubit_and_entangling(nqubits, nlayers)

    elif model == 3:
        circuit = permutation_simple(nqubits, nlayers)

    elif model == 4:
        circuit = permutation_double(nqubits, nlayers)

    elif model == 5:
        circuit = permutation_composed(nqubits, nlayers)

    circuit.create_PQC()
    circuit.create_QML()

    np.random.seed(seed)

    if model in [1, 2]:
        n_params = len(circuit.PQC.get_parameters())
    elif model == 3:
        n_params = circuit.nlayers
    elif model in [4, 5]:
        n_params = 2 * circuit.nlayers

    theta = sample_parameters(n_params, n=extra_dim)

    y_pqc = sample_function(circuit.energy, theta)
    namePQC = f'data/q{nqubits}_l{nlayers}_PQC{model}_y_r{seed}.csv'
    np.savetxt(namePQC, y_pqc)

    del y_pqc, namePQC

    y_uniform = sample_function(lambda x: circuit.function(x, 2 * np.pi* (np.random.rand(data_size) - 0.5)), theta)
    nameUNI = f'data/q{nqubits}_l{nlayers}_uniform{model}_y_r{seed}.csv'
    np.savetxt(nameUNI, y_uniform)

    del y_uniform, nameUNI
    
    
    y_gauss = sample_function(lambda x: circuit.function(x, np.sqrt(np.pi)* np.random.randn(data_size)), theta)
    nameGAUSS = f'data/q{nqubits}_l{nlayers}_gauss{model}_y_r{seed}.csv'
    np.savetxt(nameGAUSS, y_gauss)
    
    del y_gauss, nameGAUSS

    nameX = f'data/q{nqubits}_l{nlayers}_model{model}_X_r{seed}.csv'
    np.savetxt(nameX, theta)
    
    

if __name__ == '__main__':
    args = vars(parser.parse_args())    
    main(**args)
