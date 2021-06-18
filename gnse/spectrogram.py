import numpy as np
import numpy.fft as nfft
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
from .config import FT, IFT, FTFREQ, SHIFT


def spectrogram(t, w, ut, t_lim=None, Nt=1000, s0=20.0):
    """Compute spectrogram for time-domain input signal.

    Computes spectrogram of a time-domain input signal via short time Fourier
    transform employing a Gaussian window function.

    Args:
        t (:obj:`numpy.array`, 1-dim):
              Temporal grid.
        w (:obj:`numpy.array`, 1-dim):
              Angular-frequency grid.
        Et (:obj:`numpy-array`, 1-dim):
              Time-domain representation of analytic signal.
        t_lim (:obj:`list`):
              Delay time bounds for temporal axis considered for constructing
              the spectrogram (tMin, tMax), default is (min(t),max(t)).
        Nt (:obj:`int`):
              Number of delay times samples in [tMin, tMax], used for signal
              localization (default: Nt=1000).
        s0 (:obj:`float`):
              Root-mean-square width of Gaussian function used for signal
              localization (default: s0=20.0).

    Returns:
        :obj:`list`: (t_spec, w_spec, P_tw), where `t_seq`
        (:obj:`numpy.ndarray`, 1-dim) are delay times, `w`
        (:obj:`numpy.ndarray`, 1-dim) are angular frequencies, and `P_tw`
        (:obj:`numpy.ndarray`, 2-dim) is the spectrogram.
    """
    if t_lim == None:
        t_min, t_max = np.min(t), np.max(t)
    else:
        t_min, t_max = t_lim
    # -- DELAY TIMES
    t_seq = np.linspace(t_min, t_max, Nt)
    # -- WINDOW FUNCTION
    h = lambda t: np.exp(-(t ** 2) / 2 / s0 / s0) / np.sqrt(2.0 * np.pi * s0 * s0)
    # -- COMPUTE TIME-FREQUENCY RESOLVED CONTENT OF INPUT FIELD
    P = np.abs(FT(h(t - t_seq[:, np.newaxis]) * ut[np.newaxis, :], axis=-1)) ** 2
    return t_seq, SHIFT(w), np.swapaxes(SHIFT(P, axes=-1), 0, 1)


def plot_spectrogram(z_pos, t_delay, w_opt, P_tw, t_lim = None, w_lim = None, o_name = None):
    r"""Generate a figure of a spectrogram.

    Generate figure showing the intensity normalized spectrogram.  Scales the
    spectrogram data so that maximum intensity per time and frequency is unity.

    Args:
        t_delay (:obj:`numpy.ndarray`, 1-dim): Delay time grid.
        w_opt (:obj:`numpy.ndarray`, 1-dim): Angular-frequency grid.
        P_tw (:obj:`numpy.ndarray`, 2-dim): Spectrogram data.
    """
    if t_lim == None:
        t_min, t_max = t_delay[0], t_delay[-1]
    else:
        t_min, t_max = t_lim

    if w_lim == None:
        w_min, w_max = w_opt[0], w_opt[-1]
    else:
        w_min, w_max = w_lim


    f, ax1 = plt.subplots(1, 1, sharey=True, figsize=(4, 3))
    plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.78)
    cmap = mpl.cm.get_cmap("jet")

    def _setColorbar(im, refPos):
        """colorbar helper"""
        x0, y0, w, h = refPos.x0, refPos.y0, refPos.width, refPos.height
        cax = f.add_axes([x0, y0 + 1.02 * h, w, 0.05 * h])
        cbar = f.colorbar(im, cax=cax, orientation="horizontal")
        cbar.ax.tick_params(
            color="k",
            labelcolor="k",
            bottom=False,
            direction="out",
            labelbottom=False,
            labeltop=True,
            top=True,
            size=4,
            pad=0,
        )

        cbar.ax.tick_params(which="minor", bottom=False, top=False)
        return cbar

    _truncate = lambda I: np.where(I>I.max()*1e-5, I ,  I.max()*1e-5)

    I = _truncate(P_tw[:-1, :-1] / P_tw.max())
    im1 = ax1.pcolorfast(
        t_delay,
        w_opt,
        I,
        norm=col.LogNorm(vmin=1e-5 * I.max(), vmax=I.max()),
        cmap=cmap,
    )
    cbar1 = _setColorbar(im1, ax1.get_position())
    cbar1.ax.set_title(r"$P_S(t, \omega)$", color="k", y=3.5)

    ax1.set_xlim(t_min, t_max)
    ax1.set_ylim(w_min, w_max)
    ax1.tick_params(axis="y", length=2.0, direction="out")
    ax1.tick_params(axis="x", length=2.0, direction="out")
    ax1.set_xlabel(r"Delay time $t$")
    ax1.set_ylabel(r"Angular frequency $\omega$")

    ax1.text(0., 0., r'$z = %3.2lf$'%(z_pos), horizontalalignment='left', color='white',
                            verticalalignment='bottom', transform=ax1.transAxes)

    if o_name:
        plt.savefig(o_name + ".png", format="png", dpi=600)
        plt.close()
    else:
        plt.show()


