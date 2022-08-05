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

    # given file f in cint16 format, return block i (where blocks are of size BSIZE)
    @staticmethod
    def readiq(f, i, bsize):
        # extract block i
        try:
            # read values
            dat = np.fromfile(f, dtype=np.short, count=bsize*2, offset=i*bsize*2)
            # print(n, i, 'max(abs(dat))=', np.max(np.abs(dat)))
        except:
            return None

        # Convert interleaved format to complex numbers
        cdat = dat[0::2] + 1j*dat[1::2]
        return cdat

    # display a waterfall plot in ax
    @staticmethod
    def disp_spectrogram(ax, cdat):
        # split d into overlapping windows, do fft and put into spectrogram
        def spectrogram(d, fftsize=1024):
            step = fftsize // 4
            s = slice(0, None, step)
            a = np.lib.stride_tricks.sliding_window_view(d, fftsize)[s, :]
            img = abs(np.fft.fft(a))
            # print(img)
            return img
    
        # Waterfall
        ax.imshow(spectrogram(cdat))
        ax.set_xlabel('frequency')
        ax.set_ylabel('time')
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
        ax.semilogy(abs(np.fft.fft(cdat)))
        ax.set_title('fft')
        ax.set_xlabel('time')
        ax.set_ylabel('magnitude')

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
        try:
            cdat = iqd.readiq(f, i, BSIZE)   
            fig.suptitle(fname + "-({})".format(i))
            ax1.clear()
            ax2.clear()
            ax3.clear()
            iqd.disp_spectrogram(ax1, cdat)
            iqd.disp_fft(ax2, cdat)
            iqd.disp_const(ax3, cdat)
        except:
            exit(0)

    BSIZE = 1024 * 64       # block size to use

    # set up plot
    fig = plt.figure()
    ax1 = plt.subplot(212)
    ax2 = plt.subplot(221)
    ax3 = plt.subplot(222)

    # display object 
    iqd = iqdisp(BSIZE)

    # for each file
    for fname in sys.argv[1:]:
        f = open(fname, 'r')
        anime = FuncAnimation(
                fig, update, interval = 50)
        plt.show()
        f.close()

if __name__ == "__main__":
    main()
