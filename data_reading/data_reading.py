from flint import *
import numpy as np


def read_from_file(k, m, filename=None):
    """Read first k nulls with m precision
    \n k == -1 means reading all nulls"""
    if not filename:
        filename = "/media/deimos/Мои_файл_/PyCharmProjects/" \
                   "project_on_Riemann_dzeta_function/data_files/NImZetaZero40000_1_40000.val"
    arr = []
    ctx.dps = m
    with open(filename) as file:
        for i in range(k):
            number_str = file.readline()
            # берем срез с нулевого индекса до индекса "." + точность m
            number_str = number_str[:number_str.find('.') + m + 1]
            arr.append(number_str)
    return np.array(arr)


def read_zeros_conjugate(k, m, filename=None):
    """Read first k nulls with m precision
    #         \n k == -1 means reading all nulls"""
    if not filename:
        filename = "/media/deimos/Мои_файл_/PyCharmProjects/" \
                   "project_on_Riemann_dzeta_function/data_files/NImZetaZero40000_1_40000.val"
    arr = []

    with open(filename) as file:
        for i in range(k):
            number_str = file.readline()
            # ищем индекс знака .
            int_part_len = number_str.find('.')
            # берем срез с нулевого индекса до индекса "." + точность m
            number_str = number_str[:int_part_len + m + 1]
            ctx.dps = m + int_part_len
            number = acb("1/2", number_str)
            arr.append(number)
            number = acb("1/2", f"-{number_str}")
            arr.append(number)
    return np.array(arr)
