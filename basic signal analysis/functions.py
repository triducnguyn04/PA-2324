import scipy
import matplotlib.pyplot as plt
import numpy as np
import os

def refine(filename):
    count=0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    x_axis=[]
    y_axis=[]
    try:
        f = open(dir_path+'/raw_data/'+filename, "r")
        for x in f:
            if count>=4:
                a=x.split(':')
                b=a[-1].split(',')
                c=float(b[1])
                d=float(b[0])
                y_axis.append(c)
                x_axis.append(d)
            else:
                count+=1
        f.close()
    except:
        print("The file doesn't exist")
        return -1
    temp=x_axis[0]
    for i in range(len(x_axis)):
        x_axis[i]=x_axis[i]-temp
    return (x_axis,y_axis)

def visualize(filename):
    try:
        data=refine(filename)
        fig, ax = plt.subplots()     #Create a figure containing a single axes.
        ax.set_title('Time-amplitude plot')
        plt.xlabel("Time elapsed (s)")
        plt.ylabel("Voltage (V)")
        ax.plot(data[0],data[1])
        ax.axis([0, 0.05, 1.5*min(data[1]), 1.5*max(data[1])])
        ax.grid(True)
        plt.show()
    except:
        print("The file doesn't exist")
        return 0
    return 0

def all_fft(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        data = refine(filename)
        N = len(data[0])             #number of sample
        T = data[0][-1]/(N)          #sampling resolution
        fig, ax = plt.subplots(2, 2, layout='constrained')
        
        ax[0][0].set_title('Time-amplitude plot')
        ax[0][1].set_title('Fast Fourier transform plot')
        ax[1][0].set_title('Real fast Fourier transform plot')

        ax[0][0].set(xlabel='Time elapsed (s)', ylabel='Amplitude (V)')
        ax[0][1].set(xlabel='Frequency (Hz)', ylabel='Amplitude')
        ax[1][0].set(xlabel='Frequency (Hz)', ylabel='Amplitude')

        #time-amplitude plot
        ax[0][0].plot(data[0],data[1])
        ax[0][0].axis([0, 0.05, 1.5*min(data[1]), 1.5*max(data[1])])
        ax[0][0].grid(True)

        #fft
        yf = scipy.fft.fft(data[1])
        xf = scipy.fft.fftfreq(N, T)
        xf = scipy.fft.fftshift(xf)
        yf = scipy.fft.fftshift(yf)
        ax[0][1].plot(xf, np.abs(yf)/N)
        ax[0][1].grid(True)

        #rfft
        yf = scipy.fft.rfft(data[1])
        xf = scipy.fft.rfftfreq(N, T)
        ax[1][0].plot(xf, np.abs(yf)/N)
        ax[1][0].grid(True)

        #spectrogram
        #sampling rate = number of samples/total time
        ax[1][1].set_title('Spectrogram')
        ax[1][1].set(xlabel='Time elapsed (s)', ylabel='Frequency (Hz)')
        pxx, freq, t, cax = ax[1][1].specgram(data[1], Fs=1/T)
        fig.colorbar(cax).set_label('Intensity [dB]')
        plt.savefig(dir_path+'/graphs/'+filename[:-4]+".png")
        plt.show()
    except:
        print("The file doesn't exist")
    return 0
