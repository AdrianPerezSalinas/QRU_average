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
    nameUNI = f'data/q{nqubits}_l{nlayers}_uniform{model}_y_r{seed}.csv'
    theta = np.loadtxt(nameX)

    y_uniform = np.loadtxt(nameUNI)

    data_size = y_uniform.shape[-1]
    
    eps_uniform = np.zeros(data_size)
    for i in range(data_size):
        diff_uniform = compute_steps(theta, y_uniform[:, i])
        eps_uniform[i] = find_eps_max(diff_uniform)

    eps_uniform_1 = find_eps_max(compute_steps(theta, np.mean(y_uniform, axis=1)))
        
    nameEps = f'data_IC/q{nqubits}_l{nlayers}_model{model}_r{seed}.pkl'
    with open(nameEps, 'rb') as f:
        epsilons = pickle.load(f)
        
        
    epsilons['uniform']= eps_uniform
    epsilons['uniform1']= eps_uniform_1

    with open(nameEps, 'wb') as f:
        pickle.dump(epsilons, f)

if __name__ == '__main__':
    args = vars(parser.parse_args())
    main(**args)
