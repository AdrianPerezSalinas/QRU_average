import numpy as np
from scipy.stats.qmc import LatinHypercube
from scipy.optimize import minimize

'''
Functions to complete the sampling of information content
'''


def sample_parameters(param_dim, n=50):
    '''
    Creation of random points in the parameter space using latin hypercube sampling
    '''
    lhc = LatinHypercube(param_dim, )

    X = np.empty((param_dim * n, param_dim))
    for i, point in enumerate(lhc.random(param_dim * n)):
        X[i] = point

    return X

def sample_function(fun, X):
    '''
    Sampling of the function fun on the points in X
    '''

    y = []

    for point in X:
        y.append(fun(2 * np.pi * point))


    return y


def compute_steps(X, y, seed=0):
    '''
    Computation of the random walk in the parameter space for IC
    '''
    np.random.seed(seed=seed)
    p = np.random.permutation(len(y))
    X = X[p]
    y = y[p]

    diff = np.empty(len(y) - 1)

    for i in range(len(y) - 1):
        diff[i] = (y[i + 1] - y[i]) / np.linalg.norm(X[i + 1] - X[i])

    return diff


def compute_IC(diff, eps):
    '''
    Computation of information content
    '''
    steps = np.empty(len(diff))
    for i, d in enumerate(diff): #Discretization of the steps
        if np.abs(d) < eps: steps[i] = int(0)
        else: steps[i] = int(np.sign(d))


    probs = np.zeros([3, 3])
    for i in range(len(steps) - 1): # Computation of probabilities
        probs[int(steps[i] + 1), int(steps[i + 1] + 1)] += 1

    probs /= (len(steps) - 1)

    probs -= np.diag(np.diag(probs))

    ic = 0
    for p in probs.flatten():
        if p > 1e-4: ic += - p * np.log(p) / np.log(6) # Partial entropy giving IC

    return ic


def find_eps_max(diff):
    '''
    Search for the maximal eps
    '''
    epsilons = np.logspace(-4, 4, 10)
    IC_s = []
    for eps in epsilons:
        IC_s.append(compute_IC(diff, eps))

    eps_max = epsilons[np.argmax(IC_s)]
    del IC_s

    result = minimize(lambda eps: -compute_IC(diff, eps), x0 = eps_max, method='powell')

    return result['x']