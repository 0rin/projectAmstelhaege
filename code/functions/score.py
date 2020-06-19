# score.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# This file contains the score function for the Amstelhaege case, as wel
# as some helper functions to obtain the score.

from math import sqrt


def calculateScore(amstelhaege):
    """ Calculates the score.
        Args:
            The setup for the case Amstelhaege.
        Returns:
            The score, as a float.
    """
    amstelhaege.validConfig = False

    # get free space of all objects
    distancesBetweenMany(amstelhaege, "all", "houses")
    distancesBetweenMany(amstelhaege, "all", "waters")

    # validate
    if (validatePlacements(amstelhaege, "all", "houses") and
            validatePlacements(amstelhaege, "all", "waters")):
        amstelhaege.validConfig = True

    # calculate value of every house
    values = []
    for h in amstelhaege.houses:
        if h.validPosition:
            value = (h.freeSpace - h.minFreeSpace) / 2 * h.prIm * h.price + h.price
        else:
            value = 0

        values.append(value)

    # calculate score
    score = sum(values)
    amstelhaege.score = score

    return score


def validatePlacements(amstelhaege, numberPlaced, objectType):
    """ Validates the placements of the given objects.
        Args:
            The amstelhaege setup,
            The number of allready placed houses/waters or "all".
            A string indicating the type of objects e.g. "houses" or "waters".
        Returns:
            True if the free space meets the requirements. False otherwise.
    """

    if objectType == "houses":
        objects = amstelhaege.houses
        if numberPlaced == "all":
            numberPlaced = amstelhaege.variant
    elif objectType == "waters":
        objects = amstelhaege.waters
        if numberPlaced == "all":
            numberPlaced = amstelhaege.nrWaters

    # iterate over the placed objects
    for i in range(numberPlaced):
        obj1 = objects[i]

        # check if object is within the area
        if obj1.x1 < 0 or obj1.x1 >= amstelhaege.length or\
                obj1.x2 < 0 or obj1.x2 >= amstelhaege.length or\
                obj1.y1 < 0 or obj1.y1 >= amstelhaege.width or\
                obj1.y2 < 0 or obj1.y2 >= amstelhaege.width:
            obj1.validPosition = False
            return False

        # check if object is in water
        for water in amstelhaege.waters:
            if checkOverlap(obj1, water):
                obj1.validPosition = False
                return False

        # check free space requirements
        if obj1.freeSpace < obj1.minFreeSpace:
            obj1.validPosition = False
            return False

        else:
            obj1.validPosition = True

    return True


def distancesBetweenMany(amstelhaege, numberPlaced, objectType):
    """ Determines the free space for each object (house or water).
        Args:
            The amstelhaege setup,
            The number of allready placed houses/waters or "all".
            A string indicating the type of objects e.g. "houses" or "waters".
        Returns:
            True, and fills in the free space of the objects.
    """
    if objectType == "houses":
        objects = amstelhaege.houses
        if numberPlaced == "all":
            numberPlaced = amstelhaege.variant
    elif objectType == "waters":
        objects = amstelhaege.waters
        if numberPlaced == "all":
            numberPlaced = amstelhaege.nrWaters

    # iterate over the placed objects
    for i in range(numberPlaced):
        obj1 = objects[i]

        # default distances are distances to the edges of the grid
        distances = [obj1.x1, obj1.y1, amstelhaege.length - obj1.x2, amstelhaege.width - obj1.y2]

        # iterate over the other placed objects
        for j in [x for x in range(numberPlaced) if x != i]:
            obj2 = objects[j]

            # add the distance between the objects to the list
            distance = distanceBetweenTwo(obj1, obj2)
            distances.append(distance)

        # get the minimum distance to any other object (of the same type)
        obj1.freeSpace = min(distances)

    return True


def distanceBetweenTwo(obj1, obj2):
    """ Determines the shortest distance between two objects.
        Args:
            Two objects (e.i. houses or waters).
        Returns:
            An integer representing the minimal distance between these objects.
    """
    # obtain dx, which is the distance in horizontal direction
    if (obj1.x1 >= obj2.x1 and obj1.x1 <= obj2.x2) or (obj1.x2 >= obj2.x1 and obj1.x2 <= obj2.x2):
        dx = 0
    else:
        dx = min(abs(obj1.x1 - obj2.x2), abs(obj1.x2 - obj2.x1))

    # obtain dy, which is the distance in vertical direction
    if (obj1.y1 >= obj2.y1 and obj1.y1 <= obj2.y2) or (obj1.y2 >= obj2.y1 and obj1.y2 <= obj2.y2):
        dy = 0
    else:
        dy = min(abs(obj1.y1 - obj2.y2), abs(obj1.y2 - obj2.y1))

    # use pythagoras theorem for the distance
    return int(sqrt(dx**2 + dy**2))


def checkOverlap(obj1, obj2):
    """ Checks if objects overlap.
        Args:
            Two objects (e.i. houses and/or waters).
        Returns:
            True/false.
    """
    # this checks for partial overlap in a + shape
    if (((obj1.x1 < obj2.x1 and obj1.x2 > obj2.x2) and
         (obj1.y1 > obj2.y1 and obj1.y2 < obj2.y2)) or
        ((obj1.x1 > obj2.x1 and obj1.x2 < obj2.x2) and
         (obj1.y1 < obj2.y1 and obj1.y2 > obj2.y2))):
        return True

    # this checks for partial overlap in other shapes than +
    elif (((obj1.x1 > obj2.x1 and obj1.x1 < obj2.x2) or
           (obj1.x2 > obj2.x1 and obj1.x2 < obj2.x2)) and
          ((obj1.y1 > obj2.y1 and obj1.y1 < obj2.y2) or
           (obj1.y2 > obj2.y1 and obj1.y2 < obj2.y2))):
        return True

    # this checks for one object fully contained within the other
    elif ((obj1.x1 < obj2.x1 and obj1.x2 > obj2.x2) and
          (obj1.y1 < obj2.y1 and obj1.y2 > obj2.y2) or
          (obj1.x1 > obj2.x1 and obj1.x2 < obj2.x2) and
          (obj1.y1 > obj2.y1 and obj1.y2 < obj2.y2)):
        return True
    return False
