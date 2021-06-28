import sys; sys.path.append('../../../')
import numpy as np
from gnse.spectrogram import spectrogram, plot_spectrogram

def fetch_data(f_name):
    dat = np.load(f_name)
    return dat['z'], dat['t'], dat['w'], dat['utz']


def main():
    # -- READ IN DATA
    f_name = '../res_SC_generation.npz'
    z, t, w, utz  = fetch_data(f_name)

    # -- SET BOUNDARIES FOR SPECTROGRAM FIGURE 
    #t_lim = (t.min(),t.max())
    t_lim = (-100,400)
    w_lim = (-10,30)

    # -- Z-POSITION AT WHICH TO COMPUTE SPECTROGRAM
    z0 = 35.
    z_id = np.argmin(np.abs(z-z0))

    t_S, w_S, P_tw = spectrogram(t, w, utz[z_id], Nt=2000 , s0=2.5)
    plot_spectrogram(z[z_id], t_S, w_S, P_tw, t_lim = t_lim, w_lim = w_lim, o_name = 'fig_spectrogram_z%lf'%(z0))


def main2():
    # -- READ IN DATA
    f_name = '../res_SC_generation.npz'
    z, t, w, utz  = fetch_data(f_name)
    # -- CONSIDER DATA ONLY UP TO Z=50
    zmask = z<50
    z = z[zmask]
    utz = utz[zmask]
    #print(z.size);exit()

    # -- SET BOUNDARIES FOR SPECTROGRAM FIGURE 
    t_lim = (-100,400)
    w_lim = (-10,30)

    n_skip = 5
    for fig_id, ut in enumerate(utz[::n_skip]):
        t_S, w_S, P_tw = spectrogram(t, w, ut, Nt=1000 , s0=2.5)
        plot_spectrogram(z[n_skip*fig_id], t_S, w_S, P_tw, t_lim = t_lim, w_lim = w_lim, o_name = './figs/fig_%03d'%(fig_id))


if __name__ == '__main__':
    #main()
    main2()
