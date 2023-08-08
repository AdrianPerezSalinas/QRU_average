import numpy as np
from scipy.stats.qmc import LatinHypercube
from scipy.optimize import minimize


def sample_parameters(param_dim, n=50):
    lhc = LatinHypercube(param_dim, )

    X = np.empty((param_dim * n, param_dim))
    for i, point in enumerate(lhc.random(param_dim * n)):
        X[i] = point

    return X

def sample_function(fun, X):
    y = []

    for i, point in enumerate(X):
        print('step %s / %s'%(i, len(X)))
        y.append(fun(2 * np.pi * point))


    return y


def compute_steps(X, y, seed=0):
    np.random.seed(seed=seed)
    p = np.random.permutation(len(y))
    X = X[p]
    y = y[p]

    diff = np.empty(len(y) - 1)

    for i in range(len(y) - 1):
        diff[i] = (y[i + 1] - y[i]) / np.linalg.norm(X[i + 1] - X[i])

    return diff


def compute_IC(diff, eps):
    steps = np.empty(len(diff))
    for i, d in enumerate(diff):
        if np.abs(d) < eps: steps[i] = int(0)
        else: steps[i] = int(np.sign(d))


    probs = np.zeros([3, 3])
    for i in range(len(steps) - 1):
        probs[int(steps[i] + 1), int(steps[i + 1] + 1)] += 1

    probs /= (len(steps) - 1)

    probs -= np.diag(np.diag(probs))

    ic = 0
    for p in probs.flatten():
        if p > 1e-4: ic += - p * np.log(p) / np.log(6)

    return ic


def find_eps_max(diff):
    epsilons = np.logspace(-4, 4, 10)
    IC_s = []
    for eps in epsilons:
        IC_s.append(compute_IC(diff, eps))

    eps_max = epsilons[np.argmax(IC_s)]
    del IC_s

    result = minimize(lambda eps: -compute_IC(diff, eps), x0 = eps_max, method='powell')

    return result['x']