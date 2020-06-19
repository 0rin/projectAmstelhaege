# amstelhaege.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# This files runs all the algorithms.


from classes.amstelhaegeSetup import AmstelhaegeSetup
from algorithms.hillclimber import hillclimber, simulatedAnnealing
from algorithms.randomPlacements import randomPlacements
from algorithms.potentialFieldHillClimber import potentialFieldHC
import csv


def main():
    for i in range(250):
        amstelhaege1 = AmstelhaegeSetup(40)
        randomPlacements(amstelhaege1)
        amstelhaege2 = hillclimber(amstelhaege1, 5000)
        amstelhaege3 = simulatedAnnealing(amstelhaege1, 5000)

        with open("results/40_variant/40Algos.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([amstelhaege1.score])


if __name__ == "__main__":
    main()
