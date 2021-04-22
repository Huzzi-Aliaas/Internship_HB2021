"""
This module implements functions for postprocessing of simulation data.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
from .config import FTFREQ, FT, IFT, SHIFT


def plot_evolution(z, t, u, tLim=None, wLim=None, oName=None):
    def _setColorbar(im, refPos):
        x0, y0, w, h = refPos.x0, refPos.y0, refPos.width, refPos.height
        cax = f.add_axes([x0, y0 + 1.02 * h, w, 0.02 * h])
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

    def _truncate(I):
        I[I < 1e-6] = 1e-6
        return I

    w = SHIFT(FTFREQ(t.size, d=t[1] - t[0]) * 2 * np.pi)

    if tLim == None:
        tLim = (np.min(t), np.max(t))
    if wLim == None:
        wLim = (np.min(w), np.max(w))

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    cmap = mpl.cm.get_cmap("jet")

    # -- LEFT SUB-FIGURE: TIME-DOMAIN PROPAGATION CHARACTERISTICS
    It = np.abs(u) ** 2
    It /= np.max(It[0])
    It = _truncate(It)
    im1 = ax1.pcolorfast(
        t, z, It[:-1, :-1], norm=col.LogNorm(vmin=It.min(), vmax=It.max()), cmap=cmap
    )
    cbar1 = _setColorbar(im1, ax1.get_position())
    cbar1.ax.set_title(r"$|A|^2$ (normalized)", color="k", y=3.5)
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    ax1.set_xlim(tLim)
    ax1.set_ylim([0.0, z.max()])
    ax1.set_xlabel(r"Time $t$")
    ax1.set_ylabel(r"Propagation distance $z$")

    # -- RIGHT SUB-FIGURE: ANGULAR FREQUENCY-DOMAIN PROPAGATION CHARACTERISTICS
    Iw = np.abs(SHIFT(FT(u, axis=-1), axes=-1)) ** 2
    Iw /= np.max(Iw[0])
    Iw = _truncate(Iw)
    im2 = ax2.pcolorfast(
        w, z, Iw[:-1, :-1], norm=col.LogNorm(vmin=Iw.min(), vmax=Iw.max()), cmap=cmap
    )
    cbar2 = _setColorbar(im2, ax2.get_position())
    cbar2.ax.set_title(r"$|A_\omega|^2$ (normalized)", color="k", y=3.5)
    ax2.xaxis.set_ticks_position("bottom")
    ax2.yaxis.set_ticks_position("left")
    ax2.set_xlim(wLim)
    ax2.set_ylim([0.0, z.max()])
    ax2.set_xlabel(r"Angular frequency $\omega$")
    ax2.tick_params(labelleft=False)

    if oName:
        plt.savefig(oName + ".png", format="png", dpi=600)
    else:
        plt.show()
