from math import lcm

from sympy import factorint


def get_mod_classes_via_search(f: int) -> tuple[tuple[int, ...]]:
    """
    Finds the mod classes of indexes for given f. One mod class is represented as tuple of 0 and 1,
    each value represents if members of this mod class are divisible by 2, 3, ..., f+1 depending on value's
    position. E. g.,for f=4 (1, 1, 0, 1) corresponds to mod class not div. by 4 and div. by 2, 3, 5.

    :param f: number of fixed coefs (a_k=1, a_m_i=0), e.g. f=3 for a1=1, a2=a3=0
    :return: tuples of tuples, which represent divisibility of class by values 2,3,...,f+1
    """
    mod_rows = [(0,), (1,)]
    for i in range(3, f + 2):
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
            # если степень простого
            if len(factors) == 1 and first_prime_deg > 1:
                for less_degrees in range(1, first_prime_deg):
                    if row[first_prime ** less_degrees - 2] == 0:
                        break
                else:
                    # на меньшие степени не делится - можем добавить делимость на эту
                    new_mod_rows.append((*row, 1))
                # на меньшие степени делится - можем добавить только неделимость на эту
                new_mod_rows.append((*row, 0))
                continue
            # если квадрат
            if len(factors) == 1 and first_prime_deg == 2:
                new_mod_rows.append((*row, 0))
                if row[first_prime - 2] == 1:
                    new_mod_rows.append((*row, 1))
                continue
            # если составное
            for prime, deg in factors.items():
                if row[prime ** deg - 2] == 0:
                    new_mod_rows.append((*row, 0))
                    break
            else:
                new_mod_rows.append((*row, 1))
        mod_rows = new_mod_rows
    return tuple(mod_rows)


def get_least_member_of_each_mod_class(mod_classes: tuple[tuple[int, ...]]) -> tuple[int, ...]:
    """
    Finds least index in each mod class.

    :param mod_classes: to get their right representation use get_mod_classes function
    :return: tuple of least index in each mod class
    """
    return tuple(lcm(*(value for value, flag in enumerate(divs, start=2) if flag != 0))
                 for divs in mod_classes)


def is_all_indexes_in_different_classes(inds):
    f = len(inds)
    ind_mod_classes = []
    for ind in inds:
        ind_mod_classes.append(tuple(div for div in range(2, f+2) if ind % div == 0))

    return len(set(ind_mod_classes)) == len(ind_mod_classes)


if __name__ == "__main__":
    mod_classes = get_mod_classes_via_search(3)
    print(mod_classes)
    members = get_least_member_of_each_mod_class(mod_classes)
    print(members)
