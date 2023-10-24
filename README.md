# Convolutional_ChannelCoding
Simulating the convolutional encoding and Viterbi decoding, combined with the TSMA, get the BER.

This code simulate the IoT wireless digital system in physical layer. The code rate is 1/3.
You can set the structure of convolutional code in main.py Changing the structure of code will affect the correcting performance. The free distance of the code with memory constraints of 2, 3 and 4 is 8, 10 and 12 respectively.


There are three length of input bitstream can choosed via input. These lengths can also be reset in main.py
The number of simulation loops is set as 5000, which can be nodified to get a smoother result graph.
