from flint import *


class DirichletSeries:
    """
    Class which represents Dirichlet series with given coefficients. Can be called with
    various x values multiple times.
    """
    def __init__(self, coefs):
        """
        :param coefs: series coefficients
        """
        self.coefs = coefs
        self.coefs_num = coefs.nrows()

    def __call__(self, s) -> acb:
        """
        Return the sum of this series given parameter s.

        :param s: complex number
        :return: complex value - sum of series in point s
        """
        value = acb(0)
        for i in range(self.coefs_num):
            value += self.coefs[i, 0] * acb(i + 1).pow(-s)
        return value


def create_one_series(zeros):
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
    return x


def create_many_series(zeros) -> acb_mat:
    """
    Функция, позволяющая построить сразу несколько рядов Дирихле, используя разное кол-во
    переданных нетривиальных нулей дзета-функции Римана.

    :param zeros: используемые для ряда нули
    :return: n рядов Дирихле
    """
    diagonal = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    diag = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    inv_n_tildedelta = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    l_mat = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    lin_vect_elem_new = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
    a = acb_mat(len(zeros) + 2, len(zeros) + 2, 0)
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
        for k in range(j - 1):
            lin_vect_elem_new[j, k] = l_mat[j, k] * (1 if j == 0 else diagonal[j - 1, 0])
        lin_vect_elem_new[j, j] = (1 if j == 0 else diagonal[j - 1, 0])
        inv_n_tildedelta[j, 0] = acb(1) / lin_vect_elem_new[j, 0]
        for k in range(j):
            a[j, k] = lin_vect_elem_new[j, k] * inv_n_tildedelta[j, 0]
    return a

# старая функция на всякий случай
# def _old_create_series(zeros):
#     """
#     :param zeros: используемые для ряда нули
#     :return: n рядов Дирихле
#     """
#     DIAGONAL = acb_mat([[0] for i in range(len(zeros) + 2)])
#     diag = acb_mat([[0] for i in range(len(zeros) + 2)])
#     InvNTildedelta = acb_mat([[0] for i in range(len(zeros) + 2)])
#     L = acb_mat(len(zeros) + 2, len(zeros) + 2)
#     LinVectElemNew = acb_mat(len(zeros) + 2, len(zeros) + 2)
#     a = acb_mat(len(zeros) + 2, len(zeros) + 2)
#     M = acb_mat(len(zeros), len(zeros))
#
#     for i in range(len(zeros)):
#         for j in range(len(zeros)):
#             M[i, j] = acb(i + 1).pow(-zeros[j])
#
#     for i in range(len(zeros)):
#         diag[i, 0] = M[i, i]
#         DIAGONAL[i, 0] = diag[i, 0] * (1 if i == 0 else DIAGONAL[i - 1, 0])
#         for j in range(i + 1, len(zeros)):
#             z = - M[j, i] / diag[i, 0]
#             L[j, i] = z
#             M[j, i] = z
#             for k in range(i + 1, len(zeros)):
#                 M[j, k] = M[j, k] + M[i, k] * M[j, i]
#                 L[j, k] = M[j, k]
#
#     for k in range(len(zeros)):
#         for i in range(k + 1, len(zeros)):
#             for j in range(i + 1, len(zeros)):
#                 L[j, k] = L[j, k] + L[i, k] * M[j, i]
#
#     for j in range(len(zeros)):
#         for k in range(j - 1):
#             LinVectElemNew[j, k] = L[j, k] * (1 if j == 0 else DIAGONAL[j - 1, 0])
#         LinVectElemNew[j, j] = (1 if j == 0 else DIAGONAL[j - 1, 0])
#         InvNTildedelta[j, 0] = acb(1) / LinVectElemNew[j, 0]
#         for k in range(j):
#             a[j, k] = LinVectElemNew[j, k] * InvNTildedelta[j, 0]
#     return a
