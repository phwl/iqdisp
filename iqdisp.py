# Library for display of iq waveforms Philip Leong

import os
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class iqdisp:
    def __init__(self, bsize=1024*64):
        self.bsize = bsize

    # given file f in cint16 format, return block i (where blocks are of size self.bsize)
    @staticmethod
    def readiq(f, i, bsize):
        # extract block i
        dat = np.fromfile(f, dtype=np.short, count=bsize*2)

        # Convert interleaved format to complex numbers
        cdat = dat[0::2] + 1j*dat[1::2]
        return cdat

    # display a waterfall plot in ax
    @staticmethod
    def disp_spectrogram(ax, cdat):
        ax.specgram(cdat, Fs=100000000, sides='onesided', NFFT=1024)
        ax.set_ylabel('frequency')
        ax.set_xlabel('time')
        ax.set_title('waterfall')

    # display time series
    @staticmethod
    def disp_ts(ax, cdat):
        ax.plot(np.real(cdat), 'r')
        ax.plot(np.imag(cdat), 'g')
        ax.set_title('time domain')
        ax.set_xlabel('time')
        ax.set_ylabel('magnitude')

    # display fft
    @staticmethod
    def disp_fft(ax, cdat):
        ax.psd(cdat, Fs=100000000, sides='onesided', NFFT=1024)
        ax.set_title('psd');
        ax.set_xlabel('time')
        ax.set_ylabel('power')

    # display constellation
    @staticmethod
    def disp_const(ax, cdat):
        # Constellation
        ax.plot(np.real(cdat), np.imag(cdat), '.')
        ax.set_title('constellation')

    # display everything
    def disp_all(self, fname, f, i):
        # Create plots and title
        nplots = 0

        fig = plt.figure()
        ax1 = plt.subplot(212)
        ax2 = plt.subplot(221)
        ax3 = plt.subplot(222)
        fig.suptitle(fname + "-{} (B={})".format(i, self.bsize))

        # Fetch the data from f
        cdat = self.readiq(f, i, self.bsize)   

        # Display all the plots we need
        self.disp_spectrogram(ax1, cdat)
        self.disp_fft(ax2, cdat)
        self.disp_const(ax3, cdat)

        plt.show()


def main():
    # mostly the same as iqdisp.disp_all but needed to be duplicated
    # to make the animation work
    def update(i):
        if i >= (fsize // (4 * BSIZE)):
            exit(0)
        cdat = iqd.readiq(f, i, BSIZE)   
        fig.suptitle(fname + "-({})".format(i))
        ax1.clear()
        ax2.clear()
        ax3.clear()
        iqd.disp_spectrogram(ax1, cdat)
        iqd.disp_fft(ax2, cdat)
        iqd.disp_const(ax3, cdat)

    BSIZE = 1024 * 256       # block size to use

    # set up plot
    fig = plt.figure()
    ax1 = plt.subplot(212)
    ax2 = plt.subplot(221)
    ax3 = plt.subplot(222)

    # display object 
    iqd = iqdisp(BSIZE)

    # for each file
    for fname in sys.argv[1:]:
        fsize = os.path.getsize(fname)
        f = open(fname, 'r')
        anime = FuncAnimation(
                fig, update, interval = 50)
        plt.show()
        f.close()

if __name__ == "__main__":
    main()
