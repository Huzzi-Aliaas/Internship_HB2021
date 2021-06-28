import sys; sys.path.append('../../')
import numpy as np
from gnse.solver import Symmetric_Split_Step_Solver
from gnse.tools import plot_evolution
from gnse.config import FTFREQ, FT, IFT
from gnse.propagation_constant import prop_const
from gnse.tools import plot_details_prop_const


def main():
    # -- SET PARAMETERS FOR COMPUTATIONAL DOMAIN
    tMax = 400.0  # (fs) bound for time mesh
    Nt = 2 ** 13  # (-) number of sample points: t-axis
    zMax = np.pi  # (micron) upper limit for propagation routine
    Nz =  40000  # (-) number of sample points: z-axis
    nSkip = 100  # (-) keep only every nskip-th system state

    # -- SET WAVEGUIDE PARAMETERS
    b0, b1, b2, b3, b4 = 0.0, 0.0, -1.0, 0.1, 0.0 # ([bn] = fs^n/micron)
    pc = prop_const(b0, b1, b2, b3, b4)
    beta, beta1, beta2 = pc.beta, pc.beta1, pc.beta2
    gamma = 1.  # (W/micron)

    # -- SET PULSE PARAMETERS
    # ... DISPERSIVE WAVE:
    t1 = 2.0        # (fs) pulse duration of the dispersive wave (DW)
    w1 = 13.0       # (rad/fs) location of the dispersive (normal dispersion)
    s_fac = 10.    # (-) amplitude ratio of DW and S

    # -- SET INITIAL CONDITION
    # ... PEAK INTENSITY OF THE SOLITON
    P0 = np.abs(beta2(w1)) / t1 / t1 / gamma
    # ... FUNCTION IMPLEMENTING DISPERSIVE WAVE INITIAL CONDITION
    u_DW  = lambda t: s_fac*np.sqrt(P0)*np.exp(-1j*w1*t) / np.cosh((t)/t1)

    # -- DISPERSION LENGTH OF SOLITON
    LD = lambda w0, t0: t0*t0/np.abs(beta2(w0))

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    t = np.linspace(-tMax, tMax, Nt, endpoint=False)
    w = FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi
    z = np.linspace(0, 5*LD(w1,t1), Nz + 1)

    # -- INITIALIZE SOLVER
    my_solver = Symmetric_Split_Step_Solver(z, t, beta(w), gamma, nSkip=nSkip)

    # -- SET INITIAL CONDITION AND RUN
    A0_t = u_DW(t)
    my_solver.solve(A0_t)

    # -- TRANSFORM TO FRAME OF REFERENCE IN WHICH INITIAL PULSE IS STATIONARY 
    z = my_solver.z
    t = my_solver.t
    w = my_solver.w
    uwz = my_solver.uwz
    # ... REFERENCE VELOCITY
    v0 = 1./beta1(w1)
    # ... PERFORM SHIFT TO REFERENCE FRAME MOVING WITH VELOCITY v0
    utz = IFT(np.exp(-1j*w*z[:,np.newaxis]/v0)*uwz)

    # -- SAVE DATA
    results = {
        "t": t,
        "w": w,
        "z": z,
        "utz": utz,
    }
    np.savez_compressed('res_SC_generation', **results)

    # -- SHOW RESULTS
    plot_evolution(
        z, t, utz, tLim=(-100, 400), wLim=(-10, 30), oName='fig_SC_generation'
    )


if __name__ == "__main__":
    main()
