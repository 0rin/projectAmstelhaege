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
from mpldatacursor import datacursor
from matplotlib.ticker import FormatStrFormatter

global random_score
global simulated_score
global hillcloimber_score
global axisX
global interval
global shift
random_score = []
hillcloimber_score = []
simulated_score = []
axisX = []
interval = 300000
shift = 7200000


# get data for normal distribution
def getData(inputdata):
    my_list = inputdata.splitlines()
    for index in range(1, len(my_list)):
        if (my_list[index] == ""):
            continue

        # split the rowdata as colum data
        rowdata = my_list[index].split(",")
        random_score[int((float(rowdata[0]) - shift) / interval)] += 1
        hillcloimber_score[int((float(rowdata[1]) - shift) / interval)] += 1
        simulated_score[int((float(rowdata[2]) - shift) / interval)] += 1


# draw line from data
def drawLine(ax, data, lineColor):
    global axisX
    lines = ax.plot(axisX,data,"bo",axisX,data,"k",color=lineColor)
    datacursor(lines, formatter="x: {x:0.0f}\ny: {y:0.0f}".format, hover = True)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.0f"))


# initialize of variables
def setVariables(inputdata):
    global random_score
    global hillcloimber_score
    global simulated_score
    global axisX
    global interval
    global shift

   for i nd in range(0, 16):
       random_score.append(0)
       simulated_score.append(0)
       hillcloimber_score.append(0)
       axisX.append(ind * interval + 300000 + shift)


def main():

    # get data from csv file
    with open("results/20Algos.csv", "r") as infile:
        inputdata = infile.read()

    # initialize of variables
    setVariables(inputdata)
    # get data for normal distribution from inputdata
    getData(inputdata)

    # draw stacked barcharts
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.0f"))
    line1=ax.bar(axisX, random_score, interval * 4/5,color="b")
    line2=ax.bar(axisX, simulated_score, interval * 4/5, color="r", bottom=random_score)
    line3=ax.bar(axisX, hillcloimber_score, interval * 4/5, color="g",bottom=np.array(random_score)+ np.array(simulated_score))
    plt.legend((line1[0], line2[0], line3[0]), ("random score", "hillclimber score","simulated annealing score"))

    # draw lines
    drawLine(ax, random_score, "b")
    drawLine(ax, simulated_score, "r")
    drawLine(ax, hillcloimber_score, "g")
    plt.title("20 variant")
    plt.xlabel("Score")
    plt.ylabel("Count")
    # show graph
    plt.show()

if __name__ == "__main__":
    main()
