import matplotlib.pyplot as plt
import numpy as np
import math

def SHO_euler (N,XO,VO):
    
    xE = XO
    vE = VO
    tE = 0
    detE = 0.1

    dsE = []
    dtE = []

    x = XO
    v = VO
    t = 0
    det = 0.1

    ds = []
    dt = []

    error = []
    
    for i in np.arange(N):
        xE = xE + v*detE
        vE = vE - x*detE
        tE = tE + detE

        v = v - x*det
        x = x + v*det
        t = t + det
        
        dsE.append(xE)
        dtE.append(tE)
        
        ds.append(x)
        dt.append(t)

        error.append(math.fabs(xE - x))

    plt.plot(dt, ds)
    plt.plot(dtE, dsE)
    plt.plot(dt, error)

def main():

    SHO_euler(100, 10, 0)
    plt.show()
main()
