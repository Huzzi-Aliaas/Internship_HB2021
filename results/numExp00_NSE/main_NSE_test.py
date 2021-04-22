import sys; sys.path.append('../../')
import numpy as np
from gnse.solver import SolverBaseClass, SimpleSplitStepSolver
from gnse.tools import plot_evolution
from gnse.config import FTFREQ


def main():
    # -- SET PARAMETERS FOR COMPUTATIONAL DOMAIN
    tMax = 40.0  # (fs) bound for time mesh
    Nt = 2 ** 14  # (-) number of sample points: t-axis
    zMax = np.pi  # (micron) upper limit for propagation routine
    Nz = 1000  # (-) number of sample points: z-axis
    nSkip = 2  # (-) keep only every nskip-th system state

    # -- SET FIBER PARAMETERS
    b2 = -1.0  # (fs^2/micron)
    beta = lambda w: 0.5 * b2 * w * w  # (1/micron)
    beta1 = lambda w: b2 * w  # (fs/micron)
    beta2 = lambda w: b2  # (fs^2/micron)
    gamma = 1e-8  # (W/micron)

    # -- SET PULSE PARAMETERS
    c0 = 0.29979  # (fs/micron) free space speed of light
    t0 = 1.0  # (fs) pulse duration

    P0 = np.abs(beta2(0)) / t0 / t0 / gamma
    u_sol = (
        lambda t, z: 2 * np.sqrt(P0) * np.exp(0.5j * gamma * P0 * z) / np.cosh(t / t0)
    )

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    t = np.linspace(-tMax, tMax, Nt, endpoint=False)
    w = FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi
    z = np.linspace(0, zMax, Nz + 1)

    # -- INITIALIZE SOLVER
    my_solver = SimpleSplitStepSolver(z, t, beta(w), gamma, nSkip=nSkip)

    # -- SET INITIAL CONDITION AND RUN
    A0_t = u_sol(t, 0)
    my_solver.solve(A0_t)

    # -- SHOW RESULTS
    plot_evolution(
        my_solver.z, my_solver.t, my_solver.utz, tLim=(-10, 10), wLim=(-20, 20)
    )


if __name__ == "__main__":
    main()
