import matplotlib.pyplot as plt
import matplotlib.animation as anim
import math as th
import numpy as np

def euler_cromer(theta_0, w_0, N, delta_t):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    theta_array = []
    theta_cont = []
    t_array = []

    for i in range(N):
        dw_dt = 0
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        theta_array.append(theta % th.copysign(2*th.pi, theta))
        theta_cont.append(theta)
        t_array.append(t)

    # Descomentar para plotar a o ângulo e plotar a velocidade.
    #plt.plot(t_array, theta_array)
    #plt.plot(t_array, w_array)

    return t_array, theta_cont

def euler_richardson(theta_0, w_0, N, delta_t):

    w = w_0
    dw_dt = 0
    theta = theta_0
    t = 0

    w_array = []
    theta_array = []
    theta_cont = []
    t_array = []

    for i in range(N):

        # A aceleração tem módulo 0, pois o módulo da velocidade não se altera.

        w_mid = w + dw_dt * (delta_t/2)
        theta_mid = theta + w * (delta_t/2)
        dw_dt_mid = dw_dt

        w = w + dw_dt_mid * delta_t
        theta = theta + w_mid * delta_t

        t  = t + delta_t

        w_array.append(w)
        theta_array.append(theta % th.copysign(2*th.pi, theta))
        theta_cont.append(theta)
        t_array.append(t)
    # Descomentar para plotar a variação do ângulo e plotar a velocidade.
    #plt.plot(t_array, theta_array, 'y-.')
    #plt.plot(t_array, w_array)

    return t_array, theta_cont

# Animação do ventilador

# Retorna (x, y) do pêndulo em um instante dado um vetor de tempo e um de
# ângulos. Interpola por mais próximo
def getpos(time, t_array, theta_array, fan_radius = 3):
    x = 0
    y = 0
    k = -1
    for i in range(len(t_array) - 1):
        if t_array[i + 1] > time:
            k = i
            break

    frac = (time - t_array[k])/(t_array[k + 1] - t_array[k])
    theta = theta_array[k + 1]*frac + theta_array[k]*(1 - frac)

    x = fan_radius*th.sin(theta)
    y = fan_radius*th.cos(theta)
    rx = 0
    ry = 0
    return  rx, ry, x, y

def update(time, line, pendulum, ax, t_array, theta_array):
    rx, ry, x, y = getpos(time, t_array, theta_array)
    pendulum.set_data([x], [y])
    line.set_data([rx, x], [ry, y])
    plt.xlabel(str(round(time, 2)))
    return pendulum,

def animate(time_angle, fig, ax, col = 'b', fps = 60):
    t_array, theta_array = time_angle
    frame_qty = th.floor(fps*t_array[-1])
    frame_time = [i*t_array[-1]/frame_qty for i in range(frame_qty)]

    line, = ax.plot([0], [0], '-k')
    pendulum, = ax.plot([0], [0], 'o' + col)
    ax.axis('scaled')
    ax.axis([-5, 5, -5, 5])

    ani = anim.FuncAnimation(fig, update, frame_time, fargs = (line, pendulum,
        ax, t_array, theta_array), interval = th.floor(1000.0/fps))
    return ani

def main():
    # Velocidade angular inicial coletada do experimento.

    # Argumentos:
    # método(
    # <ângulo inicial(rad)>,
    # <velocidade angular inicial(rad/s)>,
    # <número de iterações>,
    # <intervalo de tempo(s)>
    #)

    cromer = euler_cromer(0, -8.9942, 200, 0.1)
    richard = euler_richardson(0, -8.9942, 200, 0.1)

    # Descomentar para visualizar os gráficos.
    #plt.show()

    # Descomentar para visualizar a animação.
    fig, ax = plt.subplots()
    ani_cromer = animate(cromer, fig, ax, 'b')
    ani_richard = animate(richard, fig, ax, 'r')
    plt.show()


main()
