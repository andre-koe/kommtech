from random import sample

import numpy as np


class FixedErrorChannel:

    def __init__(self, num_bits: int):
        self._num_bits = num_bits

    def __call__(self, message: np.array):
        num_bits_to_flip = min(self._num_bits, len(message))
        indices_to_flip = np.random.choice(len(message), size=num_bits_to_flip, replace=False)
        message[indices_to_flip] = np.bitwise_xor(message[indices_to_flip], 1)
        print("FixedErrorChannel: ", message)
        return message
