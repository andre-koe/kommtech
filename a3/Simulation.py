import numpy as np
import matplotlib.pyplot as plt
from a3.BlockCode import BlockCode
from a3.Source import Source


class Simulation:

    def __init__(self, block_code: BlockCode, message_length: int, run_for: int, channel):
        self.message_length = message_length
        self.block_code = block_code
        self.run_for = run_for
        self.channel = channel
        self.res = None

    def run(self):
        message = Source(self.message_length)
        encoded = self.block_code.encode(message)
        error_msg = self.channel(encoded)
        bit_error_before = np.count_nonzero(np.bitwise_xor(error_msg, encoded))
        corrected_msg, errors_corrected = self.block_code.decode(error_msg)
        if corrected_msg is None:
            corrected = False
            bit_error_after = 0
        else:
            bit_error_after = np.count_nonzero(np.bitwise_xor(corrected_msg, message))
            corrected = True
        return {
            "bit_error_before": bit_error_before,
            "bit_error_after": bit_error_after,
            "has_been_corrected": corrected,
            "errors_corrected": errors_corrected
        }

    def generate_statistics(self, run_for):
        res = []
        for i in range(run_for):
            res.append(self.run())

        k = len([e for e in res if e["bit_error_before"] == 0])
        n = len([e for e in res if e["errors_corrected"] != 0])
        c = len([e for e in res if e["has_been_corrected"]])
        d = len()

    def plot(self):
        pass