from circuits_IC import *

from IC_aux import compute_steps, find_eps_max
import numpy as np
from argparse import ArgumentParser
import pickle


parser = ArgumentParser()

parser.add_argument('--nqubits', type=int, default=10)
parser.add_argument('--nlayers', type=int, default = 6)
parser.add_argument('--model', type=int, default = 2)
parser.add_argument('--seed', type=int, default=0)


def main(nqubits, nlayers, model, seed):
    nameX = f'data/q{nqubits}_l{nlayers}_model{model}_X_r{seed}.csv'
    namePQC = f'data/q{nqubits}_l{nlayers}_PQC{model}_y_r{seed}.csv'
    nameUNI = f'data/q{nqubits}_l{nlayers}_uniform{model}_y_r{seed}.csv'
    nameGAUSS = f'data/q{nqubits}_l{nlayers}_gauss{model}_y_r{seed}.csv'
    theta = np.loadtxt(nameX)
    y_pqc = np.loadtxt(namePQC)
    y_uniform = np.loadtxt(nameUNI)
    y_gauss = np.loadtxt(nameGAUSS)

    assert y_uniform.shape == y_gauss.shape
    data_size = y_uniform.shape[-1]

    diff_pqc = compute_steps(theta, y_pqc)

    eps_pqc = find_eps_max(diff_pqc)

    eps_uniform = np.empty(data_size)
    eps_gauss = np.empty(data_size)

    for i in range(data_size):
        diff_uniform = compute_steps(theta, y_uniform[:, i])
        eps_uniform[i] = find_eps_max(diff_uniform)
        diff_gauss = compute_steps(theta, y_gauss[:, i])
        eps_gauss[i] = find_eps_max(diff_gauss)

    epsilons = {
        'PQC':eps_pqc, 
        'uniform':eps_uniform, 
        'gauss':eps_gauss
    }

    nameEps = f'data/q{nqubits}_l{nlayers}_model{model}_X_r{seed}.pkl'
    with open(nameEps, 'wb') as f:
        pickle.dump(epsilons, f)


if __name__ == '__main__':
    args = vars(parser.parse_args())
    main(**args)
