# Keming Chen, student number:2207263
# Image and video communication and signal processing, University of Bristol
# Research project, 2023/07

# main
import numpy as np
import time
import binary_system
import splitting_system
import matplotlib.pyplot as plt

time_start = time.time()

# Generator polynomials
polynomials_2 = np.matrix([[1, 0, 1], [1, 1, 1], [1, 1, 1]])
polynomials_3 = np.matrix([[1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 1]])
polynomials_4 = np.matrix([[1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1]])

# select the length type of data
block_size_input = [4, 7, 14]
print('select the length type: 1:short, 2:medium, 3:long')
length_type = 0
input(length_type)
block_size = block_size_input[length_type]
block_number = block_size * 3
data_size = block_size * block_number

# Binary erase channel system , check encode and decode algorithm
'''
v1 = 3
error_probability = np.arange(0.16, 0.40, 0.04)
BER = [[0] * len(error_probability) for i in range(v1)]
MCloop1 = 5000

for p in range(v1):
    if p == 0:
        polynomials = polynomials_2
    elif p == 1:
        polynomials = polynomials_3
    else:
        polynomials = polynomials_4

    BER[p] = binary_system.binary_system(polynomials, data_size, error_probability, MCloop1)
'''

# Block erase channel_compare constraints
v2 = 2  # the number of encoder
error_probability_2 = [0.2, 0.3, 0.4, 0.5]
BER_block = [[0] * len(error_probability_2) for i in range(v2)]
block_error_rate = [[0] * len(error_probability_2) for i in range(v2)]
MCloop2 = 5000

for p in range(v2):
    if p == 0:
        polynomials = polynomials_2
    elif p == 1:
        polynomials = polynomials_3
    else:
        polynomials = polynomials_4

    BER_block[p], block_error_rate[p] = splitting_system.block_system(polynomials, data_size, error_probability_2,
                                                 MCloop2, block_number)

    time_end = time.time()
    time_sum = (time_end - time_start) / 60           # unit is min
    print('Running time: ', time_sum)


print('BER:', BER_block)
print('Block error rate:', block_error_rate)

# draw figure
# remember to fix the label in the function
# draw picture 1
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.plot(error_probability_2, BER_block[0], marker='o', label='(3,1,2): BER')
ax.plot(error_probability_2, BER_block[1], marker='o', label='(3,1,3): BER')
ax.plot(error_probability_2, BER_block[2], marker='o', label='(3,1,4)')
ax.plot(error_probability_2, block_error_rate[0], marker='o', label='(3,1,2): packet error rate', linestyle=':')
ax.plot(error_probability_2, block_error_rate[1], marker='o', label='(3,1,3): packet error rate', linestyle=':')
ax.grid()

ax.set_yscale('log', base=10)
ax.set_title('The performance over Block Erase Channel(data size = 148 bits)')
ax.set_xlabel('The block erase probability')
ax.set_ylabel('BER/Packet error rate')
ax.legend(loc=0)

plt.show()
