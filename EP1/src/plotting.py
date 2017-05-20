import matplotlib.pyplot as plt
import os
import sys

####################################################################################
# Esse programa lê um arquivo de texto e a partir dele, plota os dados             #
# em um gráfico de "deslocamento x tempo". Cada linha desse arquivo é dado         #
# na forma "x,y\n", onde x é o tempo (em segundos) e y é o deslocamento (em metros)#
####################################################################################

# cria a figura e insere o gráfico dentro
figure = plt.figure()
plot = figure.add_subplot(111)

# seta as propriedades do gráfico, como legendas e escalas
plot.set_title("Deslocamento x tempo")
plot.set_ylabel("Deslocamento (m)")
plot.set_xlabel("Tempo (s)")
plot.set_ylim(30)
plot.set_axisbelow(True)
plot.yaxis.grid(color="grey", linestyle="dashed")
plot.xaxis.grid(color="grey", linestyle="dashed")
plot.invert_yaxis()

# abre o arquivo com os dados a serem plotados no gráfico
# supõe que cada linha do arquivo é da forma "x,y\n", onde
# x é o tempo (em segundos), e y é o deslocamento (em metros).
# Ambos x e y devem ser números em ponto flutuante
x = [0]
y = [0]
if len(sys.argv) > 1:
	input_file = sys.argv[1]
else:
	raise Exception("Nenhum arquivo de dados fornecido.")
with open(input_file, "r+") as f:
	line = f.readline()
	while line is not "":
		line = line.split(",")
		x.append(float(line[0]))
		y.append(float(line[1].strip()))
		line = f.readline()

# plota os dados no gráfico
plot.plot(x, y)

# salva a imagem no diretório do qual o script está sendo executado
current_dir = os.getcwd()
output_file = current_dir + "/plot_" + input_file.split(".")[0]
plt.savefig(output_file)
