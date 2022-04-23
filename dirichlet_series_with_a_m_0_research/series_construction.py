from flint import *
import numpy as np
import sympy as sp
from tqdm import tqdm


def create_one_series_a_m_zero_a_k_one(zeros, m: int, k: int = 1) -> tuple:
    """
    Function for finding Dirichlet series' coefficients with fixating a_m=0, a_k=1.

    :param zeros: list of zeros
    :param m: index of a_m to be fixed = 0
    :param k: inde of a_k to be fixed = 1
    :return: tuple of series' coefs
    """
    # a_k = 1 переносим вправо, поэтому длина = len(zeros)
    n = len(zeros)
    m -= 2  # -1 из-за специфики метода (а_k = 1 и переносится вправо) и -1 из-за нумерации
    k -= 1
    a = acb_mat(n, n)
    # заполняем матрицу коэффициентов
    for i, nont_zero in enumerate(zeros):
        # заполняем до k-го
        for j in range(0, k):
            a[i, j] = acb(f'{j + 1}').pow(-nont_zero)
        # заполняем после k-го
        for j in range(k, n):
            a[i, j] = acb(j + 2).pow(-nont_zero)

    # добавляем строчку, чтобы определить a_m
    for i in range(n):
        a[n - 1, i] = acb('0')
    a[n - 1, m] = acb('1')

    # создаем вектор B, справа в уравнении стоят перенесенные слева коэффициенты
    b = acb_mat([[-(acb(f'{k + 1}').pow(-zero))] for zero in zeros])
    # делаем последнюю координату =0, чтобы определить a_m = 0
    b[n - 1, 0] = acb('0')

    x = a.solve(b)
    ans = [elem for elem in x]
    ans.insert(k, acb('1'))
    return tuple(ans)
