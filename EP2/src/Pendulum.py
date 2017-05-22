import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.patches as mpatch
import math as th
import numpy as np


def fixer (file) :

    #------------------------------------------------------------------------------------------------------
    # Recebe o nome de um arquivo .csv e 
    # retorna uma lista de listas com os dados prontos para plotar
    #------------------------------------------------------------------------------------------------------

    content = []

    # Abre o arquivo e ignora newlines, guardando o conteúdo em uma lista de listas
    with open (file) as f:
        content = f.read ().splitlines ()
        content_aux = []    

    for i in content:

        data = i.split (';') # Separa os dados
        data_aux = []

        # Ignora o "vácuo (ponto-e-vírgula que não deveria ter)" do final
        for j in data[0:7]:
            j = j.replace (',', '.')  # Troca as vírgulas por pontos para poder converter os dados em float
            data_aux.append (float (j))

        data = data_aux
        content_aux.append (data_aux)

    content = content_aux

    #print (content) # Descomente esta parte para ver o resultado da função, a fim de debugar

    return content

def plotter (file_name): 

    #---------------------------------------------------------------------------------------------
    # Plota os dados do arquivo .csv
    #---------------------------------------------------------------------------------------------

    # Repara os arquivos, para facilitar a manipulação
    content = fixer (file_name)

    figure = plt.figure ()
    plot = figure.add_subplot (111)

    plot.set_title ("Posição e Velocidade e Aceleração x Tempo")
    plot.set_ylabel ("Posição e Velocidade e Aceleração")
    plot.set_xlabel ("Tempo")

    red = mpatch.Patch (color='red', label='Posição')
j    blue = mpatch.Patch (color='blue', label='Aceleração')
    green = mpatch.Patch (color='green', label='Velocidade')
    
    plt.legend (handles=[red, blue, green], bbox_to_anchor=(1, 1), bbox_transform=plt.gcf ().transFigure)

    t = []
    theta_e = []
    a_e = []
    v_e = []

    for data in content:
        t.append (data[0])
        theta_e.append (sin (data[0] * data[6]) * 2 * pi)
        a_e.append (data[2])
        v_e.append (data[6])

    plot.plot (t, theta_e, 'r', t, a_e, 'b', t, v_e, 'g')

    plt.savefig (file_name.replace (".csv", "_plot.png"))
    euler_cromer (0.4346, 0, 10, 1000, 0.01, 0)
    plt.show ()


def main_GUI ():
    
    #-----------------------------------------------------------------------------------------------------
    # Interface gráfica para as plotagens. A entrada é o nome de um arquivo .csv
    #-----------------------------------------------------------------------------------------------------

    window = Tk ()
    window.title ("Plotter - Circular")

    infoL = Label (window, text="Nome do arquivo:")
    info = Entry (window, bd=10)

    button = Button (window, text="Open", command= lambda: plotter (info.get ()))

    infoL.pack ()
    info.pack ()
    button.pack ()

    window.mainloop ()

main_GUI ()

def euler_cromer(theta_0, w_0, g, N, delta_t, air_res):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):
        dw_dt = -g * th.sin(theta) - air_res * w 
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Descomentar para plotar os dados aceleração, velocidade e posição, respectivamente.
    fig, ax = plt.subplots()
    ax.set_title('Euler Cromer')
    ax.plot(t_array, dw_dt_array, label='Acceleration(m/s²)')
    ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    ax.legend(loc='lower right', prop={'size': 6})
    return t_array, theta_array

def euler_richardson(theta_0, w_0, g, N, delta_t, air_res):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):

        dw_dt = -g * th.sin(theta) - air_res * w
        w_mid = w + dw_dt * (delta_t/2)
        theta_mid = theta + w * (delta_t/2)
        dw_dt_mid = -g * th.sin(theta_mid) - air_res * w_mid

        w = w + dw_dt_mid * delta_t
        theta = theta + w_mid * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Descomentar para plotar os dados aceleração, velocidade e posição, respectivamente.
    #fig, ax = plt.subplots()
    #ax.set_title('Euler Richardson')
    #ax.plot(t_array, dw_dt_array, label='Acceleration(m/s²)')
    #ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    #ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    #ax.legend(loc='lower right', prop={'size': 6})
    
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
    # <coeficiente de resistência>
    #)

    cromer = euler_cromer(0.4346, 0, 10, 1000, 0.01, 0)
    richard = euler_richardson(0.4346, 0, 10, 1000, 0.01, 0)

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
    #ax.axis([0, .5, 0, .5])
    #ani_cromer_p = animate_pendulum(cromer, fig, ax, 'b')
    #ani_richard_p = animate_pendulum(richard, fig, ax, 'r')
    
    # Descomentar para visualizar os gráficos ou animações.
    plt.show()
main()
