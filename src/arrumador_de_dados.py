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
    data =  fixer ("Bia andando 1.csv") # Descomente para testar
    for i in range (len(data) - 1):
        plt.plot([data[i][0], data[i + 1][0]], [data[i][3],data[i + 1][3]], 'r-')

    plt.show()
main()
