# PHY
# modulation BPSK, demodulation
# TSMA
# channel (BEC)

import random

# binary erase channel


def BEC(data, error_prob):

    data_size = len(data)
    for i in range(data_size):
        value = random.uniform(0, 1)
        if value < error_prob:
            data[i] = None
    return data

# block erase channel


def block_erase_channel(block_erase_prob, data, block_size):
    i = 0
    while i < len(data):
        value = random.uniform(0, 1)
        if value < block_erase_prob:
            data[i: i + block_size] = [None] * block_size
        i = i + block_size
    return data

# modulation_BPSK


def bpsk(data):
    for i in range(len(data)):
        if not data[i]:
            data[i] = -1
    return data

# demodulation_BPSK


def demoulation_bpsk(data):
    for i in range(len(data)):
        if data[i] == 1:
            data[i] = 1
        elif data[i] == -1:
            data[i] = 0
        else:
            data[i] = 0.5
    return data


# calculate error rate
def difference(data1, data2):
    size = len(data1)
    if size != len(data2):
        return 'Not equal length'
    count = 0
    for i in range(size):
        if data1[i] !=data2[i]:
            count += 1
    return count
