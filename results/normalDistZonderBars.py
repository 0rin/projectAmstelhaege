# normalDist.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# Produces a normal distrbution graph of the results


import matplotlib.pyplot as plt
import numpy as np

global random_score
global simulated_score
global hillcloimber_score
global axisX
global interval
global shift
random, hillclimber, simulatedAnnealing = [], [], []
axisX = []
interval = 400000
shift = 14400000


# get data for normal distribution
def getData(inputdata):
    my_list = inputdata.splitlines()
    for index in range(1, len(my_list)):
        if (my_list[index] == ""):
            continue

        # split the rowdata as colum data
        rowdata = my_list[index].split(",")
        random[int((float(rowdata[0]) - shift) / interval)] += 1
        hillclimber[int((float(rowdata[1]) - shift) / interval)] += 1
        simulatedAnnealing[int((float(rowdata[2]) - shift) / interval)] += 1


# draw line from data
def drawLine(ax, data, lineColor):
    global axisX
    lines = ax.plot(axisX,data,"bo",axisX,data,"k",color=lineColor)


# initialize of variables
def setVariables(inputdata):
    global random
    global hillclimber
    global simulatedAnnealing
    global axisX
    global interval
    global shift

    for ind in range(0, 16):
        random.append(0)
        hillclimber.append(0)
        simulatedAnnealing.append(0)
        axisX.append(ind * interval + 300000 + shift)


def main():

    # get data from csv file
    with open("results/40_variant/40Algos.csv", "r") as infile:
        inputdata = infile.read()

    # initialize of variables
    setVariables(inputdata)
    # get data for normal distribution from inputdata
    getData(inputdata)

    # draw stacked barcharts
    fig, ax = plt.subplots()
    line1=ax.bar(axisX, random, interval * 19/20,color="w")
    line2=ax.bar(axisX, hillclimber, interval * 19/20, color="w")
    line3=ax.bar(axisX, simulatedAnnealing, interval * 19/20, color="w")
    #plt.legend((line1[0], line2[0], line3[0]), ("random", "hillclimber","simulated annealing"))

    # draw lines
    drawLine(ax, random, "b")
    drawLine(ax, hillclimber, "r")
    drawLine(ax, simulatedAnnealing, "g")
    plt.title("40 variant")
    plt.xlabel("Score")
    plt.ylabel("Count")
    # show graph
    plt.show()

if __name__ == "__main__":
    main()
