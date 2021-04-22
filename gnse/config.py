"""
Module containing helper routines, convenient abbreviations, and constants.
"""
import numpy as np
import numpy.fft as nfft

# -- CONVENIENT ABBREVIATIONS
FTFREQ = nfft.fftfreq
FT = nfft.ifft
IFT = nfft.fft
SHIFT = nfft.ifftshift
