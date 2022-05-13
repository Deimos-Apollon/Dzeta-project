import random
from itertools import combinations

from matplotlib import pyplot as plt

from src.data_reading.data_reading import read_zeros_conjugate
from src.dirichlet_series.dirichlet_series_with_a_m_0.series_construction import create_series_a_m_zero_a_k_one, \
    create_series_many_a_i_zero_a_k_one


def save_coefs_plot_a_m_zero(coefs, plot_dir, m, k):
    """
    Save plot of coefs of Dirichlet series with fixed a_m=0, using default plot

    :param coefs: coefs of Dirichlet series with fixed a_m=0
    :param plot_dir: directory, where plot will be stored
    :param m: index of fixed a_m=0
    :param k: index of fixed a_k=1

    :return:
    """
    plt.figure(figsize=(14, 8))
    x_values = [i for i in range(1, len(coefs) + 1)]
    plt.title(f"a_{m}=0")
    plt.plot(x_values, [coef.real for coef in coefs])
    # выделим y = 0
    plt.plot(x_values, [0 for _ in coefs], color=u'#1f77b4', linestyle='--')
    # оранжевым обозначим точки коэффициентов
    plt.scatter(x_values, [coef.real for coef in coefs], color='indigo', s=25)
    # красным обозначим точки, где a_m=0
    if m < len(coefs):
        plt.scatter(m, coefs[m-1].real, color='red', label=f'a_{m}=0')

    if k < len(coefs):
        plt.scatter(k, coefs[k - 1].real, color='magenta', label=f'a_{k}=1')

    plt.xlabel('Индекс коэффициента')
    plt.ylabel('Значение коэффициента')
    plt.legend()

    plot_filename = f"{plot_dir}/a_{m}_0.png"
    with open(plot_filename, 'w') as file:
        plt.savefig(plot_filename)
    plt.close()


def save_coefs_plot_many_a_m_zero(coefs, plot_filename, plot_title, m_indexes, k):
    """
    Save plot of coefs of Dirichlet series with fixed a_m=0, using default plot

    :param coefs: coefs of Dirichlet series with fixed a_m=0
    :param plot_filename: file path, where plot will be stored
    :param plot_title: title for plot
    :param m_indexes: indexes of fixed a_m=0
    :param k: index of fixed a_k=1
    :return:
    """
    plt.figure(figsize=(14, 8))
    x_values = [i for i in range(1, len(coefs) + 1)]
    plt.plot(x_values, [coef.real for coef in coefs])
    # выделим y = 0
    plt.plot(x_values, [0 for _ in coefs], color=u'#1f77b4', linestyle='--')
    # оранжевым обозначим точки коэффициентов
    plt.scatter(x_values, [coef.real for coef in coefs], color='indigo', s=25)
    plt.title(plot_title)
    # красным обозначим точки, где a_m=0
    plt.scatter(m_indexes[0], coefs[m_indexes[0]-1].real, color='red', label="a_m=0") # строка для норм легенды
    for m in m_indexes:
        if m < len(coefs):
            plt.scatter(m, coefs[m-1].real, color='red')
    # зеленым обозначим точки, где a_k=1
    if k < len(coefs):
        plt.scatter(k, coefs[k - 1].real, color='magenta', label='a_k=1')

    plt.xlabel('Индекс коэффициента')
    plt.ylabel('Значение коэффициента')

    plt.legend()
    with open(plot_filename, 'w') as file:
        plt.savefig(plot_filename)
    plt.close()


def save_plots_and_coefs_many_ai_zero(k, m_indexes, zeros, end_point, file_dir):
    """
    Save plots and coefs for this combination of k and m_indexes.

    :param k: fix a_k = 1
    :param m_indexes: fix a_m = 0
    :param zeros: zeta-zeros
    :param end_point: the last index of a to show in plot (because first 60-70% of all coefs in plot are meaningful)
    :param file_dir: directory, where plot and coefs files will be stored.
    :return: None
    """
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
