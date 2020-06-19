# objects.py
# Minor programmeren; Heuristiek; Amstelhaege
#
# team KOX
# Khalid El Khuri   11927739
# Orin Habich       10689508
# Xander Locsin     10722432
#
# Contains the class for objects for Amstelhaege.py, those objects can be
# houses and waters.


class AmstelhaegeObject:
    """ An object for Amstelhaege. e.g. a house or water.

    Attributes:
        Name            Type        Description
        x1              integer     Coordinate of left side.
        y1              integer     Coordinate of top side.
        x2              integer     Coordinate of right side.
        y2              integer     Coordinate of bottom side.
        price           integer     The price.
        prIm            float       The price improvement per meter.
        minFreeSpace    integer     Required minimum free space.
        length          integer     Length.
        width           integer     Width.
        freeSpace       integer     Actual free space.
        validPosition   boolean     Indicates if the current position is valid.
    """

    def __init__(self, price, prIm, minFreeSpace, length, width):
        """ Initializes the object.
            Args:       Price, price improvement per meter, minimal free space,
                        length of the object, width of the object.
            Returns:    A certain object (a house or water)
        """
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.price = price
        self.prIm = prIm
        self.minFreeSpace = minFreeSpace
        self.length = length
        self.width = width
        self.freeSpace = None
        self.validPosition = False

    def rotate(self):
        """ Rotates the object.
            Position of top left corner is fixed, thus new top left corner
            gets same position as previous top left corner had.
            Args:       None
            Returns:    True
        """
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.length
        self.length, self.width = self.width, self.length
        return True

    def relocate(self, x1New, y1New, x2New, y2New):
        """ Relocates the object.
            Args:       The target coordinates x1New, y1New, x2New, y2New
            Returns:    True
        """
        self.x1, self.y1, self.x2, self.y2 = x1New, y1New, x2New, y2New
        return True
