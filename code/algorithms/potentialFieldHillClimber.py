# PotentialFieldHillClimbers.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# A variant of the hillclimber algorithm where at each step a potential field
# is calculated upon which the movement of the houses is based.


import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math as m
from functions.score import calculateScore


def potentialFieldHC(amstelhaegeInput, steps= 100, exportImages=False):
    length = amstelhaegeInput.length
    width = amstelhaegeInput.width
    maisonPrIm = (0.06 * 610000)/2.

    plotFieldList = []
    houseList = []
    waterList = []
    amstelhaege = copy.deepcopy(amstelhaegeInput)

    terrain = None

    infoRetrieval = retrieveInfo(amstelhaege)
    houseList = infoRetrieval[0]
    waterList = infoRetrieval[1]

    step = 0
    while step < steps:
        # ------------------- CALCULATE POTENTIAL ------------------------------
        # Initialise potential field with 0 potential
        PField = np.array([[0] * length] * width)

        # Add boundary and water contribution
        PField = boundaryContribution(PField, houseList, maisonPrIm, length, width)
        PField = addWater(PField, waterList, maisonPrIm * 5)
        # NOTE: the potential strength of water and the boundaries are set to
        # maisonPrIm and maisonPrIm * 5 but these are variable.

        # Add contribution of houses
        for i in range(len(houseList)):
            PField = addContribution(PField, houseList[i], houseList, length, width)

        # ------------------- MOVE HOUSES --------------------------------------
        # copy houselist to create a houselist that can be tested on
        newHouseList = copy.deepcopy(houseList)

        # Move all houses with the best move
        for i in range(len(houseList)):
            newHouseList[i] = potentialMoveHouse(PField, houseList[i], length, width)

        houseList = newHouseList

        # Save arrays for eventual export to images
        if exportImages == True:
            PFieldWithHouse = copy.deepcopy(PField)
            plotFieldList.append(PFieldWithHouse)

        step += 1

    # ------------------- UPDATE FOR RESULTS -----------------------------------
    # After climbing, copy info from houseList back into amstelhaege
    for i in range(len(amstelhaege.houses)):
        houseUpdate = amstelhaege.houses[i]

        houseUpdate.x1 = houseList[i][0]
        houseUpdate.y1 = houseList[i][1]
        houseUpdate.x2 = houseList[i][2]
        houseUpdate.y2 = houseList[i][3]
        houseUpdate.price = houseList[i][4]
        houseUpdate.prIm = houseList[i][5]
        houseUpdate.minFreeSpace = houseList[i][6]

    resultScore = calculateScore(amstelhaege)

    # Exports the plots of the saved arrays to images
    if exportImages == True:
        for i in range(len(plotFieldList)):
            fig = plt.figure()
            plt.imshow(plotFieldList[i])
            plt.title("step " + str(i))
            plt.savefig("../results/images/exports/potentialField/Im" + str(i) + ".png")
            plt.close(fig)

    return amstelhaege

# -------------------FUNCTIONS--------------------------------------------------
def retrieveInfo(amstelhaege):
    """
    Retrieves information on the houses and the water from the given setup.
    Args:
        amstelhaege: An amstelhaege object (see amstelhaegeSetup)
    Returns:
        A tuple containing a list of lists of information on all houses and a
        list of coordinates of all bodies of water.
    """
    houseList = []
    waterList = []

    # Copies the relevent information on all houses in the setup to houseList
    for house in amstelhaege.houses:
        houseInfoList = [house.x1, house.y1, house.x2, house.y2, house.price, house.prIm, house.minFreeSpace]
        houseList.append(houseInfoList)

    # Copies the relevent information on all bodies of water to waterList
    for water in amstelhaege.waters:
        waterInfoList = [water.x1, water.y1, water.x2, water.y2]
        waterList.append(waterInfoList)

    return (houseList, waterList)


def boundaryContribution(PotField, houseList, strength, length, width):
    """
    Adds the contribution of the boundaries to the potential field.
    Args:
        Potfield; A numpy array representing the potential field.
        houseList; List holding the x1, y1, x2, y2, price and prIm of every house.
    Returns:
        A potential field with the contribution of tbe boundary added.
    """
    for house in houseList:
        refX1 = house[0]
        refY1 = house[1]
        refX2 = house[2]
        refY2 = house[3]
        maxDelta = largestDelta(refX1, refY1, refX2, refY2)

        # Add potential to the field in an area around the house and its
        # possible rotated position
        for x in range(refX1 - 1, refX1 + maxDelta + 1):
            for y in range(refY1 - 1, refY1 + maxDelta + 1):

                # If within the boundaries: add potential of
                # strength / (distance to boundary)
                if x >= 0 and x < length and y >= 0 and y < width:
                    distance = min([x ,y, length - x, width - y]) + 1
                    PotField[y][x] += strength / distance
    return PotField

def addWater(potField, waterList, strength):
    """
    Adds a potential to the cells that water occupies.
    Args:
        Potfield; A numpy array representing the potential field.
        waterList; A list holding coordinates of the bodies of water.
    Returns:
        A potential field with the contribution of water added.
    """
    for water in waterList:
        x1 = water[0]
        y1 = water[1]
        x2 = water[2]
        y2 = water[3]

        # For every cell which the water occupies: add strength to the potential
        for x in range(x1, x2):
            for y in range(y1, y2):
                potField[y][x] += strength
    return potField

def addContribution(PotField, houseInfo, houseList, length, width):
    """
    Adds the contribution of a house's potential to the potential field.
    Args:
        Potfield; A numpy array representing the potential field.
        houseInfo; A list holding the x1, y1, x2, y2, price and prI of a house.
    Returns:
        A potential field with the contribution of the house added.
    """
    x1 = houseInfo[0]
    y1 = houseInfo[1]
    x2 = houseInfo[2]
    y2 = houseInfo[3]
    price = houseInfo[4]
    prIm = houseInfo[5]
    spaceMin = houseInfo[6]

    improvementPerCell = (prIm * price) / 2

    # Add potential on the field around the other houses
    for house in houseList:
        refX1 = house[0]
        refY1 = house[1]
        refX2 = house[2]
        refY2 = house[3]

        maxDelta = largestDelta(refX1, refY1, refX2, refY2)

        # Add potential in an area of 1 pixel larger radius around the space
        # house occupies and the space a possible rotated house occupies
        for x in range(refX1 - 1, refX1 + maxDelta + 1):
            for y in range(refY1 - 1, refY1 + maxDelta + 1):
                distance = distanceToPoint(x, y, x1, y1, x2, y2)
                potential = 0

                # To prevent potential outside the boundaries
                withinBounds = (x >= 0 and x < length and y >= 0 and y < width)

                # To prevent placing potential in its own freespace
                inOwnFreespace = (x >= x1 - spaceMin and x <= x2 + spaceMin and
                                    y >= y1 - spaceMin and y <= y2 + spaceMin)
                if inOwnFreespace:
                    # Large potential
                    potential = improvementPerCell * 8

                if withinBounds and distance != 0 and not inOwnFreespace:
                    potential = improvementPerCell * (1 / (distance))
                PotField[y][x] += potential

    return PotField



def potentialMoveHouse(PotField, houseInfo, length, width):
    """
    Checks a house's possible moves and moves the house in the best direction
    Args:
        Potfield; A numpy array representing the potential field.
        houseInfo; A list holding the x1, y1, x2, y2, price, prI
            and spaceMin of a house.
    Returns:
        A houseInfo list with the position coordinates of the higher potential
        location.
    """
    dummyHouse = copy.copy(houseInfo)
    moveChanges = []
    moveScores = []

    # Test movement
    for xChange in [-1, 0, 1]:
        for yChange in [-1, 0, 1]:
            # Move dummy
            dummyX1 = dummyHouse[0] = dummyHouse[0] + xChange
            dummyY1 = dummyHouse[1] = dummyHouse[1] + yChange
            dummyX2 = dummyHouse[2] = dummyHouse[2] + xChange
            dummyY2 = dummyHouse[3] = dummyHouse[3] + yChange

            # Log new coordinates
            moveChanges.append([dummyX1, dummyY1, dummyX2, dummyY2])

            # Calculate and log the potential for the moved dummy
            dummyScore = potentialCalculator(PotField, dummyHouse, length, width)
            moveScores.append(dummyScore)


            # Reset dummy house to initial position
            dummyHouse = copy.copy(houseInfo)

    # Test rotation
    # Move dummy
    deltaX = abs(houseInfo[2] - houseInfo[0])
    deltaY = abs(houseInfo[3] - houseInfo[1])
    dummyX2 = dummyHouse[0] + deltaY
    dummyY2 = dummyHouse[1] + deltaX
    dummyHouse[2] = dummyX2
    dummyHouse[3] = dummyY2

    # log new coordinates. x1 and y1 are left unchanged.
    moveChanges.append([houseInfo[0], houseInfo[1], dummyX2, dummyY2])

    # Calculate and log the potential for the rotated dummy
    dummyScore = potentialCalculator(PotField, dummyHouse, length, width)
    moveScores.append(dummyScore)

    # Reset dummy house to initial position
    dummyHouse = copy.copy(houseInfo)


    # Find the the coordinates for the best score
    bestScoreIndex = moveScores.index(min(moveScores))
    bestMove = moveChanges[bestScoreIndex]

    # Copy the new (and better) coordinates to newHouseInfo. Return newHouseInfo
    newHouseInfo = houseInfo
    for i in range(4):
        newHouseInfo[i] = bestMove[i]

    return newHouseInfo



def potentialCalculator(PotField, houseInfo, length, width):
    """
    Calculates the sum of the potential of the cells a house occupies
    Args:
        Potfield; A numpy array representing the potential field.
        houseInfo; A list holding the x1, y1, x2, y2, price, prI
            and spaceMin of a house.
    Returns:
        A houseInfo list with the position coordinates of the higher potential
        location.
    """
    houseX1 = houseInfo[0]
    houseY1 = houseInfo[1]
    houseX2 = houseInfo[2]
    houseY2 = houseInfo[3]

    # Calculates the sum of the potential in the cells that the house occupies
    potentialSum = 0
    for x in range(houseX1, houseX2):
        for y in range(houseY1, houseY2):
            if x >= 0 and x < length and y >= 0 and y < width:
                potentialSum += PotField[y][x]
            else:
                # Arbitrary high number to discourage moving over the boundary
                potentialSum = 100000
                break

    return potentialSum


def largestDelta(x1, y1, x2, y2):
    # Determine along which axis the house is longer
    dX = abs(x2 - x1)
    dY = abs(y2 - y1)
    maxDelta = max([dY, dX])
    return maxDelta


def distanceToPoint(pointX, pointY, houseX1, houseY1, houseX2, houseY2):
    """
    Determines the distance from a point to a house
    Args:
        the x and y coordinates of the point and the coordinates of two
        opposing corners of the house.
    Returns:
        The distance between the point and the house.
    """
    #determine x distance
    if pointX < houseX1:
        dx = abs(pointX - houseX1)
    if pointX > houseX2:
        dx = abs(pointX - houseX2)
    if pointX >= houseX1 and pointX <= houseX2:
        dx = 0

    #determine y distance
    if pointY < houseY1:
        dy = abs(pointY - houseY1)
    if pointY > houseY2:
        dy= abs(pointY - houseY2)
    if pointY >= houseY1 and pointY <= houseY2:
        dy = 0

    return m.sqrt(dx**2 + dy**2)
