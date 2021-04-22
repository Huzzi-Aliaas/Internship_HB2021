"""
Implents solver base class that serves as driver for different propagation
algorithms. Currently, the following algorithms are supported:

    SimpleSplitStepSolver

DATE: 2021-04-22

CHANGELOG:

Do 22 Apr 2021 16:28:14 CEST
----------------------------
* refactored from project specific script -- OM
"""
import numpy as np
from .config import FTFREQ, FT, IFT


class SolverBaseClass:

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
        return IFT(np.asarray(self._u), axis=-1)

    @property
    def uwz(self):
        return np.asarray(self._u)

    @property
    def z(self):
        return np.asarray(self._z)

    def singleStep(self, uw):
        raise NotImplementedError


class SimpleSplitStepSolver(SolverBaseClass):

    def singleStep(self, uw):
        # -- DECLARE CONVENIENT ABBREVIATIONS
        dz, w, beta, gamma = self.dz, self.w, self.beta, self.gamma
        e_fac = np.exp(1j * dz * beta)
        # -- LINEAR HALF STEP / FREQUENCY DOMAIN
        _lin = lambda uw: e_fac * uw
        # -- NONLINEAR STEP / TIME DOMAIN
        _nlin = lambda ut: np.exp(1j * gamma * np.abs(ut) ** 2 * dz) * ut

        # -- ADVANCE FIELD
        return _lin(FT(_nlin(IFT(uw))))
