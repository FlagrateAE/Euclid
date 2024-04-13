from basics import *
from utilFuncs import *

class Triangle(Polygon):
    def __init__(self, label):
        super().__init__(label)

        self.ways["length"].extend(["sideBySinTheorem"])
        self.ways["area"].extend(["areaBySinTheorem"])

    def sideBySinTheorem(self, targetSide: str):
        delegateFind = []

        pass

    def areaBySinTheorem(self, toFind: str):
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