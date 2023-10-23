import encoder
import channel1
import Viterbi_decoder
import random
import numpy as np


def binary_system(polynomials, data_size, error_probability, MCloop):

    constraints = np.size(polynomials, 1) - 1
    BER = [0] * len(error_probability)

    for i in range(len(error_probability)):

        difference = 0

        for j in range(MCloop):

            # generate bitstream and flushing bits
            bitstream = [random.randint(0, 1) for _ in range(data_size-constraints)] + [0] * constraints

            # encode
            encoded_data = encoder.encoder(bitstream, polynomials)

            # modulation
            transmit_data = channel1.bpsk(encoded_data)

            # channel_BEC
            received_data = channel1.BEC(transmit_data, error_probability[i])

            # receiver
            # demodulation
            demodulated_data = channel1.demoulation_bpsk(received_data)

            # decoding
            decoded_data = Viterbi_decoder.viterbi_decoder(demodulated_data, polynomials)

            # calculate difference
            difference += channel1.difference(bitstream, decoded_data)

        BER[i] = difference / MCloop / data_size

        print('error probability:', error_probability[i], 'constraints:', constraints)
        print('error_rate:', BER[i])

    return BER