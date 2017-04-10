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
    v = [0.0]
    t = [0.0]
    media_tempo = 0
    v_media = 0

    for i in range (len(data_MRU)):
        media_tempo = (float(data_MRU[i][0]) + float(data_MRU[i][1]))/2
        t.append(media_tempo)
        v.append((i+1)*10/media_tempo) 

    print("Tempos", t)    
    print("Velocidades", v)

    for i in range(len(v)):
        v_media += v[i]
    v_media /= 4

    print("Velocidade Média", v_media)

def MRUV (data_MRUV):
#Assim como no MRU, calcula a velocidade em cada intervalo de tempo registrado no experimento,
#e a partir desses dados, calcula a velocidade média. Além disso, calcula a aceleração em cada
#trecho marcado da trajetória e a aceleração média.
    v = [0.0]
    a = [0.0]
    t = [0.0]
    media_tempo = 0
    ac_media = 0
    v_media = 0
    
    for i in range (len(data_MRUV)):
        media_tempo = (float(data_MRUV[i][0]) + float(data_MRUV[i][1]))/2
        t.append(media_tempo)
        v.append((i+1)*10/media_tempo)        
    print("Tempos" ,t)    
    print("Velocidades" ,v)

    for i in range(len(v)):
        v_media += v[i]
    v_media /= 4
    print("Velocidade Média", v_media)

    for i in range (len(data_MRUV)):
        if (t[i] != 0):
            a.append((v[i + 1] - v[i])/(t[i + 1] - t[i]))

        print ("Acelerações", a)

    for i in range(len(a)):
        ac_media += a[i]
    ac_media /= 4

    print("Aceleração Média", ac_media)

main()


