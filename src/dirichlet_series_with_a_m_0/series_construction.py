from flint import *


def create_series_a_m_zero_a_k_one(zeros, m: int, k: int) -> tuple:
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
    return tuple(elem for elem in x)


def create_series_many_a_i_zero_a_k_one(zeros, m_indexes: tuple, k: int = 1) -> tuple:
    """
    Function for finding Dirichlet series' coefficients with fixating a_m1 = a_m2 = ... = a_mp = 0, a_k=1.

    :param zeros: list of zeros
    :param m_indexes: tuple with indexes of coefs to be fixed =0
    :param k: index of a_k to be fixed = 1
    :return: tuple of series' coefs
    """

    k -= 1
    m_indexes = tuple(m-1 for m in m_indexes)

    # len(zeros) уравнений для обращения в 0 в нулях + уравнения для am=0 + уравнение для ak=1
    n = len(zeros) + len(m_indexes) + 1
    if len(m_indexes) > n-2:
        raise ValueError('Too many elements in indexes!')
    if k in m_indexes:
        raise ValueError('k in m_indexes: a_k=0 and a_k=1')

    a = acb_mat(n, n, 0)
    # создаем вектор B
    b = acb_mat(n, 1, 0)

    # заполняем матрицу коэффициентов
    for i, nont_zero in enumerate(zeros):
        for j in range(n):
            # a_indexes = 0 по условию, a_k занулим, т.к. перенесли вправо
            a[i, j] = acb(j + 1).pow(-nont_zero)

    # делаем строчку, чтобы определить a_k=1 (по умолчанию матрица нулевая)
    n_zeros = len(zeros)
    a[n_zeros, k] = 1
    b[n_zeros, 0] = 1

    # добавляем строчки, чтобы определить a_m=0 где m из m_indexes
    for i, m in zip(range(n_zeros+1, n), m_indexes):
        a[i, m] = acb('1')
        b[i, 0] = acb('0')

    x = a.solve(b)
    ans = tuple(elem for elem in x)
    return ans
