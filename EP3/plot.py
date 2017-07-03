from matplotlib import pyplot as plt

def main():
    file = open("flow.txt")
    myvect = []
    myvect2 = []
    for line in file:
        values = line.split(' ')
        values = [float(value) for value in values]
        print (values)
        myvect.append(values[1])
        print (myvect)
        myvect2.append(values[2])
        print (myvect2)  
    plt.ylabel ("Flow")
    plt.xlabel ("Density")
    plt.plot (myvect,myvect2)
    plt.show()

main()
