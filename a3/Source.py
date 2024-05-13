import numpy as np


class Source:

    def __init__(self, num_bits: int):
        self._num_bits = num_bits

    def __call__(self):
        return np.array([np.random.randint(0, self._num_bits) for _ in range(self._num_bits)]) % 2

