import sys; sys.path.append('../../')
import numpy as np
from gnse.solver import Interaction_picture_method, SimpleSplitStepSolver, Symmetric_Split_Step_Solver
from gnse.tools import figure_1b
from gnse.config import FTFREQ
from gnse.propagation_constant import prop_const




def main():
    # -- SET PARAMETERS FOR COMPUTATIONAL DOMAIN
    tMax = 1  # (fs) bound for time mesh
    Nt = 1024  # (-) number of sample points: t-axis
    zMax = 0.5  # (micron) upper limit for propagation routine
    nSkip = 50  # (-) keep only every nskip-th system state

    # -- SET WAVEGUIDE PARAMETERS
    b0, b1, b2, b3, b4 = 0.0, 0.0, -0.01276, 0, 0.0 # ([bn] = fs^n/micron)
    pc = prop_const(b0, b1, b2, b3, b4)
    beta, beta1, beta2 = pc.beta, pc.beta1, pc.beta2
    gamma = 0.045    # (W/micron)
    
    
    # -- SET PULSE PARAMETERS
    t0 = 0.0284     # (fs) pulse duration of the soliton
    w0 = 0.0        # (rad/fs) location of the soliton (S) (anomalous dispersion)
    
    
    # ... PEAK INTENSITY OF THE SOLITON
    P0 = np.abs(beta2(w0)) / t0 / t0 / gamma
    # ... FUNCTION IMPLEMENTING SOLITON INITIAL CONDITION
    u_S  = lambda t: np.sqrt(P0) / np.cosh((t)/ t0)
    
  

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    t = np.linspace(-tMax, tMax, Nt, endpoint=False)
    w = FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi
    
    
    # -- ANONYMOUS FUNCTION: EXACT SOLITON SOLUTION
    _AExact = lambda z,t: np.sqrt(P0)/np.cosh(t/t0)*np.exp(0.5j*gamma*P0*z)

    # -- ANONYMOUS FUNCTION: ROOT MEAN SQUARE ERROR
    _RMSError = lambda x,y: np.sqrt(np.sum(np.abs(x-y)**2)/x.size)
    
    
    # -- RUN SIMULATION
    res = []
    for Nz in [2**n for n in range(7,14)]:
        print("# Nz = %d"%(Nz))
        _z = np.linspace(0, zMax, Nz, endpoint=True)
        
        
        # -- simple splitting scheme
        my_solver_1 = SimpleSplitStepSolver(_z, t, beta(w), gamma, nSkip=nSkip)        
        A0_t_1 = u_S(t)   # -- SET INITIAL CONDITION
        my_solver_1.solve(A0_t_1)
        Azt_1 = my_solver_1.utz
        
        # -- symmetric splitting scheme
        my_solver_2 = Symmetric_Split_Step_Solver(_z, t, beta(w), gamma, nSkip=nSkip)
        A0_t_2 = u_S(t)   # -- SET INITIAL CONDITION
        my_solver_2.solve(A0_t_2)
        Azt_2 = my_solver_2.utz  
        
        # -- interaction picture method        
        my_solver_3 = Interaction_picture_method(_z, t, beta(w), gamma, nSkip=nSkip)
        A0_t_3 = u_S(t)   # -- SET INITIAL CONDITION
        my_solver_3.solve(A0_t_3)
        Azt_3 = my_solver_3.utz
        z = my_solver_3.z
        
        AExact = _AExact(z[-1],t)

        # -- ACCUMULATE SIMULATION RESULTS
        res.append(( _z[1]-_z[0],              # z-stepsize
               _RMSError(AExact, Azt_1[-1]),  # RMSE - simple splitting scheme
               _RMSError(AExact, Azt_2[-1]),  # RMSE - symmetric splitting scheme
               _RMSError(AExact, Azt_3[-1])   # RMSE - interaction picture method 
              ))
              
        
        
    # -- POSTPROCESS RESULTS
    figure_1b(res, 'Quality_control.png')


if __name__ == "__main__":
    main()    
