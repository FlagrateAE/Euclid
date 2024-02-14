import math
import inspect as ins
import sys
import time
import yaml


def translateByLabels(lst):
    res = []
    for item in lst:
        res.append(item.label)
    return res


def attrKnown(label, attr):
    return type(getattr(FIGURES[label], attr)).__name__ != "NoneType"


def getClassNameByLabel(label: str):
    return FIGURES[label].__class__.__name__

def getMethods(target: str, attr: str = ""):
    
    searchZone = []
    
    if attr == "area" or attr == "perimeter":
        searchZone.append(target)
    
    else:
        targetType = getClassNameByLabel(target)
        
        match targetType:
            case "Segment":
                attr = "length"
                
                for figure in FIGURES:
                    if isinstance(FIGURES[figure], Polygon) and set(target).issubset(set(figure)):
                        searchZone.append(figure)
    
    ways = []
    for parentFigure in searchZone:
            for method in FIGURES[parentFigure].ways[attr]:
                    ways.append(f"FIGURES['{parentFigure}'].{method}('{target}')")
    
    return ways


def findPath(goalTarget: str, goalAttr: str = ""):
    # корень (старт - конец)
    goalMethods = getMethods(goalTarget, goalAttr)
    for method in goalMethods:
        PATHES.append([f"{method}<{goalAttr}>"])
        
    while not nextPathSegment():
        nextPathSegment()
    
    for path in PATHES:
        path: list
        path.reverse()
        
        print(*path, sep=" -> ")
        
        # INFERENCE
        for method in path:
            method: str
            method = method.split("<")[0]
            res = eval(method)
        
        print(res)

def nextPathSegment():
    for path in PATHES:
        path: list
        # проверить последний сегмент
        res = eval(path[-1].split("<")[0])
        
        if isinstance(res, dict):
            # продолжение
            PATHES.remove(path)
            for need in res:
                methods = getMethods(need, res[need])
                
                for method in methods:
                    try:
                        if method in path:
                            continue
                        
                        # проверка на совпадение
                        for existingMethod in path:
                            existingMethod: str
                            existingMethodTarget = existingMethod.split("'")[3]
                            existingMethodAttr = existingMethod.split("<")[1][:-1]
                            if need == existingMethodTarget and res[need] == existingMethodAttr:
                                raise Exception("Loop detected")
                            # print(existingMethod.split("'", 1))

                        else:
                            PATHES.append(path + [f"{method}<{res[need]}>"])
                    except Exception:
                        continue
                    
            
            
        elif res.__class__.__name__ == "NoneType":
            # return
            pass
        else:
            return res

PATHES = []
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


# площадь с запутыванием
# ack = rightTriangle("ACK", "K")
# abc = rightTriangle("ABC", "C")
# FIGURES["AB"].length = 5
# FIGURES["BC"].length = 3
# findPath("AC", "length")

# катет через другой треугольник
# abc = rightTriangle("ABC", "C")
# abd = rightTriangle("ABD", "A")
# FIGURES["AD"].length = 12
# FIGURES["BD"].length = 13
# FIGURES["BC"].length = 3
# findPath("AC", "length")

# простой тест пифагора
acb = rightTriangle("ABC", "C")
FIGURES["AB"].length = 5
FIGURES["BC"].length = 3
findPath("ABC", "area")