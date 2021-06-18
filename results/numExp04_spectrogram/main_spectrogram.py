import sys; sys.path.append('../../')
import numpy as np
from gnse.spectrogram import spectrogram, plot_spectrogram

def fetch_data(f_name):
    dat = np.load(f_name)
    return dat['z'], dat['t'], dat['w'], dat['utz']


def main():
    # -- READ IN DATA
    f_name = '../numExp03_cleaned_up_soliton/res_S_DW_collision.npz'
    z, t, w, utz  = fetch_data(f_name)

    # -- SET BOUNDARIES FOR SPECTROGRAM FIGURE 
    #t_lim = (t.min(),t.max())
    t_lim = (-40,60)
    w_lim = (-15,35)

    # -- Z-POSITION AT WHICH TO COMPUTE SPECTROGRAM
    z_id = np.argmin(np.abs(z-16.))

    t_S, w_S, P_tw = spectrogram(t, w, utz[z_id], Nt=1000 , s0=1.)
    plot_spectrogram(z[z_id], t_S, w_S, P_tw, t_lim = t_lim, w_lim = w_lim)


def main2():
    # -- READ IN DATA
    f_name = '../numExp03_cleaned_up_soliton/res_S_DW_collision.npz'
    z, t, w, utz  = fetch_data(f_name)

    # -- SET BOUNDARIES FOR SPECTROGRAM FIGURE 
    t_lim = (-40,60)
    w_lim = (-15,35)


    for idx, i in enumerate(range(10,20,1)):
            print(idx, i)

    exit()

    for fig_id, ut in enumerate(utz[::6]):
        t_S, w_S, P_tw = spectrogram(t, w, ut, Nt=1000 , s0=1.0)
        plot_spectrogram(z[fig_id], t_S, w_S, P_tw, t_lim = t_lim, w_lim = w_lim, o_name = './figs/fig_%03d'%(fig_id))


if __name__ == '__main__':
    #main()
    main2()
