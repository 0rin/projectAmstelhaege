# linegraph.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# Produces a line graph of the results

import matplotlib.pyplot as plt
# from mpldatacursor import datacursor
# from matplotlib.ticker import ScalarFormatter, FormatStrFormatter


# draw line from data
def drawLine(ax, data, lineColor, label):

    lines, = ax.plot(data, color=lineColor)
    lines.set_label(label)

    # set label
    plt.legend()


def drawLines(inputdata):
    random, hillclimber, simulatedAnnealing = [], [], []

    # split the input data as rowdata
    my_list = inputdata.splitlines()
    for index in range(1, len(my_list)):
        if (my_list[index] == ""):
            continue

         # split the rowdata as colum data
        rowdata = my_list[index].split(",")

        # append data to list
        random.append(float(rowdata[0]))
        hillclimber.append(float(rowdata[1]))
        simulatedAnnealing.append(float(rowdata[2]))


    fig, ax = plt.subplots()

    # draw lines
    drawLine(ax, random, "blue", "random")
    drawLine(ax, hillclimber, "red", "hillclimber")
    drawLine(ax, simulatedAnnealing, "green", "simulated annealing")

    # set labels and draw plot
    plt.title("20 variant")
    plt.xlabel("Scores")
    plt.ylabel("Number")
    plt.show()


def main():

	# get data from csv filer
    with open("results/20_variant/20AlgosTest.csv", "r") as infile:
        inputdata = infile.read()

    # draw lines
    drawLines(inputdata)


if __name__ == "__main__":
    main()
