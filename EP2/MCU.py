import matplotlib.pyplot as plt
import math as th
import numpy as np

def euler_cromer(teta_0, w_0, N, delta_t):

    w = w_0
    teta = teta_0
    t = 0

    w_array = []
    teta_array = []
    t_array = []
    
    for i in range(N):
        dw_dt = 0
        w = w + dw_dt * delta_t
        teta = teta + w * delta_t
        if (teta <= -2*th.pi):
            teta = 0
        t  = t + delta_t

        w_array.append(w)
        teta_array.append(teta)
        t_array.append(t)
        
   # Descomentar para plotar a variação do ângulo e plotar a velocidade. 
   # plt.plot(t_array, teta_array)
   # plt.plot(t_array, w_array)
    
def euler_richardson(teta_0, w_0, N, delta_t):

    w = w_0
    dw_dt = 0
    teta = teta_0
    t = 0

    w_array = []
    teta_array = []
    t_array = []
    
    for i in range(N):
        
        # A aceleração tem módulo 0, pois o módulo da velocidade não se altera.
        
        w_mid = w + dw_dt * (delta_t/2)
        teta_mid = teta + w * (delta_t/2)
        dw_dt_mid = dw_dt
        
        w = w + dw_dt_mid * delta_t
        teta = teta + w_mid * delta_t
        if (teta < -2*th.pi):
            teta = 0
        t  = t + delta_t

        w_array.append(w)
        teta_array.append(teta)
        t_array.append(t)

    plt.plot(t_array, teta_array, 'y-.')
   # plt.plot(t_array, w_array)

def main():
    # Velocidade angular inicial coletada do experimento.
    # Argumentos (<ângulo inicial(rad)>, <velocidade angular inicial(rad/s)>, <número de iterações>, <intervalo de tempo(s)>)
    euler_cromer(0, -8.9942, 200, 0.1)
    euler_richardson(0, -8.9942, 200, 0.1)
    plt.show()

main()
