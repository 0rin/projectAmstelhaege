# hillclimber.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# Contains the Hillclimber algorithm as well as the Simulated Annealing algorithm
# for the case Amstelhaege.

from functions.score import calculateScore
import random as random
from copy import deepcopy
from math import exp


def hillclimber(amstelhaege, nrIterations, chancesActions=[1 / 3, 1 / 3, 1 / 3]):
    """ Runs a hillclimber algorithm.
        Args:       amstelhaege: A setup for the case Amstelhaege.
                    nrIterations: The number of iterations.
                    chancesActions: An array with the chance for each action,
                                    (optional, default is [1/3, 1/3, 1/3]).
        Returns:    A new setup for the case Amstelhaege.
        Selects randomly an object (house or water), performs some random
        change on this objec, accepts change if the score doesn't get worse.
    """
    amstelhaegeNew = deepcopy(amstelhaege)
    previousScore = amstelhaegeNew.score

    for i in range(nrIterations):

        # remember setup
        amstelhaegePrevious = deepcopy(amstelhaegeNew)

        # choose a house or water
        obj = random.choice(amstelhaegeNew.houses + amstelhaegeNew.waters)

        # make some random change and get the score
        randomChange(amstelhaegeNew, obj, chancesActions)
        newScore = calculateScore(amstelhaegeNew)

        # new high score
        if newScore < previousScore:
            amstelhaegeNew = deepcopy(amstelhaegePrevious)

        # remember the new score
        else:
            previousScore = newScore

    return amstelhaegeNew


def simulatedAnnealing(amstelhaege, nrIterations,
                       chancesActions=[1 / 3, 1 / 3, 1 / 3], startingTemp=20000):
    """ Runs a simulated annealing algorithm.
        Args:       amstelhaege: The setup for the case Amstelhaege.
                    nrIterations: The number of iterations.
                    chancesActions: An array with the chance for each action,
                                    (optional, default is [1/3, 1/3, 1/3]).
                    startingTemp: The initial temperature
                                    (optional, default is 20000).
        Returns:    A new setup for the case Amstelhaege.
        Selects randomly an object (house or water), performs some random change
        on this object. If the change is no downturn, it is accepted.
        Otherwise the change is accepted  with a chance depending on the size
        of the deterioration and the iteration.
    """
    amstelhaegeNew = deepcopy(amstelhaege)
    currentHighscore = 0
    previousScore = amstelhaegeNew.score
    bestConfig = deepcopy(amstelhaegeNew)
    amstelhaegeBest = deepcopy(amstelhaegeNew)

    for i in range(nrIterations):

        # remember setup
        amstelhaegePrevious = deepcopy(amstelhaegeNew)

        # choose an object
        obj = random.choice(amstelhaegeNew.houses + amstelhaegeNew.waters)

        # make some random change on this object and get the resulting score
        randomChange(amstelhaegeNew, obj, chancesActions)
        newScore = calculateScore(amstelhaegeNew)

        if newScore >= previousScore:
            previousScore = newScore


            if newScore > currentHighscore and amstelhaegeNew.validConfig:
                currentHighscore = newScore
                amstelhaegeBest = deepcopy(amstelhaegeNew)
        else:
            temperature = startingTemp * nrIterations / float(1 + i)
            acceptanceChance = exp((newScore - previousScore) / temperature)
            chosenNr = random.uniform(0, 1)

            # accept
            if chosenNr < acceptanceChance:
                previousScore = newScore

            # discard
            else:
                amstelhaegeNew = deepcopy(amstelhaegePrevious)

    amstelhaegeNew = deepcopy(amstelhaegeBest)

    return amstelhaegeNew


def randomChange(amstelhaege, obj, chancesActions=[1 / 3, 1 / 3, 1 / 3]):
    """ Makes some random change (move, rotate or swap) on the given object.
        Args:       amstelhaege: A setup for the case Amstelhaege.
                    obj: An object e.i. house or water
                    chancesActions: An array with the chance for each action,
                                    (optional, default is [1/3, 1/3, 1/3]).
        Returns:    True
    """
    stepsize = 2

    # choose an action
    action = random.choice(["move", "rotate", "swap"])

    # if object is water, allow only moves
    if obj.price == 0:
        action = "move"

    if action == "move":
        # choose a direction
        xMove, yMove = random.choice([[stepsize, 0],
                                      [-stepsize, 0],
                                      [0, stepsize],
                                      [0, -stepsize]])
        obj.relocate(obj.x1 + xMove,
                     obj.y1 + yMove,
                     obj.x2 + xMove,
                     obj.y2 + yMove)

    elif action == "rotate" and (obj.length != obj.width):
        obj.rotate()

    elif action == "swap":

        # choose a different type of house to swap with
        sameType = True
        while sameType:
            obj2 = random.choice(amstelhaege.houses)
            if obj.prIm != obj2.prIm or obj.minFreeSpace != obj2.minFreeSpace:
                sameType = False

        # swap houses
        obj, obj2 = obj2, obj

    return True
