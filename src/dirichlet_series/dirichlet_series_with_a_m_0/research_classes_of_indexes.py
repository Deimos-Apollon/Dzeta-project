from sympy import factorint, lcm


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
    pass
