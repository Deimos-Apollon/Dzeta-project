from flint import *
import numpy as np


def read_zeros(zeros_num: int, precision: int, filename: str) -> np.array:
    """
    Read first 'zeros_num' zeta-function zeros with precision 'precision' digits after
    integer part from file.

    Parameters
    ----------
    zeros_num
        number of zeros, if -1, then read all 40000 zeros
    precision
        zeros precision (in digits after int part)
    filename
        file must be "NImZetaZero40000_1_40000.val"

    Returns
    -------
    np.array(float)
        An array of real numbers - coefficients of zeros imaginary parts

    """

    zeroes_arr = []
    ctx.dps = precision
    new_zeros_num = 40000 if zeros_num == -1 else zeros_num

    with open(filename) as file:
        for i in range(new_zeros_num):
            number_str = file.readline()
            int_part_len = number_str.find('.')
            # slice from 0 index to index of "." (int part) + precision after int part
            number_str = number_str[:int_part_len + precision + 1]
            ctx.dps = precision + int_part_len
            zeroes_arr.append(arb(number_str))
    return np.array(zeroes_arr)


def read_zeros_conjugate(zeros_num: int, precision: int, filename: str) -> np.array:
    """
    Read first 'zeros_num' zeta-function zeros with precision 'precision' digits after
    integer part from file.

    Parameters
    ----------
    zeros_num
        number of zeros, if -1, then read all 40000 zeros
    precision
        zeros precision (in digits after int part)
    filename
        file must be "NImZetaZero40000_1_40000.val"

    Returns
    -------
    np.array(float)
        An array of complex numbers - zeta-function zeros, conjugate zeros are grouped
    """

    zeroes_arr = []
    new_zeros_num = 40000 if zeros_num == -1 else zeros_num

    with open(filename) as file:
        for i in range(new_zeros_num):
            number_str = file.readline()

            int_part_len = number_str.find('.')
            # slice from 0 index to index of "." (int part) + precision after int part
            number_str = number_str[:int_part_len + precision + 1]
            ctx.dps = precision + int_part_len

            number = acb("1/2", number_str)
            zeroes_arr.append(number)
            number = acb("1/2", f"-{number_str}")
            zeroes_arr.append(number)
    return np.array(zeroes_arr)
