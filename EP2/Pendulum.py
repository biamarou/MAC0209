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
        
   # Descomentar para plotar os dados aceleração e velocidade, respectivamente.
   # plt.plot(t_array, dw_dt_array)
   # plt.plot(t_array, w_array)

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

   # Descomentar para plotar os dados aceleração e velocidade, respectivamente.
   # plt.plot(t_array, dw_dt_array)
   # plt.plot(t_array, w_array)

def main():

    #Considerei o ângulo inicial como 0.4346rad, aproximou bem com os dados que a gente coletou. E é uma abertura bem plausível(24.9°).
    #Argumentos: método(<ângulo inicial(rad)>, <velocidade angular inicial(rad/s)>, <gravidade(m/s²)>, <número de iterações>, <intervalo de tempo(s)>).

    euler_cromer(0.4346, 0, 10, 200, 0.1)
    euler_richardson(0.4346, 0, 10, 200, 0.1)
    
    # Descomentar para visualizar os gráficos.
    # plt.show()

main()
