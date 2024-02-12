import math
import inspect as ins
import sys
import time


def translateByLabels(lst):
    res = []
    for item in lst:
        res.append(item.label)
    return res


def attrKnown(label, attr):
    return type(getattr(FIGURES[label], attr)).__name__ != "NoneType"


def getClassNameByLabel(label: str):
    return FIGURES[label].__class__.__name__


def findPath(goalTarget: str, goalAttr: str = ""):
    pass

TARGETED = {}
FIGURES = {}


class Segment():
    def __init__(self, label):
        self.label = label
        self.length: float = None

        FIGURES[label] = self


class Polygon():
    def __init__(self, label):
        self.label = label
        self.sides = []
        self.area = None

        FIGURES[label] = self

        # инициализация всех сторон
        for i in range(len(self.label)):
            for j in range(i+1, len(self.label)):
                char1 = self.label[i]
                char2 = self.label[j]
                Segment(char1+char2)
                self.sides.append(char1+char2)

        # пути получения данных
        self.ways = {
            "angle": [],
            "length": [],
            "area": [],
            "perimeter": ["perimeterClassic"]
        }

    def perimeterClassic(self, any):
        p = 0
        delegateFind = {}

        for side in self.sides:
            if not attrKnown(side, "length"):
                delegateFind[side] = "length"
            else:
                p += FIGURES[side].length

        if delegateFind == {}:
            return p
        else:
            return delegateFind


class Triangle(Polygon):
    def __init__(self, label):
        super().__init__(label)

        self.ways["length"].extend(["sinTheorem"])

    def sinTheorem(self, toFind: str):
        delegateFind = []

        pass


class isoscelesTriangle(Triangle):
    def __init__(self, label: str, baseSide: str):
        super().__init__(label)
        self.baseSide = baseSide


class rightTriangle(Triangle):
    def __init__(self, label: str, rightVertex: str):
        super().__init__(label)
        self.rightVertex = rightVertex
        self.legs = []
        for side in self.sides:
            if self.rightVertex in side:
                self.legs.append(side)
            else:
                self.hypotenuse = side

        self.ways["length"].extend(["pythagorean"])
        self.ways["area"].extend(["areaByLegs"])

    def areaByLegs(self, any):
        """
        Calculate the area of a figure based on the lengths of its legs.

        Parameters:
            self (obj): The object itself.
            any: Any parameter.

        Returns:
            float: The area of the figure if the lengths of all legs are known, a dictionary containing the legs and their missing attributes otherwise.
        """

        delegateFind = {}
        for leg in self.legs:
            if not attrKnown(leg, "length"):
                delegateFind[leg] = "length"
        if delegateFind == {}:
            self.area = 0.5 * FIGURES[self.legs[0]
                                      ].length * FIGURES[self.legs[1]].length
            return self.area
        else:
            return delegateFind

    def pythagorean(self, targetSide: str):
        """
        Calculate the missing side length of a right-angled triangle using the Pythagorean theorem. 

        Args:
            toFind: The side length to calculate.

        Returns:
            If the side length toFind is found, returns the length value. If not found, returns a list of sides to calculate.
        """

        delegateFind = {}
        if targetSide != self.hypotenuse:
            if not attrKnown(self.legs[self.legs.index(targetSide) ^ 1], "length"):
                delegateFind[self.legs[self.legs.index(
                    targetSide) ^ 1]] = "length"

            if not attrKnown(self.hypotenuse, "length"):
                delegateFind[self.hypotenuse] = "length"

            if delegateFind == {}:
                FIGURES[targetSide].length = math.sqrt(
                    FIGURES[self.hypotenuse].length ** 2 - FIGURES[self.legs[self.legs.index(targetSide) ^ 1]].length ** 2)
                return FIGURES[targetSide].length
            else:
                return delegateFind
        else:
            delegateFind = {}
            for leg in self.legs:
                if not attrKnown(leg, "length"):
                    delegateFind[leg] = "length"

            if delegateFind == {}:
                FIGURES[targetSide].length = math.sqrt(
                    FIGURES[self.legs[0]].length ** 2 + FIGURES[self.legs[1]].length ** 2)
                return FIGURES[targetSide].length
            else:
                return delegateFind


# площадь
ack = rightTriangle("ACK", "K")
abc = rightTriangle("ABC", "C")

FIGURES["AB"].length = 5
FIGURES["BC"].length = 3
find("ABC", "area")

# катет через другой треугольник
# abc = rightTriangle("ABC", "C")
# abd = rightTriangle("ABD", "A")
# FIGURES["AD"].length = 12
# FIGURES["BD"].length = 13
# FIGURES["BC"].length = 3
# find("AC", "length")
