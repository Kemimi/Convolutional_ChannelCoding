import copy
from itertools import chain
import numpy as np


# test
def encoder(data, polynomials):
    constraint = np.size(polynomials, 1) - 1

    # initial state
    state = np.zeros((1, constraint + 1), dtype=int)
    data_size = len(data)
    output = np.zeros((data_size, 3), dtype=int)

    # encoding
    for i in range(0, data_size):
        state[0, 0] = data[i]

        # encoding
        for j in range(3):
            output[i][j] = np.dot(state, polynomials[j, :].T) % 2

        state[0, 1:constraint + 1] = state[0, 0:constraint]

    output = output.tolist()
    output = list(chain(*output))

    return output


def interleave(data, degree):
    output = [0] * len(data)
    k = 0
    for j in range(degree):
        for i in range(degree):
            output[k] = data[i * degree + j]
            k += 1

    return output
