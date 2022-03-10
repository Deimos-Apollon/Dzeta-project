from flint import *


def create_series(zeros):
    """
    :param zeros: используемые для ряда нули
    :return: n рядов Дирихле
    """
    DIAGONAL = acb_mat([[0] for i in range(len(zeros) + 2)])
    diag = acb_mat([[0] for i in range(len(zeros) + 2)])
    InvNTildedelta = acb_mat([[0] for i in range(len(zeros) + 2)])
    L = acb_mat(len(zeros) + 2, len(zeros) + 2)
    LinVectElemNew = acb_mat(len(zeros) + 2, len(zeros) + 2)
    a = acb_mat(len(zeros) + 2, len(zeros) + 2)
    M = acb_mat(len(zeros), len(zeros))

    for i in range(len(zeros)):
        for j in range(len(zeros)):
            M[i, j] = acb(i + 1).pow(-zeros[j])

    for i in range(len(zeros)):
        diag[i, 0] = M[i, i]
        DIAGONAL[i, 0] = diag[i, 0] * (1 if i == 0 else DIAGONAL[i - 1, 0])
        for j in range(i + 1, len(zeros)):
            z = - M[j, i] / diag[i, 0]
            L[j, i] = z
            M[j, i] = z
            for k in range(i + 1, len(zeros)):
                M[j, k] = M[j, k] + M[i, k] * M[j, i]
                L[j, k] = M[j, k]

    for k in range(len(zeros)):
        for i in range(k + 1, len(zeros)):
            for j in range(i + 1, len(zeros)):
                L[j, k] = L[j, k] + L[i, k] * M[j, i]

    for j in range(len(zeros)):
        for k in range(j - 1):
            LinVectElemNew[j, k] = L[j, k] * (1 if j == 0 else DIAGONAL[j - 1, 0])
        LinVectElemNew[j, j] = (1 if j == 0 else DIAGONAL[j - 1, 0])
        InvNTildedelta[j, 0] = acb(1) / LinVectElemNew[j, 0]
        for k in range(j):
            a[j, k] = LinVectElemNew[j, k] * InvNTildedelta[j, 0]
    return a
