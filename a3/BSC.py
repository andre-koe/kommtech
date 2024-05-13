from random import random

import numpy as np


class BSC:

    def __init__(self, error_probability: float = 0.1):
        self.error_probability = error_probability

    def __call__(self, message: np.array) -> np.array:
        errors = np.random.rand(*message.shape) < self.error_probability
        return np.bitwise_xor(message, errors.astype(int))
