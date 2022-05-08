from flint import acb


class DirichletSeries:
    """
    Class represents Dirichlet series with given coefficients. Can be called with
    various s values multiple times.
    """
    def __init__(self, coefs):
        """
        :param coefs: tuple of N series coefficients
        """
        self.coefs = coefs
        self.coefs_num = len(coefs)

    def __call__(self, s) -> acb:
        """
        Return the sum of this series given parameter s.

        :param s: complex number
        :return: complex value - sum of series in point s
        """
        value = acb('0')
        for i in range(self.coefs_num):
            value += self.coefs[i] * acb(i + 1).pow(-s)
        return value
