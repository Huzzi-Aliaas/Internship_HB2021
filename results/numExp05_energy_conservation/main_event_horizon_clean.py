import sys; sys.path.append('../../')
import numpy as np
from gnse.solver import Symmetric_Split_Step_Solver
from gnse.tools import plot_evolution
from gnse.config import FTFREQ, FT, IFT
from gnse.propagation_constant import prop_const
from gnse.tools import plot_details_prop_const


def energy(Iw):
    return np.sum(Iw,axis=-1)


def main():
    # -- SET PARAMETERS FOR COMPUTATIONAL DOMAIN
    tMax = 200.0  # (fs) bound for time mesh
    Nt = 2 ** 12  # (-) number of sample points: t-axis
    zMax = np.pi  # (micron) upper limit for propagation routine
    Nz =  20000  # (-) number of sample points: z-axis
    nSkip = 100  # (-) keep only every nskip-th system state

    # -- SET WAVEGUIDE PARAMETERS
    b0, b1, b2, b3, b4 = 0.0, 0.0, -1.0, 0.1, 0.0 # ([bn] = fs^n/micron)
    pc = prop_const(b0, b1, b2, b3, b4)
    beta, beta1, beta2 = pc.beta, pc.beta1, pc.beta2
    gamma = 1.  # (W/micron)

    # -- SET PULSE PARAMETERS
    # ... SOLITON:
    t0 = 0.5        # (fs) pulse duration of the soliton
    w0 = 0.0        # (rad/fs) location of the soliton (S) (anomalous dispersion)
    # ... DISPERSIVE WAVE:
    t1 = 4.0        # (fs) pulse duration of the dispersive wave (DW)
    w1 = 19.5       # (rad/fs) location of the dispersive (normal dispersion)
    t_sep = 30.0    # (fs) initial separation between S and DW
    s_fac = 0.2    # (-) amplitude ratio of DW and S

    # -- SET INITIAL CONDITION
    # ... PEAK INTENSITY OF THE SOLITON
    P0 = np.abs(beta2(w0)) / t0 / t0 / gamma
    # ... FUNCTION IMPLEMENTING SOLITON INITIAL CONDITION
    u_S  = lambda t: np.sqrt(P0) / np.cosh(t / t0)
    # ... FUNCTION IMPLEMENTING DISPERSIVE WAVE INITIAL CONDITION
    u_DW  = lambda t: s_fac*np.sqrt(P0)*np.exp(-1j*w1*t) / np.cosh((t-t_sep)/t1)

    # -- DISPERSION LENGTH OF SOLITON
    LD = lambda w0, t0: t0*t0/np.abs(beta2(w0))

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    t = np.linspace(-tMax, tMax, Nt, endpoint=False)
    w = FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi
    z = np.linspace(0, 600*LD(w0,t0), Nz + 1)

    # -- INITIALIZE SOLVER
    my_solver = Symmetric_Split_Step_Solver(z, t, beta(w), gamma, nSkip=nSkip)

    # -- SET INITIAL CONDITION AND RUN
    A0_t = u_S(t)  #+ u_DW(t)
    my_solver.solve(A0_t)

    # -- CLEAN UP THE SOLITON: GET RID OF BACKROUND RADIATION
    # ... CONSIDER THE SOLITON + EXCESS RADIATION AT z=20
    z_id = np.argmin(np.abs(my_solver.z-20))
    ut_s = np.copy(my_solver.utz[z_id])
    It_s = np.abs(ut_s)**2
    # ... FIND WHERE THE PEAK OF THE SOLITON IS SO WE CAN SHIFT IT BACK TO t=0
    t_max = t[np.argmax(It_s)]
    # ... SHIFT THE SOLITON BACK TO t=0
    ut_s = IFT(np.exp(-1j*w*t_max)*FT(ut_s))
    # ... FILTER OUT THE SOLITON AND GET RID OF THE EXCESS RADIATION
    t_mask = np.where(np.abs(t)<4,1,0)
    ut_s *= t_mask
    # ... SET UP THE NEW INITIAL CONDITION CONSISTING OF SOLITON + DW
    A0_t = ut_s  + u_DW(t)
    # ... CLEAN UP THE INTERNAL WORKING ARRAYS OF THE SOLVER
    my_solver._z = []
    my_solver._u = []
    # ... PERFORM A NEW SIMULATION RUN WITH A CLEANED UP INITIAL CONDITION
    my_solver.solve(A0_t)

    #It = np.abs(ut_s)**2
    #for i in range(t.size):
    #  print(t[i], It[i])
    #exit()

    # -- SAVE DATA
    results = {
        "t": my_solver.t,
        "w": my_solver.w,
        "z": my_solver.z,
        "utz": my_solver.utz,
    }
    #np.savez_compressed('res_S_DW_collision', **results)


    # -- COMPUTE THE PULSE ENERGIES
    z = my_solver.z
    w = my_solver.w
    uwz = my_solver.uwz
    Iw = np.abs(uwz)**2

    e_full = energy(Iw)
    e_a    = energy(Iw[:, w<10.])
    e_n    = energy(Iw[:, w>10.])

    for i in range(z.size):
        print(z[i], e_full[i], e_a[i], e_n[i])
    exit()

    # -- SHOW RESULTS
    oName = 'res_cleaned_up_t0_%lf_w0_%lf_t1_%lf_w1_%lf_tsep_%lf_sfac_%lf'%(t0,w0,t1,w1,t_sep,s_fac)
    plot_evolution(
        my_solver.z, my_solver.t, my_solver.utz, tLim=(-20, 100), wLim=(-20, 30), oName=oName
    )


if __name__ == "__main__":
    main()
