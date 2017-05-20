import matplotlib.pyplot as plt
import math as th
import numpy as np

def euler_cromer(teta_0, w_0, g, N, delta_t):

    w = w_0
    teta = teta_0
    t = 0

    w_array = []
    dw_dt_array = []
    teta_array = []
    t_array = []
    
    for i in range(N):
        dw_dt = -g * th.sin(teta)
        w = w + dw_dt * delta_t
        teta = teta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        teta_array.append(teta)
        t_array.append(t)

   # plt.plot(t_array, dw_dt_array)
    plt.plot(t_array, w_array)

def euler_richardson(teta_0, w_0, g, N, delta_t):

    w = w_0
    teta = teta_0
    t = 0

    w_array = []
    dw_dt_array = []
    teta_array = []
    t_array = []
    
    for i in range(N):
        
        dw_dt = -g * th.sin(teta)
        w_mid = w + dw_dt * (delta_t/2)
        teta_mid = teta + w * (delta_t/2)
        dw_dt_mid = -g * th.sin(teta_mid)
        
        w = w + dw_dt_mid * delta_t
        teta = teta + w_mid * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        teta_array.append(teta)
        t_array.append(t)

   # plt.plot(t_array, dw_dt_array)
    plt.plot(t_array, w_array)

def main():
    euler_cromer(0.4346, 0, 10, 200, 0.1)
    euler_richardson(0.4346, 0, 10, 200, 0.1)
    plt.show()
main()
