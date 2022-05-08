from flint import *


def create_one_series(zeros):
    """
    Creates Dirichlet series from zeros.

    :param zeros: list of zeta-function zeros
    :return: acb_mat 1xN of series' coefs, N - number of zeros+1
    """
    n = len(zeros) + 1
    a = acb_mat(n, n)
    # заполняем матрицу коэффициентов
    for i, nont_zero in enumerate(zeros):
        for j in range(n):
            a[i, j] = acb(j + 1).pow(-nont_zero)
    # добавляем строчку, чтобы определить a_1 = 1
    for i in range(1, n):
        a[n - 1, i] = 0
    a[n - 1, 0] = 1

    # создаем вектор B и делаем последнюю координату =1, чтобы определить a_1 = 1
    b = acb_mat([[0] for i in range(n)])
    b[n - 1, 0] = 1

    x = a.solve(b)
    return tuple(elem for elem in x)


def create_many_series(zeros) -> acb_mat:
    """
    Creates many Dirichlet series from zeros, using n zeros for each series, n=1...len(zeros).

    :param zeros: list of zeta-function zeros
    :return: acb_mat NxN, where N=len(zeros)+2, with series coefs (first and last two rows is 0)
    """
    diagonal = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    diag = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    inv_n_tildedelta = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    l_mat = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    lin_vect_elem_new = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    a = acb_mat(len(zeros), len(zeros), 0)
    m = acb_mat([
        [acb(i + 1).pow(-zeros[j]) for j in range(len(zeros))]
        for i in range(len(zeros))
    ])

    for i in range(len(zeros)):
        diag[i, 0] = m[i, i]
        diagonal[i, 0] = diag[i, 0] * (1 if i == 0 else diagonal[i - 1, 0])
        for j in range(i + 1, len(zeros)):
            z = - m[j, i] / diag[i, 0]
            l_mat[j, i] = z
            m[j, i] = z
            for k in range(i + 1, len(zeros)):
                m[j, k] = m[j, k] + m[i, k] * m[j, i]
                l_mat[j, k] = m[j, k]

    for k in range(len(zeros)):
        for i in range(k + 1, len(zeros)):
            for j in range(i + 1, len(zeros)):
                l_mat[j, k] = l_mat[j, k] + l_mat[i, k] * m[j, i]

    for j in range(len(zeros)):
        for k in range(j):
            lin_vect_elem_new[j, k] = l_mat[j, k] * (1 if j == 0 else diagonal[j - 1, 0])
        lin_vect_elem_new[j, j] = (1 if j == 0 else diagonal[j - 1, 0])
        inv_n_tildedelta[j, 0] = acb(1) / lin_vect_elem_new[j, 0]
        for k in range(j + 1):
            a[j, k] = lin_vect_elem_new[j, k] * inv_n_tildedelta[j, 0]
    return a
