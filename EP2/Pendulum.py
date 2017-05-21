import matplotlib.pyplot as plt
import matplotlib.animation as anim
import math as th
import numpy as np

def euler_cromer(theta_0, w_0, g, N, delta_t):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):
        dw_dt = -g * th.sin(theta)
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Descomentar para plotar os dados aceleração, velocidade e posição, respectivamente.
    #plt.plot(t_array, dw_dt_array)
    #plt.plot(t_array, w_array)
    #plt.plot(t_array, theta_array)
    return t_array, theta_array

def euler_richardson(theta_0, w_0, g, N, delta_t):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):

        dw_dt = -g * th.sin(theta)
        w_mid = w + dw_dt * (delta_t/2)
        theta_mid = theta + w * (delta_t/2)
        dw_dt_mid = -g * th.sin(theta_mid)

        w = w + dw_dt_mid * delta_t
        theta = theta + w_mid * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Descomentar para plotar os dados aceleração, velocidade e posição, respectivamente.
    #plt.plot(t_array, dw_dt_array)
    #plt.plot(t_array, w_array)
    #plt.plot(t_array, theta_array)
    return t_array, theta_array

# Animação do pêndulo

# Retorna (x, y) do pêndulo em um instante dado um vetor de tempo e um de
# ângulos. Interpola o ângulo linearmente
def getpos(time, t_array, theta_array, ceil = .5, pend_len = 0.38, pend_x = .25):
    x = 0
    y = 0
    k = -1
    for i in range(len(t_array) - 1):
        if t_array[i + 1] > time:
            k = i
            break

    frac = (time - t_array[k])/(t_array[k + 1] - t_array[k])
    theta = theta_array[k + 1]*frac + theta_array[k]*(1 - frac)

    x = pend_x + pend_len*th.sin(theta)
    y = ceil - pend_len*th.cos(theta)
    rx = pend_x
    ry = ceil
    return  rx, ry, x, y, theta

def update_pendulum(time, line, pendulum, ax, t_array, theta_array):
    rx, ry, x, y, theta = getpos(time, t_array, theta_array)
    pendulum.set_data([x], [y])
    line.set_data([rx, x], [ry, y])
    ax.set_ylabel(str(round(time, 2)))

def animate_pendulum(time_angle, fig, ax, col = 'b', fps = 60):
    t_array, theta_array = time_angle
    frame_qty = th.floor(fps*t_array[-1])
    frame_time = [i*t_array[-1]/frame_qty for i in range(frame_qty)]

    line, = ax.plot([0], [0], '-k')
    pendulum, = ax.plot([0], [0], 'o' + col)

    ani = anim.FuncAnimation(fig, update_pendulum, frame_time, fargs = (line, pendulum,
        ax, t_array, theta_array),
            interval = th.floor(1000.0/fps))
    return ani

def update_graph(time, line, ax, t_array, theta_array):
    rx, ry, x, y, theta = getpos(time, t_array, theta_array)
    t_new = []
    theta_new = []

    for i in range(len(t_array)):
        if t_array[i] > time:
            break
        t_new.append(t_array[i])
        theta_new.append(theta_array[i])

    t_new.append(time)
    theta_new.append(theta)

    ax.relim()
    ax.autoscale_view()

    line.set_data(t_new, theta_new)

def animate_graph(time_angle, fig, ax, col = 'b', fps = 60):
    t_array, theta_array = time_angle
    frame_qty = th.floor(fps*t_array[-1])
    frame_time = [i*t_array[-1]/frame_qty for i in range(frame_qty)]

    line, = ax.plot([0], [0], '-' + col)

    ani = anim.FuncAnimation(fig, update_graph, frame_time, fargs = (line,
        ax, t_array, theta_array),
            interval = th.floor(1000.0/fps))
    return ani

# Main
def main():

    # Considerei o ângulo inicial como 0.4346rad, pois aproximou bem com os
    # dados que a gente coletou, e é uma abertura bem plausível(24.9°).

    # Argumentos:
    # método(
    # <ângulo inicial(rad)>,
    # <velocidade angular inicial(rad/s)>,
    # <gravidade(m/s²)>,
    # <número de iterações>,
    # <intervalo de tempo(s)>
    #)

    cromer = euler_cromer(0.4346, 0, 10, 200, 0.1)
    richard = euler_richardson(0.4346, 0, 10, 200, 0.1)

    # Descomentar para visualizar a animação.

    # Pêndulo e gráfico
    fig = plt.figure()
    ax = plt.subplot(211)
    ax.axis('scaled')
    ax.axis([0, .5, 0, .5])
    ani_cromer_p = animate_pendulum(cromer, fig, ax, 'b')
    ani_richard_p = animate_pendulum(richard, fig, ax, 'r')
    ax2 = plt.subplot(212)
    ani_cromer_g = animate_graph(cromer, fig, ax2, 'b')
    ani_richard_g = animate_graph(richard, fig, ax2, 'r')
    
    # Só pêndulo
    #fig, ax = plt.subplots()
    #ax.axis('scaled')
    #ax.axis([0, 5, 0, 5])
    #ani_cromer_p = animate_pendulum(cromer, fig, ax, 'b')
    #ani_richard_p = animate_pendulum(richard, fig, ax, 'r')
    
    # Descomentar para visualizar os gráficos ou animações.
    plt.show()
main()
