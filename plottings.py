import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fftPackage

def plotDots(x,y):
    x=np.array(x)
    y=np.array(y)
    plt.plot(x,y)

def saveFigs(sum2, name):
    plt.grid()
    if (sum2 != 0):
        plt.savefig('/home/sepehr/Desktop/myProject/figures/' + name)
    else:
        plt.savefig('/home/sepehr/Desktop/myProject/zeroFigures/' + name)
    plt.close()

def saveFigsFFT(sum2, name):
    plt.grid()
    if (sum2 != 0):
        plt.savefig('/home/sepehr/Desktop/myProject/figuresFFT/' + name)
    else:
        plt.savefig('/home/sepehr/Desktop/myProject/zeroFiguresFFT/' + name)
    plt.close()

def pltFFT(yf,xf):
    y=yf[1:len(yf)-1]
    x=xf[1:len(xf)-1]
    plt.plot(x,y)
    plt.show()

def pltiFFT(y, yf,xf,treshhold, format):
    absyf = np.abs(yf)
    index = absyf <= treshhold
    if format=="log":
        np.log(absyf, absyf)

    yf[index]=0
    yPrime= fftPackage.ifft(yf)
    plt.plot(xf, y)
    plt.plot(xf, yPrime)
    plt.show()