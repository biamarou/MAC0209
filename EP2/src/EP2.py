import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib.lines as mlines
from tkinter import *
import matplotlib.animation as anim
import math as th
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
    FUNÇÕES RELACIONADAS AOS DADOS DO EXPERIMENTO

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def fixer (file, flag) :

    #------------------------------------------------------------------------------------------------------
    # Recebe o nome de um arquivo .csv e 
    # retorna uma lista de listas com os dados prontos para plotar
    # A "flag" decide se o arquivo possui dados do pêndulo ou do MCU
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
        if flag == 'c': # Condicional, dependendo do tipo de csv, pois as posições dos dados variam
            for j in data[0:7]:
                j = j.replace (',', '.')  # Troca as vírgulas por pontos para poder converter os dados em float
                data_aux.append (float (j))
        elif flag == 'p':
            for j in data[0:10]:
                j = j.replace (',', '.')
                data_aux.append (float (j))

        data = data_aux
        content_aux.append (data_aux)

    content = content_aux

    #print (content) # Descomente esta parte para ver o resultado da função, a fim de debugar

    return content




def plotter_pendulum (file_name, radius = .53): 

    #---------------------------------------------------------------------------------------------
    # Plota os dados de um arquivo pendulox.csv
    #---------------------------------------------------------------------------------------------

    # Repara os arquivos, para facilitar a manipulação
    content = fixer (file_name, 'p')

    # Processamento dos dados do experimento
    t = []
    theta_e = []
    a_e = []
    v_e = []

    for data in content:
        t.append (data[0])
        theta_e.append (data[3])
        a_e.append (data[5])
        v_e.append (data[7])

    # Cria subplots para cada grandeza dos dados, a legenda e plota dos dados
    figure = plt.figure (figsize=(20, 8))
    plot1 = figure.add_subplot (131)
    plot2 = figure.add_subplot (132)
    plot3 = figure.add_subplot (133)

    figure.suptitle ("Posição e Velocidade e Aceleração x Tempo - Pêndulo")

    plot1.set_ylabel ("Posição")
    plot1.set_xlabel ("Tempo")
    plot2.set_ylabel ("Velocidade")
    plot2.set_xlabel ("Tempo")
    plot3.set_ylabel ("Aceleração")
    plot3.set_xlabel ("Tempo")

    red = mpatch.Patch (color='red', label='Posição')
    blue = mpatch.Patch (color='blue', label='Aceleração')
    green = mpatch.Patch (color='green', label='Velocidade')
    
    plt.legend (handles=[red, blue, green], bbox_to_anchor=(1, 1), bbox_transform=plt.gcf ().transFigure)

    plot1.plot (t, theta_e, 'r')
    plot2.plot (t, v_e, 'g')
    plot3.plot (t, a_e, 'b')

    plt.savefig (file_name.replace (".csv", "_plot_experiment.png"))
    plt.close (figure)




def plotter_circular (file_name, radius = .48): 

    #---------------------------------------------------------------------------------------------
    # Plota os dados de um arquivo circularx.csv
    #---------------------------------------------------------------------------------------------

    # Repara os arquivos, para facilitar a manipulação
    content = fixer (file_name, 'c')

    # Processamento dos dados do experimento
    t = []
    theta_e = []
    a_e = []
    v_e = []

    last_time = 0
    curr_theta = 0

    for data in content:
        curr_theta += data[6] * (data[0] - last_time)
        last_time = data[0]
        t.append (data[0])
        theta_e.append (curr_theta % th.copysign(2*th.pi, curr_theta))
        a_e.append (data[1] / radius)
        v_e.append (data[6])

    # Cria subplots para cada grandeza dos dados, a legenda e plota dos dados
    figure = plt.figure (figsize=(20, 8))
    plot1 = figure.add_subplot (131)
    plot2 = figure.add_subplot (132)
    plot3 = figure.add_subplot (133)

    figure.suptitle ("Posição e Velocidade e Aceleração x Tempo - MCU")

    plot1.set_ylabel ("Posição")
    plot1.set_xlabel ("Tempo")
    plot2.set_ylabel ("Velocidade")
    plot2.set_xlabel ("Tempo")
    plot3.set_ylabel ("Aceleração")
    plot3.set_xlabel ("Tempo")

    red = mpatch.Patch (color='red', label='Posição')
    blue = mpatch.Patch (color='blue', label='Aceleração')
    green = mpatch.Patch (color='green', label='Velocidade')
    
    plt.legend (handles=[red, blue, green], bbox_to_anchor=(1, 1), bbox_transform=plt.gcf ().transFigure)

    plot1.plot (t, theta_e, 'r')
    plot2.plot (t, v_e, 'g')
    plot3.plot (t, a_e, 'b')

    plt.savefig (file_name.replace (".csv", "_plot_experiment.png"))
    plt.close (figure)

def plotter_all_experiment ():

    #-----------------------------------------------------------------------------------------------------
    # Plota todos os arquivos .csv, salvando-os no diretório atual
    #-----------------------------------------------------------------------------------------------------

    plotter_pendulum ("pendulo1.csv")
    plotter_pendulum ("pendulo2.csv")
    plotter_pendulum ("pendulo3.csv")
    plotter_pendulum ("pendulo4.csv")
    plotter_pendulum ("pendulo5.csv")

    plotter_circular ("circular1.csv")
    plotter_circular ("circular2.csv")
    plotter_circular ("circular3.csv")
    plotter_circular ("circular4.csv")
    plotter_circular ("circular5.csv")




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    FUNÇÕES RELACIONADAS ÀS SIMULAÇÕES

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def euler_cromer_pendulum(theta_0, w_0, g, N, delta_t, air_res, radius=.53):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):
        linacc = -g * th.sin(theta) - air_res * w 
        dw_dt = linacc / radius
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Plotar os dados aceleração, velocidade e posição, respectivamente.
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_title('Euler Cromer - Pêndulo')
    ax.plot(t_array, dw_dt_array, label='Angular Acceleration(rad/s²)')
    ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    ax.legend(loc='lower right', prop={'size': 6})

    plt.savefig ("pendulo_cromer_simulado.png")
    plt.close (fig)

    return t_array, theta_array




def euler_richardson_pendulum(theta_0, w_0, g, N, delta_t, air_res, radius=.53):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):

        linacc = -g * th.sin(theta) - air_res * w
        dw_dt = linacc/radius
        w_mid = w + dw_dt * (delta_t/2)
        theta_mid = theta + w * (delta_t/2)
        linacc_2 = -g * th.sin(theta_mid) - air_res * w_mid
        dw_dt_mid = linacc_2/radius
        w = w + dw_dt_mid * delta_t
        theta = theta + w_mid * delta_t
        t = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Plotar os dados aceleração, velocidade e posição, respectivamente.
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_title('Euler Richardson - Pêndulo')
    ax.plot(t_array, dw_dt_array, label='Angular Acceleration(rad/s²)')
    ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    ax.legend(loc='lower right', prop={'size': 6})
    
    plt.savefig ("pendulo_richardson_simulado.png")
    plt.close (fig)

    return t_array, theta_array




def euler_cromer_MCU (theta_0, w_0, N, delta_t):

    w = w_0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
    theta_array = []
    theta_cont = []
    t_array = []

    for i in range(N):
        dw_dt = 0
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta % th.copysign(2*th.pi, theta))
        theta_cont.append(theta)
        t_array.append(t)

    # Para plotar a o ângulo e plotar a velocidade.
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_title('Euler Cromer - MCU')
    ax.plot(t_array, dw_dt_array, label='Angular Acceleration(rad/s²)')
    ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    ax.legend(loc='lower right', prop={'size': 6})

    plt.savefig ("circular_cromer_simulado.png")
    plt.close (fig)

    return t_array, theta_cont




def euler_richardson_MCU (theta_0, w_0, N, delta_t):

    w = w_0
    dw_dt = 0
    theta = theta_0
    t = 0

    w_array = []
    dw_dt_array = []
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
        
        dw_dt_array. append(dw_dt)
        w_array.append(w)
        theta_array.append(theta % th.copysign(2*th.pi, theta))
        theta_cont.append(theta)
        t_array.append(t)
        
    # Para plotar a variação do ângulo e plotar a velocidade.
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_title('Euler Richardson - MCU')
    ax.plot(t_array, dw_dt_array, label='Angular Acceleration(rad/s²)')
    ax.plot(t_array, w_array, label='Angular Velocity(rad/s)')
    ax.plot(t_array, theta_array, label='Angular Variation(rad)')
    ax.legend(loc='lower right', prop={'size': 6})
    
    plt.savefig ("circular_richardson_simulado.png")
    plt.close (fig)

    return t_array, theta_cont




def plotter_all_simulation ():

    #-----------------------------------------------------------------------------------------------------
    # Plota os gráficos de todas simulações, salvando-os no diretório atual
    # OBS: os dados de retorno das funções são ignorados
    #-----------------------------------------------------------------------------------------------------

    trash1 = euler_cromer_pendulum (0.4, 0, 10, 1500, 0.01, 0)
    trash2 = euler_richardson_pendulum (0.4, 0, 10, 1500, 0.01, 0)
    trash3 = euler_cromer_MCU (0, -9, 350, 0.1)
    trash4 = euler_richardson_MCU (0, -9, 350, 0.1)




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    FUNÇÕES RELACIONADAS À SOBREPOSIÇÃO DOS GRÁFICOS DOS EXPERIMENTOS E DAS SIMULAÇÕES (APENAS CROMER)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def plotter_pendulum_comparison (file_name, theta_0, w_0, g, N, delta_t,
        air_res, init_offset, radius = .53): 

    #---------------------------------------------------------------------------------------------
    # Plota os dados de um arquivo pendulox.csv juntamente com sua simulação
    #---------------------------------------------------------------------------------------------

    # Repara os arquivos, para facilitar a manipulação
    content = fixer (file_name, 'p')

    # Processamento dos dados do experimento e da simulação
    t_e = []
    theta_e = []
    a_e = []
    v_e = []

    for data in content:
        t_e.append (data[0] + init_offset)
        ang_pos = th.atan(data[3]/data[2])
        theta_e.append (ang_pos)
        a_e.append (data[6] / radius)
        v_e.append (data[7])

    w = w_0
    theta = theta_0
    t = 5 # Protocolo do experimento (5 segundos de espera)

    w_array = []
    dw_dt_array = []
    theta_array = []
    t_array = []

    for i in range(N):
        linacc = -g * th.sin(theta) - air_res * w
        dw_dt = linacc / radius
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta)
        t_array.append(t)

    # Cria subplots para cada grandeza dos dados, a legenda e plota dos dados
    figure = plt.figure (figsize=(20, 8))
    plot1 = figure.add_subplot (131)
    plot2 = figure.add_subplot (132)
    plot3 = figure.add_subplot (133)

    figure.suptitle ("Posição e Velocidade e Aceleração x Tempo - Pêndulo (Simulação vs Experimento)")

    plot1.set_ylabel ("Posição")
    plot1.set_xlabel ("Tempo")
    plot2.set_ylabel ("Velocidade")
    plot2.set_xlabel ("Tempo")
    plot3.set_ylabel ("Aceleração")
    plot3.set_xlabel ("Tempo")

    red = mpatch.Patch (color='red', label='Posição')
    blue = mpatch.Patch (color='blue', label='Aceleração')
    green = mpatch.Patch (color='green', label='Velocidade')
    line1 = mlines.Line2D([], [], color='black', marker='_', label='Experimento (Colorido)')
    line2 = mlines.Line2D([], [], color='black', marker='_', label='Simulado (Preto)')
    
    plt.legend (handles=[red, blue, green, line1, line2], bbox_to_anchor=(1, 1), bbox_transform=plt.gcf ().transFigure)

    plot1.plot (t_e, theta_e, 'r', t_array, theta_array, 'k')
    plot2.plot (t_e, v_e, 'g', t_array, w_array, 'k')
    plot3.plot (t_e, a_e, 'b', t_array, dw_dt_array, 'k')

    plt.savefig (file_name.replace (".csv", "_plot_comparison.png"))
    plt.close (figure)




def plotter_circular_comparison (file_name, theta_0, w_0, N, delta_t, radius = .48): 

    #---------------------------------------------------------------------------------------------
    # Plota os dados de um arquivo circularx.csv juntamente com sua simulação
    #---------------------------------------------------------------------------------------------

    # Repara os arquivos, para facilitar a manipulação
    content = fixer (file_name, 'c')

    # Processamento dos dados do experimento e da simulação
    t_e = []
    theta_e = []
    a_e = []
    v_e = []

    curr_theta = 0
    last_time = 0

    for data in content:
        curr_theta += data[6] * (data[0] - last_time)
        last_time = data[0]
        t_e.append (data[0])
        theta_e.append (curr_theta % th.copysign(2*th.pi, curr_theta))
        a_e.append (data[1] / radius)
        v_e.append (data[6])

    w = w_0
    theta = theta_0
    t = 5 # Protocolo do experimento (5 segundos de espera)

    w_array = []
    dw_dt_array = []
    theta_array = []
    theta_cont = []
    t_array = []

    for i in range(N):
        dw_dt = 0
        w = w + dw_dt * delta_t
        theta = theta + w * delta_t
        t  = t + delta_t

        w_array.append(w)
        dw_dt_array.append(dw_dt)
        theta_array.append(theta % th.copysign(2*th.pi, theta))
        theta_cont.append(theta)
        t_array.append(t)

    # Cria subplots para cada grandeza dos dados, a legenda e plota dos dados
    figure = plt.figure (figsize=(20, 8))
    plot1 = figure.add_subplot (131)
    plot2 = figure.add_subplot (132)
    plot3 = figure.add_subplot (133)

    figure.suptitle ("Posição e Velocidade e Aceleração x Tempo - MCU (Simulação vs Experimento)")

    plot1.set_ylabel ("Posição")
    plot1.set_xlabel ("Tempo")
    plot2.set_ylabel ("Velocidade")
    plot2.set_xlabel ("Tempo")
    plot3.set_ylabel ("Aceleração")
    plot3.set_xlabel ("Tempo")

    red = mpatch.Patch (color='red', label='Posição')
    blue = mpatch.Patch (color='blue', label='Aceleração')
    green = mpatch.Patch (color='green', label='Velocidade')
    line1 = mlines.Line2D([], [], color='black', marker='_', label='Experimento (Colorido)')
    line2 = mlines.Line2D([], [], color='black', marker='_', label='Simulado (Preto)')

    plt.legend (handles=[red, blue, green, line1, line2], bbox_to_anchor=(1, 1), bbox_transform=plt.gcf ().transFigure)

    plot1.plot (t_e, theta_e, 'r', t_array, theta_array, 'k')
    plot2.plot (t_e, v_e, 'g', t_array, w_array, 'k')
    plot3.plot (t_e, a_e, 'b', t_array, dw_dt_array, 'k')

    plt.savefig (file_name.replace (".csv", "_plot_comparison.png"))
    plt.close (figure)




def plotter_all_overlap ():

    #-----------------------------------------------------------------------------------------------------
    # Plota os gráficos dos experimentos sobrepostos com os gráficos das simulações,
    # salvando-os no diretório atual
    # OBS: os dados de retorno das funções são ignorados
    #----------------------------------------------------------------------------------------------------

    init_ang = 0.4
    air_fric = .04

    plotter_pendulum_comparison ("pendulo1.csv", init_ang, 0, 10, 1500, 0.01,
            air_fric, -0.5)
    plotter_pendulum_comparison ("pendulo2.csv", init_ang, 0, 10, 1500, 0.01,
            air_fric, 0)
    plotter_pendulum_comparison ("pendulo3.csv", init_ang, 0, 10, 1500, 0.01,
            air_fric, 0)
    plotter_pendulum_comparison ("pendulo4.csv", init_ang, 0, 10, 1500, 0.01,
            air_fric, -0.53)
    plotter_pendulum_comparison ("pendulo5.csv", init_ang, 0, 10, 1500, 0.01,
            air_fric, -0.52)

    ang_vel = -9.0

    plotter_circular_comparison ("circular1.csv", 0, ang_vel, 350, 0.1)
    plotter_circular_comparison ("circular2.csv", 0, ang_vel, 350, 0.1)
    plotter_circular_comparison ("circular3.csv", 0, ang_vel, 350, 0.1)
    plotter_circular_comparison ("circular4.csv", 0, ang_vel, 350, 0.1)
    plotter_circular_comparison ("circular5.csv", 0, ang_vel, 350, 0.1)




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    ANIMAÇÕES DAS SIMULAÇÕES

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#-----------------------------------------------------------------------------------------------------
# Animação do pêndulo
#
# Retorna (x, y) do pêndulo em um instante dado um vetor de tempo e um de
# ângulos. Interpola o ângulo linearmente
#-----------------------------------------------------------------------------------------------------
def getpos_pendulum(time, t_array, theta_array, ceil = .5, pend_len = 0.38, pend_x = .25):
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
    rx, ry, x, y, theta = getpos_pendulum(time, t_array, theta_array)
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




def update_graph_pendulum(time, line, ax, t_array, theta_array):
    rx, ry, x, y, theta = getpos_pendulum(time, t_array, theta_array)
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




def animate_graph_pendulum(time_angle, fig, ax, col = 'b', fps = 60):
    t_array, theta_array = time_angle
    frame_qty = th.floor(fps*t_array[-1])
    frame_time = [i*t_array[-1]/frame_qty for i in range(frame_qty)]

    line, = ax.plot([0], [0], '-' + col)

    ani = anim.FuncAnimation(fig, update_graph_pendulum, frame_time, fargs = (line,
        ax, t_array, theta_array),
            interval = th.floor(1000.0/fps))
    return ani




def pendulum_animator ():

    #-----------------------------------------------------------------------------------------------------
    # Simula o pêndulo utilizando animações gráficas
    #-----------------------------------------------------------------------------------------------------

    cromer = euler_cromer_pendulum (0.4, 0, 10, 1500, 0.01, 0)
    richard = euler_richardson_pendulum (0.4, 0, 10, 1500, 0.01, 0)

    # Pêndulo e gráfico
    fig = plt.figure()
    ax = plt.subplot(211)
    ax.axis('scaled')
    ax.axis([0, .5, 0, .5])
    ani_cromer_p = animate_pendulum(cromer, fig, ax, 'b')
    ani_richard_p = animate_pendulum(richard, fig, ax, 'r')
    ax2 = plt.subplot(212)
    ani_cromer_g = animate_graph_pendulum(cromer, fig, ax2, 'b')
    ani_richard_g = animate_graph_pendulum(richard, fig, ax2, 'r')

    plt.show()



#-----------------------------------------------------------------------------------------------------
# Animação do MCU
#
# Retorna (x, y) do MCU em um instante dado um vetor de tempo e um de
# ângulos. Interpola o ângulo linearmente
#-----------------------------------------------------------------------------------------------------

def getpos_MCU (time, t_array, theta_array, fan_radius =.48):
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




def update_MCU (time, line, pendulum, ax, t_array, theta_array):
    rx, ry, x, y = getpos_MCU(time, t_array, theta_array)
    pendulum.set_data([x], [y])
    line.set_data([rx, x], [ry, y])
    plt.xlabel(str(round(time, 2)))
    return pendulum,




def animate_MCU (time_angle, fig, ax, col = 'b', fps = 60):
    t_array, theta_array = time_angle
    frame_qty = th.floor(fps*t_array[-1])
    frame_time = [i*t_array[-1]/frame_qty for i in range(frame_qty)]

    line, = ax.plot([0], [0], '-k')
    pendulum, = ax.plot([0], [0], 'o' + col)
    ax.axis('scaled')
    ax.axis([-1, 1, -1, 1])

    ani = anim.FuncAnimation(fig, update_MCU, frame_time, fargs = (line, pendulum,
        ax, t_array, theta_array), interval = th.floor(1000.0/fps))
    return ani




def circular_animator ():

    #-----------------------------------------------------------------------------------------------------
    # Simula o MCU utilizando animações gráficas
    #-----------------------------------------------------------------------------------------------------

    cromer = euler_cromer_MCU (0, -9, 350, 0.1)
    richard = euler_richardson_MCU (0, -9, 350, 0.1)

    fig, ax = plt.subplots()
    ani_cromer = animate_MCU(cromer, fig, ax, 'b')
    ani_richard = animate_MCU(richard, fig, ax, 'r')

    plt.show()





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    MAIN

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main_GUI ():
    
    #-----------------------------------------------------------------------------------------------------
    # Interface gráfica para as plotagens, usando tkinter.
    # Todos os gráficos plotados são salvados no diretório atual
    #-----------------------------------------------------------------------------------------------------

    window = Tk ()
    window.title ("EP2 - MAC0209")


    infoL = Label (window, text="O que deseja fazer?")
    button1 = Button (window, text="Plotar os gráficos dos experimentos realizados", command= plotter_all_experiment) 
    button2 = Button (window, text="Plotar os gráficos das simulações", command= plotter_all_simulation) 
    button3 = Button (window, text="Plotar os gráficos dos experimentos realizados sobrepostos com a simulação", command= plotter_all_overlap)
    button4 = Button (window, text="Simular o pêndulo com animações", command= pendulum_animator) 
    button5 = Button (window, text="Simular o MCU com animações", command= circular_animator) 
    

    infoL.pack ()
    button1.pack ()
    button2.pack ()
    button3.pack ()
    button4.pack ()
    button5.pack ()

    window.mainloop ()

main_GUI ()
