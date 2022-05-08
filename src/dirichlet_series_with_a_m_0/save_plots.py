from matplotlib import pyplot as plt

from src.data_reading.data_reading import read_zeros_conjugate
from src.dirichlet_series_with_a_m_0.series_construction import create_series_a_m_zero_a_k_one


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


if __name__ == "__main__":
    # example of usage
    zeros = read_zeros_conjugate(zeros_num=80,
                                 precision=200,
                                 filename='/data_files/NImZetaZero40000_1_40000.val',
                                 )
    coefs = create_series_a_m_zero_a_k_one(zeros, m=5)
    save_coefs_plot_a_m_zero(
                            coefs=coefs[:98],
                            plot_dir='/plots_pictures',
                            m=4)
