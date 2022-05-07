from flint import *
import numpy as np
import sympy as sp
from tqdm import tqdm


def create_series_a_m_zero_a_k_one(zeros, m: int, k: int = 1) -> tuple:
    """
    Function for finding Dirichlet series' coefficients with fixating a_m=0, a_k=1.

    :param zeros: list of zeros
    :param m: index of a_m to be fixed = 0
    :param k: index of a_k to be fixed = 1
    :return: tuple of series' coefs
    """
    n = len(zeros) + 2
    m -= 1  # -1 из-за специфики метода (а_k = 1 и переносится вправо) и -1 из-за нумерации
    k -= 1
    a = acb_mat(n, n)
    # заполняем матрицу коэффициентов
    for i, nont_zero in enumerate(zeros):
        for j in range(n):
            a[i, j] = acb(f"{j + 1}").pow(-nont_zero)

    # добавляем строчку, чтобы определить a_m и a_1
    for i in range(n):
        a[n - 2, i] = acb('0')
        a[n - 1, i] = acb('0')
    a[n - 2, k] = acb('1')
    a[n - 1, m] = acb('1')

    # создаем вектор B
    b = acb_mat(n, 1, 0)
    # определяем, чему равны a_m и a_k
    b[n - 2, 0] = acb('1')
    b[n - 1, 0] = acb('0')

    x = a.solve(b)
    ans = [elem for elem in x]
    return tuple(ans)
