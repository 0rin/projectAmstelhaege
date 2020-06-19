# random.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# A random placing algorithm for Amstelhaege.

from functions.score import calculateScore, distancesBetweenMany, validatePlacements
import random as random
from math import sqrt, ceil
import numpy as np


def randomPlacements(amstelhaege):
    """ Randomly places houses on the grid.
        Args:       The setup for the case Amstelhaege.
        Returns:    True on succes, false otherwise.
        Note:
        There are ranLimit attempts for placing objects. If not everything has
        been placed after all these attempts, then everything is resetted and
        another ranLimit attempts will be made from scratch.
        There are maxNrAttempts times everything starts from scratch.
        This is done to increase the chance on succes.
    """
    ranLimit = 1000
    maxNrAttempts = 10

    for attempt in range(maxNrAttempts):
        ah = amstelhaege.houses
        allHousesPlaced = False
        allWatersPlaced = False
        random.shuffle(ah)
        ranCnt = 0

        # obtain the distribution of the water over the waters
        percentages = divideInParts(amstelhaege.nrWaters)

        # place waters first
        indexWaters = 0
        while indexWaters < amstelhaege.nrWaters and ranCnt < ranLimit:

            ranCnt += 1
            water = amstelhaege.waters[indexWaters]
            waterArea = percentages[indexWaters] * amstelhaege.waterArea

            # determine the dimensions of the water
            lowBndLength = max(1, int(sqrt(waterArea * amstelhaege.lowBndRatio /
                                           amstelhaege.upBndRatio)))
            upBndLength = int(sqrt(waterArea * amstelhaege.upBndRatio / amstelhaege.lowBndRatio))
            waterLength = random.randint(lowBndLength, upBndLength)
            waterWidth = int(ceil(waterArea / waterLength))

            # determine the position, e.i. coordinates for top left corner
            x = random.randint(0, amstelhaege.length - waterLength)
            y = random.randint(0, int(amstelhaege.width - waterWidth))

            # set coordinates
            water.x1 = x
            water.x2 = x + waterLength
            water.y1 = y
            water.y2 = y + waterWidth
            water.length = waterLength
            water.width = waterWidth

            # get distance to previously placed waters
            distancesBetweenMany(amstelhaege, indexWaters + 1, "waters")

            # validate position
            if validatePlacements(amstelhaege, indexWaters + 1, "waters"):
                indexWaters += 1

            if indexWaters == amstelhaege.nrWaters:
                allWatersPlaced = True

        # place houses
        index = 0
        while not allHousesPlaced and ranCnt < ranLimit:
            ranCnt += 1
            house = ah[index]

            # determine the borders for valid placement
            leftBorder = ah[index].minFreeSpace
            rightBorder = amstelhaege.length - ah[index].minFreeSpace - ah[index].length
            bottomBorder = amstelhaege.width - ah[index].minFreeSpace - ah[index].width
            topBorder = ah[index].minFreeSpace

            # get coordinates for top left corner of the house
            x = random.randint(leftBorder, rightBorder)
            y = random.randint(topBorder, bottomBorder)

            # set coordinates
            house.x1 = x
            house.x2 = x + house.length
            house.y1 = y
            house.y2 = y + house.width

            # get distances to previously placed houses
            distancesBetweenMany(amstelhaege, index + 1, "houses")

            # validate position
            if validatePlacements(amstelhaege, index + 1, "houses"):
                index += 1

            if index == amstelhaege.variant:
                allHousesPlaced = True

        if (allHousesPlaced and allWatersPlaced):
            amstelhaege.validConfig = True
            calculateScore(amstelhaege)
            return True
        else:
            amstelhaege.resetSetup()

    print("exit randomPlacements without succes")
    return False


def divideInParts(numberOfParts, partitionList=[1]):
    """ Creates n numbers between 0 and 1 that add up to 1.
        Splits the number 1 (n - 1) times into two parts.
        Args:
            An integer for the number of parts we need.
            The second argument is passed in through the recursion.
        Returns:
            An array with n numbers between 0 and 1 that add up to 1.
        This is a recursive function.
    """
    # ends recursion
    if numberOfParts == 1:
        return partitionList

    # divide the biggest part
    list.sort(partitionList)
    biggestPart = partitionList[-1]

    # remove the part we are going to split into two
    partitionList = partitionList[:-1]

    # split the biggest part into two smaller parts
    part1 = random.uniform(0, biggestPart)
    part2 = biggestPart - part1

    # add the two new parts to the list
    partitionList.append(part1)
    partitionList.append(part2)

    # recursion
    return divideInParts(numberOfParts - 1, partitionList)
