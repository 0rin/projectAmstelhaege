# amstelhaegeSetup.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# Contains the class that sets up the terrain houses and waters for Amstelhaege.py
# This class contains all specifications of the case.

from classes.amstelhaegeObjects import AmstelhaegeObject
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from math import ceil
import random as random


class AmstelhaegeSetup:
    """ The setup for the project Amstelhaege, thus the terrain, waters and houses.

    Attributes:
        Name            Type        Description

        variant         integer     The total number of houses.
        score           float       The score, sum of values of houses.
        validConfig     boolean     Indicates the validity of the current setup.
        length          integer     Length of the area (in 0.5m).
        width           integer     Width of the area (in 0.5m).
        area            integer     Area of the terrain Amstelhaege.
        grid            array       Grid over the terrain.
        minNrWaters     integer     Minimum number of waters required.
        maxNrWaters     integer     Maximum number of waters required.
        nrWaters        integer     Actual number of waters.
        waterArea       float       Area that has to be water.
        lowBndRatio     integer     Minimum for the ratios of water dimensions.
        upBndRatio      integer     Maximum for the ratios of water dimensions.
        percSfh         float       Required percentage single family houses.
        percBun         float       Required percentage bungalows.
        percMai         float       Required percentage maisons.
        nrSfh           integer     Required number of single family houses.
        nrBun           integer     Required number of bungalows.
        nrMai           integer     Required number of maisons.
        houses          array       List with houses.
        waters          array       List with waters.
    """

    def __init__(self, variant):
        """ Initializes the terrain.
            Args:       The variant (20, 40 or 60).
            Returns:    The setup of the project, with all waters and houses.
        """
        self.variant = variant
        self.score = 0
        self.validConfig = False
        self.length = 360
        self.width = 320
        self.area = self.length * self.width
        self.grid = np.array([[0] * self.length] * self.width)
        self.minNrWaters = 1
        self.maxNrWaters = 4
        self.nrWaters = random.randint(self.minNrWaters, self.maxNrWaters)
        self.waterArea = 0.2 * self.area
        self.lowBndRatio = 1
        self.upBndRatio = 4
        self.percSfh = 0.6
        self.percBun = 0.25
        self.percMai = 0.15
        self.nrSfh = int(self.percSfh * self.variant)
        self.nrBun = int(self.percBun * self.variant)
        self.nrMai = int(self.percMai * self.variant)
        self.houses = []
        self.waters = []
        self.initialiseObjects()

    def initialiseObjects(self):
        """ Initialises all objects for the project. (the houses and waters)
            Args:       None
            Returns:    True,
                        has the side effect that the arrays houses and waters
                        get filled.
        """
        for i in range(self.nrSfh):
            house = AmstelhaegeObject(285000, 0.03, 4, 16, 16)
            self.houses.append(house)
        for i in range(self.nrBun):
            house = AmstelhaegeObject(399000, 0.04, 6, 20, 15)
            self.houses.append(house)
        for i in range(self.nrMai):
            house = AmstelhaegeObject(610000, 0.06, 12, 22, 21)
            self.houses.append(house)
        for i in range(self.nrWaters):
            water = AmstelhaegeObject(0, 0, 1, 0, 0)
            self.waters.append(water)
        return True

    def resetSetup(self):
        """ Resets appropriate fields in this class.
            Args:       None
            Returns:    True
        """
        self.grid = np.array([[0] * self.length] * self.width)
        self.waters = []
        self.houses = []
        self.initialiseObjects()
        self.score = 0
        return True

    def plotSetup(self):
        """ Creates a plot of the current configuration.
            Args:       The setup of the project.
            Returns:    A matplotlib image of the terrain.
        """
        # draw waters (min, max are used to ensure ranges are within area)
        for water in self.waters:
            for j in range(max(0, water.x1), min(water.x2, self.length)):
                for k in range(max(0, water.y1), min(water.y2, self.width)):
                    self.grid[k][j] = 1

        # draw houses
        for i in range(self.variant):
            h = self.houses[i]

            # choose color
            if h.price == 285000:
                color = 2
            elif h.price == 399000:
                color = 3
            elif h.price == 610000:
                color = 4

            # draw house (min, max are used to ensure ranges are within area)
            for j in range(max(0, h.x1), min(h.x2, self.length)):
                for k in range(max(0, h.y1), min(h.y2, self.width)):
                    self.grid[k][j] = color

        # colors mean respectively:
        # grass, water, single family house, bungalow, maison
        cmap = colors.ListedColormap(["mediumseagreen", "dodgerblue",
                                      "red", "orange", "purple"])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # make title
        if self.validConfig:
            title_obj = plt.title("Score: {:,.2f}".format(self.score))
        else:
            title_obj = plt.title("INVALID score: {:,.2f}".format(self.score))
        plt.imshow(self.grid, norm=norm, cmap=cmap)

        # reset grid for next plot
        self.grid = np.array([[0] * self.length] * self.width)

        # show the image
        plt.show()
