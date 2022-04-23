from matplotlib import pyplot as plt

from data_reading.data_reading import read_zeros_conjugate
from dirichlet_series_with_a_m_0_research.series_construction import *


def save_coefs_plot_a_m_zero(coefs, plot_dir, m):
    """
    Save plot of coefs of Dirichlet series with fixed a_m=0, using default plot

    :param coefs: coefs of Dirichlet series with fixed a_m=0
    :param plot_dir: directory, where plots will be stored
    :param m: index of fixed a_m=0
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
        plt.scatter(m, coefs[m-1].real, color='red')

    plot_filename = f"{plot_dir}/a_{m}_0.png"
    with open(plot_filename, 'w') as file:
        plt.savefig(plot_filename)
    plt.close()


def save_coefs_scatter_a_m_zero(coefs, plot_dir, m):
    """
    Save plot of coefs of Dirichlet series with fixed a_m=0, using scatter plots

    :param coefs: coefs of Dirichlet series with fixed a_m=0
    :param plot_dir: directory, where plots will be stored
    :param m: index of fixed a_m=0
    :return: None
    """
    plt.figure(figsize=(14, 8))
    x_values = [i for i in range(1, len(coefs) + 1)]
    plt.title(f"a_{m}=0")
    plt.scatter([x for ind, x in enumerate(x_values, start=1) if (ind % 2 != 0 and ind % 3 != 0)],
                [coef.real for ind, coef in enumerate(coefs, start=1) if (ind % 2 != 0 and ind % 3 != 0)],
                color='indigo')
    plt.scatter([x for ind, x in enumerate(x_values, start=1) if (ind % 2 == 0 and ind % 3 != 0)],
                [coef.real for ind, coef in enumerate(coefs, start=1) if (ind % 2 == 0 and ind % 3 != 0)],
                color='blue')
    plt.scatter([x for ind, x in enumerate(x_values, start=1) if (ind % 2 != 0 and ind % 3 == 0)],
                [coef.real for ind, coef in enumerate(coefs, start=1) if (ind % 2 != 0 and ind % 3 == 0)],
                color='green')
    plt.scatter([x for ind, x in enumerate(x_values, start=1) if (ind % 2 == 0 and ind % 3 == 0)],
                [coef.real for ind, coef in enumerate(coefs, start=1) if (ind % 2 == 0 and ind % 3 == 0)],
                color='black')
    # выделим y = 0
    plt.plot(x_values, [0 for _ in coefs], color=u'#1f77b4', linestyle='--')

    # красным обозначим точку, где a_m=0
    if m < len(coefs):
        plt.scatter(m, coefs[m - 1].real, color='red')

    plot_filename = f"{plot_dir}/a_{m}_0.png"
    with open(plot_filename, 'w') as file:
        plt.savefig(plot_filename)
    plt.close()


if __name__ == "__main__":
    # example of usage
    zeros = read_zeros_conjugate(zeros_num=150,
                                 precision=200,
                                 filename='/media/deimos/Мои_файл_/PyCharmProjects/'
                                          'project_on_Riemann_dzeta_function/'
                                          'data_files/NImZetaZero40000_1_40000.val',
                                 )
    coefs = create_one_series_a_m_zero_a_k_one(zeros, m=4)
    save_coefs_scatter_a_m_zero(
                            coefs=coefs[:100],
                            plot_dir='/media/deimos/Мои_файл_/PyCharmProjects'
                                     '/project_on_Riemann_dzeta_function/plots_pictures',
                            m=4)
