# Viterbi decoding function
# input: transmitted data, polynomials(hex or bin), constraints
# soft decision
# backtracking
import copy
from itertools import chain
import numpy as np

def state_table(polynomials, number_state, v):

    state = [[0] * 4 for i in range(number_state)]

    for i in range(number_state):
        # now is state i (0 ~ 2^v-1)
        state[i][0] = i // 2  # col 1: next state, input = 0
        state[i][1] = i // 2 + number_state / 2  # col 2: next state, input = 1

        state_bi = bin(i)[2:]  # state binary, is string
        temp_state = [int(bit) for bit in state_bi]  # state binary, is list
        while len(temp_state) < v:
            temp_state.insert(0, 0)  # insert 0 before binary, ensure the length of state is v

        # col 3: output 1x3, input = 0
        temp_state.insert(0, 0)
        output = np.dot(temp_state, polynomials.T) % 2
        output = output.tolist()
        state[i][2] = list(chain(*output))

        # col 4, output 1x3, input = 1
        temp_state[0] = 1
        output = np.dot(temp_state, polynomials.T) % 2
        output = output.tolist()
        state[i][3] = list(chain(*output))

    return state

def HammingDist(x, y):
    distance = 0
    for i in range(0, len(x)):
        distance += abs(x[i] - y[i])
    return distance


def PathMetric(bits, path_metric, number_state, state):
    pre_pm = copy.copy(path_metric)
    source_state = [0] * number_state  # output

    for i in range(number_state):
        # i is target_state, find source_state
        source_state1 = int(i % (number_state / 2)) * 2
        source_state2 = source_state1 + 1

        # calculate Branch Metric
        a = int(i // (number_state / 2))
        Metrics1 = HammingDist(bits, state[source_state1][2 + a])
        Metrics2 = HammingDist(bits, state[source_state2][2 + a])

        # calculate pathmetric
        pm1 = pre_pm[source_state1] + Metrics1
        pm2 = pre_pm[source_state2] + Metrics2

        # update path_metrics
        if pm1 <= pm2:
            path_metric[i] = pm1
            source_state[i] = source_state1
        else:
            path_metric[i] = pm2
            source_state[i] = source_state2

    return source_state

def UpdateTrellis(trellis, source_state, number_state, i):
    pre_trellis = copy.deepcopy(trellis)
    for j in range(number_state):
        trellis[j] = copy.copy(pre_trellis[source_state[j]])
        trellis[j][i] = j
    return trellis


def back_track(MLtrellis, state):
    output_size = len(MLtrellis)
    output = [0] * output_size
    output[0] = 0 if MLtrellis[0] == state[0][0] else 1
    for i in range(1, output_size):
        output[i] = 0 if MLtrellis[i] == state[MLtrellis[i - 1]][0] else 1
    return output

def viterbi_decoder(data, polynomials):
    # Initialization
    constraint = np.size(polynomials, 1) - 1
    number_state = 2 ** constraint
    data_size = len(data)
    output_size = int(data_size / 3)

    path_metric =[0] + [float("inf")] * (number_state - 1)
    trellis = [[0] * output_size for i in range(number_state)]

    # generating states diagram
    state = state_table(polynomials, number_state, constraint)

    # decoding
    for i in range(output_size):
        # access 3 bit -is list
        current_bits = data[i * 3: i * 3 + 3]

        # update Path Metric and find the last state
        source_state = PathMetric(current_bits, path_metric, number_state, state)

        # update trellis
        trellis = UpdateTrellis(trellis, source_state, number_state, i)

    # get the ML path, generally, it is the one returns the state 0

    miniPM = min(path_metric)
    miniPM_idx = path_metric.index(miniPM)
    MLtrellis = trellis[miniPM_idx]

    # back track
    output = back_track(MLtrellis, state)

    return output