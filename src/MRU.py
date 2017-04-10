import sys

data_MRU = []
data_MRUV = []

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    raise Exception ("No file found.")

with open(input_file, "r+") as f:
    line = f.readline()
    line = line.split()

    data_MRU.append(line[0:2])
    data_MRU.append(line[2:4])
    data_MRU.append(line[4:6])


print (data_MRU)

v = []
media_tempo = 0;
delta = 0

for i in range (len(data_MRU)):
    media_tempo = (float(data_MRU[i][0]) + float(data_MRU[i][1]))/2
    v.append((i+1)*10/media_tempo)    

print(v)
