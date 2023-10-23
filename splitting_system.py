import numpy as np
import random
import encoder
import channel1
import Viterbi_decoder


def block_system(polynomials, data_size, error_probability, MCloop, block_number):
    constraints = np.size(polynomials, 1) - 1
    BER = [0] * len(error_probability)
    block_error_rate = [0] * len(error_probability)

    for i in range(len(error_probability)):

        difference_total = 0
        error_block = 0

        for j in range(MCloop):

            # generate bitstream and flushing bits
            bitstream = [random.randint(0, 1) for _ in range(data_size - constraints)] + [0] * constraints

            # encode
            encoded_data = encoder.encoder(bitstream, polynomials)

            # interleave
            interleaved_data = encoder.interleave(encoded_data, block_number)

            # modulation
            transmit_data = channel1.bpsk(interleaved_data)

            # channel_BEC
            received_data = channel1.block_erase_channel(error_probability[i], transmit_data, block_number)

            # receiver
            # demodulation
            demodulated_data = channel1.demoulation_bpsk(received_data)

            # de-interleave
            de_inter_data = encoder.interleave(demodulated_data, block_number)

            # decode
            decoded_data = Viterbi_decoder.viterbi_decoder(de_inter_data, polynomials)

            # calculate difference
            difference = channel1.difference(bitstream, decoded_data)
            difference_total += difference

            if difference != 0:
                error_block += 1

        BER[i] = difference_total / MCloop / data_size
        block_error_rate[i] = error_block / MCloop  # packet, not the split block
        print('error probability:', error_probability[i], 'constraints:', constraints)
        print('error_rate:', BER[i], 'error_packet', error_block)
    return BER, block_error_rate
