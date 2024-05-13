import numpy as np

from a3.BSC import BSC
from a3.BlockCode import BlockCode
from a3.FixedErrorChannel import FixedErrorChannel
from a3.Source import Source
from a3.Simulation import Simulation


def exercise_4(msg: np.ndarray, p: np.ndarray, num_corr_bits: int, fixed_error_count: int):
    block_code = BlockCode(max_corr_bits=num_corr_bits, p=p)
    message = block_code.encode(msg)
    channel = FixedErrorChannel(fixed_error_count)
    error_msg = channel(message)
    print(error_msg)
    y_corr, err_count = block_code.decode(error_msg)
    print("Original Message: ", msg)
    print("Error Message: ", error_msg)
    print("Corrected Message: ", y_corr, " Error Count", err_count)

def exercise5(msg_length: int, max_corr_bits: int, error_prob: float):
    block_code = BlockCode(max_corr_bits)

    simulation = Simulation(block_code, 4, 1000, )






if __name__ == '__main__':

    # A.4
    # A.1

    """
    Example from lecture - works without issues
    
    Original Message:  [0 1 1 0]
    Error Message:  [0 0 0 0 1 1 0]
    Corrected Message:  [0 1 1 0]  Error Count 1
    
    exercise_4(np.array([0, 1, 1, 0]), p=np.array([[1, 1, 0],
                                                   [0, 1, 1],
                                                   [1, 1, 1],
                                                   [1, 0, 1]], dtype=int), num_corr_bits=1, fixed_error_count=1)
    """

    exercise_4(np.array([1, 0]), p=np.array([[1, 1, 1, 1, 0, 0],
                                                   [0, 0, 1, 1, 1, 1]], dtype=int),
               num_corr_bits=2,
               fixed_error_count=2)

    exercise_4(np.array([1, 0, 1]), p=np.array([[1, 1, 1, 1, 0, 0, 0],
                                             [0, 0, 1, 1, 1, 1, 0],
                                             [1, 0, 1, 0, 1, 0, 1]], dtype=int),
               num_corr_bits=2,
               fixed_error_count=2)


    for i in range(0, 1000):


    print(s())
