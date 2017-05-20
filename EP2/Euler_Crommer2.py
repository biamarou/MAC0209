import matplotlib.pyplot as plt
import matplotlib.animation as anim
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

fig, ax = plt.subplots()
x = [i*25.0/60 for i in range(60)]
line, = ax.plot(x, [0 for v in x], 'o-b')

def update(frame):
    line.set_ydata([np.sin(frame + v/2.0) for v in x])
    return line,

def main():
    ani = anim.FuncAnimation(fig, update, [i*2*3.1415/200 for i in range(200)],
            interval=20)

    euler_cromer(0.4346, 0, 10, 200, 0.1)
    euler_richardson(0.4346, 0, 10, 200, 0.1)

    plt.show()
main()
