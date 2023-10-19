from circuits_IC import *

from IC_aux import sample_parameters, sample_function
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('--nqubits', type=int, default=10)
parser.add_argument('--nlayers', type=int, default = 6)
parser.add_argument('--model', type=int, default = 2)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--extra_dim', type=int, default=25)
parser.add_argument('--data_size', type=int, default=25)


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
    y_uniform = sample_function(lambda x: circuit.function(x, 2 * np.pi* (np.random.rand(data_size) - 0.5)), theta)
    y_gauss = sample_function(lambda x: circuit.function(x, np.sqrt(np.pi)* np.random.randn(data_size)), theta)
    nameX = f'data/q{nqubits}_l{nlayers}_model{model}_X_r{seed}.csv'
    namePQC = f'data/q{nqubits}_l{nlayers}_PQC{model}_y_r{seed}.csv'
    nameUNI = f'data/q{nqubits}_l{nlayers}_uniform{model}_y_r{seed}.csv'
    nameGAUSS = f'data/q{nqubits}_l{nlayers}_gauss{model}_y_r{seed}.csv'
    np.savetxt(nameX, theta)
    np.savetxt(namePQC, y_pqc)
    np.savetxt(nameUNI, y_uniform)
    np.savetxt(nameGAUSS, y_gauss)



if __name__ == '__main__':
    seed = vars(parser.parse_args())['seed']
    nqubits_list = [4, 6, 8, 10, 12]
    nlayers_list = [4, 8, 12, 20]
    models = [1, 2]
    seed_num = 10
    
    model_num = seed // (len(nqubits_list) * len(nlayers_list) * seed_num)
    seed = seed % (len(nqubits_list) * len(nlayers_list) * seed_num)
    model = models[model_num]

    q = seed // (len(nlayers_list) * seed_num)
    seed = seed % (len(nlayers_list) * seed_num)
    nqubits = nqubits_list[q]

    l = seed // (seed_num)
    seed = seed % (seed_num)
    nlayers = nlayers_list[l]

    extra_dim = 25
    data_size = 25

    print('nqubits', nqubits)
    print('nlayers', nlayers)
    print('model', model)
    print('seed', seed + 1)

    main(nqubits, nlayers, model, seed + 1, extra_dim, data_size)
