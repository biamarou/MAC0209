import sys

def main ():
    #Recebe arquivo de texto com dados do experimento numa matriz 6x7, na qual a primeira coluna indica se o movimento
    #é MRU(indicado por '0') ou MRUV (indicado por '1'). 

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        raise Exception ("No file found.")

    line = " "

    with open(input_file, "r+") as f:
        count_MRU = 1
        count_MRUV = 1
        while(1):
            data_MRU = []
            data_MRUV = []
            line = f.readline()
            if (line == ''):
                break
            line = line.split()

            if (line[0] == '0'):
                data_MRU.append(line[1:3])
                data_MRU.append(line[3:5])
                data_MRU.append(line[5:7])
                print("Teste " + str(count_MRU) + " MRU")
                count_MRU += 1
                MRU(data_MRU)
            else:
                data_MRUV.append(line[1:3])
                data_MRUV.append(line[3:5])
                data_MRUV.append(line[5:7])
                print("Teste " + str(count_MRUV) + " MRUV")
                count_MRUV += 1
                MRUV(data_MRUV)

def MRU (data_MRU):
#Calcula a velocidade em cada intervalo de tempo registrado no experimento,
#e a partir desses dados, calcula a velocidade média.
    v = []
    t = []

    for i in range (len(data_MRU)):
        dt = (float(data_MRU[i][0]) + float(data_MRU[i][1]))/2
        if i > 0:
            dt -= (float(data_MRU[i - 1][0]) + float(data_MRU[i - 1][1]))/2

        t.append(dt)
        v.append(10/dt)

    print("Delta times", t)
    print("Velocidades", v)

    print("Velocidade Média", sum(v)/len(v))
    return t, v

def MRUV (data_MRUV):
#Assim como no MRU, calcula a velocidade em cada intervalo de tempo registrado no experimento,
#e a partir desses dados, calcula a velocidade média. Além disso, calcula a aceleração em cada
#trecho marcado da trajetória e a aceleração média.
    t, v = MRU(data_MRUV)
    a = []

    for i in range (len(data_MRUV)):
        dt = t[i]
        dv = v[i]
        if i > 0:
            dv -= v[i - 1]
        a.append(dv/dt)

    print ("Acelerações", a)

    print("Aceleração Média", sum(a)/len(a))
    return t, v, a

main()


