from sympy import divisors

from src.data_reading.data_reading import read_zeros_conjugate
from src.dirichlet_series.dirichlet_series_with_a_m_0.research_classes_of_indexes import \
    is_all_indexes_in_different_classes
from src.dirichlet_series.dirichlet_series_with_a_m_0.series_construction import create_series_many_a_i_zero_a_k_one


def get_b_coefs(f, series_coefs) -> tuple[int, ...]:
    b = [series_coefs[0]]
    for i in range(2, f+2):
        b_i = series_coefs[i-1]
        for i_div in divisors(i, proper=True):
            b_i -= b[i_div-1]
        b.append(b_i)
    return tuple(b)


if __name__ == "__main__":
    zeros_filename = '/media/deimos/Мои_файл_/PyCharmProjects/' \
                     'project_on_Riemann_dzeta_function/data_files/NImZetaZero40000_1_40000.val'
    zeros_num, prec = 100, 200
    zeros = read_zeros_conjugate(zeros_num=zeros_num, precision=prec, filename=zeros_filename)

    k, m_inds = 1, (2, 3, 4, 5)
    if is_all_indexes_in_different_classes((k, *m_inds)):
        coefs = create_series_many_a_i_zero_a_k_one(zeros=zeros, k=k, m_indexes=m_inds)
        f = 1 + len(m_inds)
        b_coefs = get_b_coefs(f, coefs)
        for ind, coef in enumerate(b_coefs, 1):
            print(f'b_{ind}: {coef}')
    else:
        print('Индексы пересекаются по классам!')
