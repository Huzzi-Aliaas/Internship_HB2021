"""
The provided module implements a convenience class for performing simple
calculations for a user-defined propagation constant.

"""
import scipy
import scipy.optimize as so
import scipy.misc as smi
import scipy.special as ssp
import numpy as np


class PropConst:
    r"""Convenience class for working with propagation constants.

    Implements methods that provide convenient access to recurrent tasks
    involving propagation constants.

    Args:
        beta_fun (:obj:`callable`):
            Function implementing a propagation constant.

    Attributes:
        beta_fun (:obj:`callable`):
            Function implementing a propagation constant.
        dw (:obj:`int`):
            Angular frequency increment used for calculating derivatives.
        c0 (:obj:`float`):
            Speed of light (default = 0.29970 micron/fs).
    """

    def __init__(self, beta_fun):
        self.dw = 1e-2
        self.beta_fun = beta_fun

    def beta(self, w):
        """Propagation constant.

        Args:
            w (:obj:`numpy.ndarray`):
                Angular frequency for which to compute propagation constant.

        Returns:
            :obj:`numpy.ndarray` or `float`: Propagation constant.
        """
        return self.beta_fun(w)

    def beta1(self, w):
        """Group delay.

        Args:
            w (:obj:`numpy.ndarray`):
                Angular frequency for which to compute group delay.

        Returns:
            :obj:`numpy.ndarray` or `float`: Group delay.
        """
        return smi.derivative(self.beta_fun, w, dx=self.dw, n=1, order=3)

    def beta2(self, w):
        """Group velocity dispersion (GVD).

        Args:
            w (:obj:`numpy.ndarray`):
                Angular frequency for which to compute GVD.

        Returns:
            :obj:`numpy.ndarray` or `float`: Group velocity dispersion.
        """
        return smi.derivative(self.beta_fun, w, dx=self.dw, n=2, order=5)

    def beta3(self, w):
        """Third order dispersion.

        Args:
            w (:obj:`numpy.ndarray`):
                Angular frequency for which to compute 3rd order dispersion.

        Returns:
            :obj:`numpy.ndarray` or `float`: Group velocity dispersion.
        """
        return smi.derivative(self.beta_fun, w, dx=self.dw, n=3, order=7)

    def vg(self, w):
        r"""Group velocity profile.

        Args:
            w (:obj:`numpy array` or `float`):
                Angular frequency for which to compute group-velocity.

        Returns:
            :obj:`numpy.ndarray` or `float`: Group velocity.
        """
        return 1.0 / self.beta1(w)


    def find_root_beta2(self, w_min, w_max):
        r"""Determine bracketed root of 2nd order dispersion profile.

        Attempts to find a root of the 2nd order dispersion profile in the
        interval from :math:`\omega_{\mathrm{min}}` to
        :math:`\omega_{\mathrm{max}}`.

        Note:
            * Helper method for analysis of dispersion profile
            * Uses scipy.optimize.bisect for bracketed root finding

        Args:
            w_min (:obj:`float`): lower bound for root finding procedure
            w_max (:obj:`float`): upper bound for root finding procedure

        Returns:
            :obj:`float`: root of 2nd order dispersion profile in bracketed
            interval

        """
        return so.bisect(self.beta2, w_min, w_max)

    def find_match_beta1(self, w0, w_min, w_max):
        r"""Determine group velocity matched partner frequency.

        Attempts to find a group-velocity matched partner frequency for
        :math:`\omega_0` in the interval from :math:`\omega_{\mathrm{min}}` to
        :math:`\omega_{\mathrm{max}}`.

        Note:
            * Helper method for analysis of dispersion profile
            * Uses scipy.optimize.minimize_scalar for bracketed minimization
            * If no group velocity matched frequency is contained in the
              supplied interval, the output should not be trusted. Check the
              resulting frequency by assessing whether `beta1(res)==beta1(w0)`.

        Args:
            w0 (:obj:`float`):
                Frequency for which group velocity matched partner frequency
                will be computed.
            w_min (:obj:`float`):
                Lower bound for root finding procedure
            w_max (:obj:`float`):
                Upper bound for root finding procedure

        Returns:
            :obj:`float`: Group-velocity matched partner frequency of `w0`.
        """
        return so.minimize_scalar(
            lambda w: np.abs(self.beta1(w) - self.beta1(w0)),
            bounds=(w_min, w_max),
            method="bounded",
        ).x



def prop_const(b0, b1, b2, b3, b4):
    """Helper function for propagation constant.

    Enclosing function returning a closure implementing a polynomial expansion
    of the propagation constant.

    Returns:
        :obj:`callable`: Propagation constant.
    """
    beta_fun = np.poly1d([ b4/24, b3/6, b2/2, b1, b0 ])
    return PropConst(beta_fun)

