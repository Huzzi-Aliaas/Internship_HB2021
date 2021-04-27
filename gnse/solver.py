"""
Implents solver base class that serves as driver for different propagation
algorithms. Currently, the following algorithms are supported:

    SimpleSplitStepSolver

DATE: 2021-04-22

CHANGELOG:

Do 22 Apr 2021 16:28:14 CEST
----------------------------
* refactored from project specific script -- OM

Di 27 Apr 2021 18:18:33 CEST
----------------------------
* added doc-strings
* moved changelog to version.py

"""
import numpy as np
from .config import FTFREQ, FT, IFT


class SolverBaseClass:
    r"""Base class for solver.

    Implements solver base class that serves as driver for the implemented
    :math:`z`-propagation algorithms.

    Attributes:
        beta (:obj:`numpy.ndarray`):
           Frequency dependent propagation constant.
        gamma (:obj:`float` or :obj:`numpy.ndarray`):
           Coefficient function of nonlinear part.
        dz (:obj:`float`):
            Stepsize, i.e. :math:`z`-increment for integration.
        z_ (:obj:`numpy.ndarray`):
            :math:`z`-values used for :math:`z`-integration.
        t (:obj:`numpy.ndarray`):
            Temporal grid.
        w (:obj:`numpy.ndarray`):
            Angular frequency grid.
        _z (:obj:`list`):
            :math:`z`-values for which field is stored and available after
            propagation.
        _uz (:obj:`list`):
            Frequency domain representation of the field at :math:`z`-values
            listed in `_z`.
        nSkip (:obj:`int`):
            Step interval in which data is stored upon propagation (default: 1).

    Args:
        z (:obj:`numpy.ndarray`):
            :math:`z`-values used for :math:`z`-integration.
        t (:obj:`numpy.ndarray`):
            Temporal grid.
        beta (:obj:`numpy.ndarray`):
           Frequency dependent propagation constant.
        gamma (:obj:`float` or :obj:`numpy.ndarray`):
           Coefficient function of nonlinear part.
        nSkip (:obj:`int`):
            Step interval in which data is stored upon propagation (default: 1).

    """

    def __init__(self, z, t, beta, gamma, nSkip=1):
        self.nSkip = nSkip
        self.beta = beta
        self.gamma = gamma
        self.dz = z[1] - z[0]
        self.z_ = z
        self.t = t
        self.w = FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi
        self._z = []
        self._u = []

    def solve(self, u):
        r"""Propagate field

        Args:
            u (:obj:`numpy.ndarray`):
                Time-domain representation of initial field.
        """
        uw = FT(u)
        self._z.append(self.z_[0])
        self._u.append(uw)
        for i in range(1, self.z_.size):
            uw = self.singleStep(uw)
            if i % self.nSkip == 0:
                self._u.append(uw)
                self._z.append(self.z_[i])

    @property
    def utz(self):
        r""":obj:`numpy.ndarray`, 2-dim: Time-domain representation of field"""
        return IFT(np.asarray(self._u), axis=-1)

    @property
    def uwz(self):
        r""":obj:`numpy.ndarray`, 2-dim: Frequency-domain representation of
        field"""
        return np.asarray(self._u)

    @property
    def z(self):
        r""":obj:`numpy.ndarray`, 1-dim: :math:`z`-slices at which field is
        stored"""
        return np.asarray(self._z)

    def singleStep(self, uw):
        r"""Advance field by a single :math:`z`-slice"""
        raise NotImplementedError


class SimpleSplitStepSolver(SolverBaseClass):
    r"""Fixed stepsize algorithm implementing the simple split step
    method (SiSSM).

    Implements a fixed stepsize algorithm referred to as the simple split step
    Fourier method (SiSSM) [1].

    References:
        [1] T. R. Taha, M. J. Ablowitz,
        Analytical and numerical aspects of certain nonlinear evolution
        equations. II. Numerical, nonlinear Schrödinger equation,
        J. Comput. Phys. 55 (1984) 203,
        https://doi.org/10.1016/0021-9991(84)90003-2.
    """

    def singleStep(self, uw):
        r"""Advance field by a single :math:`z`-slice

        Implements simple splitting formula for split-step Fourier approach.

        Args:
            uw (:obj:`numpy.ndarray`): Frequency domain representation of the
            field at the current :math:`z`-position.

        Returns:
            :obj:`numpy.ndarray`: Frequency domain representation of the field
            at :math:`z` + :math:`dz`.
        """
        # -- DECLARE CONVENIENT ABBREVIATIONS
        dz, w, beta, gamma = self.dz, self.w, self.beta, self.gamma
        e_fac = np.exp(1j * dz * beta)
        # -- LINEAR STEP / FREQUENCY DOMAIN
        _lin = lambda uw: e_fac * uw
        # -- NONLINEAR STEP / TIME DOMAIN
        _nlin = lambda ut: np.exp(1j * gamma * np.abs(ut) ** 2 * dz) * ut

        # -- ADVANCE FIELD
        return _lin(FT(_nlin(IFT(uw))))


class Symmetric_Split_Step_Solver(SolverBaseClass):
    r"""Fixed stepsize algorithm implementing the symmetric split step
    method (SySSM).

    Implements a fixed stepsize algorithm referred to as the symmetric split
    step Fourier method (SySSM) as discussed in [1,2].

    References:
        [1] P. L. DeVries,
        Application of the Split Operator Fourier Transform method to the
        solution of the nonlinear Schrödinger equation,
        AIP Conference Proceedings 160, 269 (1987),
        https://doi.org/10.1063/1.36847.

        [2] J. Fleck, J. K. Morris, M. J. Feit,
        Time-dependent propagation of high-energy laser beams through the
        atmosphere: II,
        Appl. Phys. 10, (1976) 129,
        https://doi.org/10.1007/BF00882638.
    """

    def singleStep(self, uw):
        r"""Advance field by a single :math:`z`-slice

        Implements symmetric splitting formula for split-step Fourier approach.

        Args:
            uw (:obj:`numpy.ndarray`): Frequency domain representation of the
            field at the current :math:`z`-position.

        Returns:
            :obj:`numpy.ndarray`: Frequency domain representation of the field
            at :math:`z` + :math:`dz`.
        """

        # -- DECLARE CONVENIENT ABBREVIATIONS
        dz, w, beta, gamma = self.dz, self.w, self.beta, self.gamma
        e_fac = np.exp(0.5j * dz * beta)

        # -- LINEAR HALF STEP / FREQUENCY DOMAIN
        _lin = lambda uw: e_fac * uw
        # -- NONLINEAR STEP / TIME DOMAIN
        _nlin = lambda ut: np.exp(1j * gamma * np.abs(ut) ** 2 * dz) * ut

        # -- ADVANCE FIELD
        return _lin(FT(_nlin(IFT(_lin(uw)))))

