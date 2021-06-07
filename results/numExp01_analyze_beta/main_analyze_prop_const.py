import sys; sys.path.append("../../")
import numpy as np
import numpy as np
from gnse.propagation_constant import prop_const
from gnse.tools import plot_details_prop_const


def main():
    b0, b1, b2, b3, b4 = 0.0, 0.0, -1.0, 0.1, 0.0
    pc = prop_const(b0, b1, b2, b3, b4)

    # -- DETERMINE ZERO-DISPERSION POINT SEPARATING ANOMALOUS AND NORMAL DOMAIN OF DISPERSION
    w_min, w_max = 0., 50.
    w_Z = pc.find_root_beta2(w_min, w_max)
    print("# w_Z = %lf"%(w_Z))

    # -- DETERMINE FREQUENCY IN DOMAIN OF NORMAL DISPERSION, GV-MATCHED TO SOLITON
    w0, w_min, w_max = 0, w_Z, 20.
    w_GVM = pc.find_match_beta1(w0, w_min, w_max)
    print("# w_GVM = %lf"%(w_GVM))

    # -- SHOW BETA1 AND BETA2
    w = np.linspace(-5, 25, 100)
    plot_details_prop_const(w, pc.beta1(w), pc.beta2(w), oName = 'plot_beta2_%lf_beta3_%lf'%(b2,b3))


if __name__ == '__main__':
    main()
