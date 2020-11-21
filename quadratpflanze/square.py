import matplotlib.pyplot as plt
import numpy as np

class Square():

    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3
    NONE = -1

    def __init__(self, xy, size, openAt, parentSquare):
        self.xy = xy
        self.size = size
        self.openAt = openAt
        self.parent = parentSquare

    def getSize(self):
        return self.size

    def getX(self):
        return self.xy[0]

    def getXPoints(self):
        x = self.getX()
        return np.array([x, x+self.size, x+self.size, x, x])

    def getY(self):
        return self.xy[1]

    def getYPoints(self):
        y = self.getY()
        return np.array([y, y, y+self.size, y+self.size, y])

    def getXY(self):
        return self.xy

    def getParent(self):
        return self.parent


    def whereOpen(self):
        return self.openAt

    def getChilds(self):
        result = []
        newSize = self.size*1/3
        r = None
        x, y = 0, 0
        if self.openAt != Square.LEFT:
            x = self.getX()-newSize
            y = self.getY()+newSize
            r = Square((x, y), newSize, Square.RIGHT, self)
            result.append(r)

        if self.openAt != Square.RIGHT:
            x = self.getX()+self.size
            y = self.getY()+newSize
            r = Square((x, y), newSize, Square.LEFT, self)
            result.append(r)

        if self.openAt != Square.BOTTOM:
            x = self.getX()+newSize
            y = self.getY()-newSize
            r = Square((x, y), newSize, Square.TOP, self)
            result.append(r)

        if self.openAt != Square.TOP:
            x = self.getX()+newSize
            y = self.getY()+self.size
            r = Square((x, y), newSize, Square.BOTTOM, self)
            result.append(r)

        return result



