from utilFuncs import *


class Segment():
    def __init__(self, label):
        self.label = label
        self.length: float = None

        FIGURES[label] = self


class Polygon():
    def __init__(self, label):
        self.label = label
        self.sides = []

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

    def methodToAttr(self, method: str):
        for attr in self.ways:
            if method in self.ways[attr]:
                return attr

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