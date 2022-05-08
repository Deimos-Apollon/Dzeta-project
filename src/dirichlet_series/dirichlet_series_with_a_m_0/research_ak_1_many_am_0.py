import random

from src.data_reading.data_reading import read_zeros_conjugate
from src.dirichlet_series.dirichlet_series_with_a_m_0.save_plots import save_coefs_plot_many_a_m_zero
from src.dirichlet_series.dirichlet_series_with_a_m_0.series_construction import create_series_many_a_i_zero_a_k_one
from itertools import combinations
from sympy.ntheory import factorint


def save_plots_and_coefs_many_ai_zero(k, m_indexes, zeros, end_point, file_dir):
    coefs = create_series_many_a_i_zero_a_k_one(zeros=zeros, m_indexes=m_indexes, k=k)

    filename = f"{file_dir}/a{k}_eq_1_and_"
    plot_title = f"a_{k}=1 and"
    for m in m_indexes:
        filename += f"a_{m}_"
        plot_title += f" a{m}"
    filename += f"eq_0"
    plot_title += f" =0"

    with open(f'{filename}.txt', 'w') as f:
        for ind, zero in enumerate(coefs, start=1):
            f.write(f"a_{ind:2}: {zero}\n")

    save_coefs_plot_many_a_m_zero(coefs[:end_point], f"{filename}_close_look.png",
                                  plot_title=plot_title,
                                  m_indexes=m_indexes, k=k)


def find_number_of_mod_classes(f):
    """

    :param f: number of fixed coefs (a_k=1, a_m_i=0)
    :return: number of mod classes for indexes
    """
    mod_rows = [(0, ), (1,)]
    for i in range(3, f+2):
        new_mod_rows = []
        factors = factorint(i)
        first_prime, first_prime_deg = factors.popitem()
        factors[first_prime] = first_prime_deg
        for row in mod_rows:
            # если простое
            if len(factors) == 1 and first_prime_deg == 1:
                new_mod_rows.append((*row, 0))
                new_mod_rows.append((*row, 1))
                continue
            # если квадрат
            if len(factors) == 1 and first_prime_deg == 2:
                new_mod_rows.append((*row, 0))
                if row[first_prime-2] == 1:
                    new_mod_rows.append((*row, 1))
                continue
            # если составное - пропускаем
            new_mod_rows.append(row)
        mod_rows = new_mod_rows
    print(f"Кол-во классов делимости для f={f}: {len(mod_rows)}")


if __name__ == "__main__":
    zeros_filename = '/data_files/NImZetaZero40000_1_40000.val'

    zeros_num, prec, end_point = 200, 200, 140
    zeros = read_zeros_conjugate(zeros_num=zeros_num, precision=prec, filename=zeros_filename)

    file_dir = "/plots_pictures/research ak=1 and many am=0"

    #save_plots_and_coefs_many_ai_zero(1, (6, 8, 10), zeros, end_point, file_dir)

    all_indexes = {5, 2, 10, 3, 15, 6, 30, 4, 20, 12, 60}
    part_of_indexes = {4, 6, 60}
    for k in part_of_indexes:
        indexes_tuple = random.sample(tuple(combinations(all_indexes.difference({k, }), 4)), 20)
        for inds in indexes_tuple:
            save_plots_and_coefs_many_ai_zero(k, inds, zeros, end_point, file_dir)

    # inds_set = {1, 2, 3, 6, 8, 12}
    # for k in inds_set:
    #     indexes_tuple = combinations({1, 2, 3, 6, 8, 12}.difference({k, }), 2)
    #     for inds in indexes_tuple:
    #         save_plots_and_coefs_many_ai_zero(k, inds, zeros, end_point, file_dir)
