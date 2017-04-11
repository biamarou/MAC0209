import matplotlib.pyplot as plt

def fixer (file) :

    #-------------------------------------------------------------------------------------------------------------
    # Recebe o nome de um arquivo _repaired.csv e retorna uma lista de listas com os dados prontos para plotar
    #-------------------------------------------------------------------------------------------------------------

    content = []

    with open (file) as f:    #Abre o arquivo e ignora newlines, guardando o conteúdo em uma lista de listas
        content = f.read ().splitlines ()
        content_aux = []    

    for i in content:

        data = i.split (';') #Separa os dados
        data_aux = []

        for j in data:
            j = j.replace (',', '.')    #Troca as vírgulas por pontos para poder converter os dados em float
            data_aux.append (float (j))

        data = data_aux
        content_aux.append (data_aux)

    content = content_aux

   # print (content) # Descomente esta parte para ver o resultado da função =)

    return content


def main ():

    data = []
    data =  fixer ("Bia correndo 1.csv") # Descomente para testar
    k = 7
    for i in range (len(data) - 1):
        plt.plot([data[i][0], data[i + 1][0]], [data[i][2],data[i + 1][2]], 'r-')
        
    t = [0.0, 4.84, 6.35, 8.05]
    v = [0.0, 2.54, 3.35, 3.93]
    plt.plot([t[0] + k, t[1] + k],[v[0], v[1]/t[1]],'b-')
    plt.plot([t[1] + k, t[2] + k],[v[1]/t[1], ((v[2] - v[1])/(t[2] - t[1]))],'b-')
    plt.plot([t[2] + k, t[3] + k],[((v[2] - v[1])/(t[2] - t[1])), ((v[3] - v[2])/(t[3] - t[2]))],'b-')
    

    plt.show()
main()
