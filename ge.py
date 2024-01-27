import math
import re

def translateByLabels(lst):
    res = []
    for item in lst:
        res.append(item.label)
    return res

def valueKnown(label, value):
    return type(getattr(FIGURES[label], value)).__name__ != "NoneType"

def getClassNameByLabel(label: str):
    return FIGURES[label].__class__.__name__

GOAL = ""
prevGoal = ""


def find(toFind: str):
    """
    find - This function is used to find a specific element or the area of a figure.
    
    Parameters:
        toFind (str): The element or figure to be found.
    
    Returns:
        None
    """

    global GOAL, prevGoal
    if GOAL == "":
        GOAL = toFind
        print("Goal = " + GOAL)

    if prevGoal == "":
        prevGoal = toFind
    print("prevGoal = " + prevGoal)


    if getClassNameByLabel(toFind) in ["Segment", "Angle"]:
        print("Finding " + toFind)
        
        potentialFigures = []

        for potentialFigure in FIGURES:
            try:
                if len(potentialFigure) > 2 and set(toFind).issubset(set(potentialFigure)): 
                    potentialFigures.append(potentialFigure)
                    way = FIGURES[potentialFigure].findElementMethod(toFind)
            
            except RecursionError:
                continue

# re.match(r'^S\(.+\)$', toFind) is not None
        
    else:
        print("Finding area of " + toFind)
        way = FIGURES[toFind].findElementMethod(toFind)

    if(way.__class__ == list):
            print(f"Need to find {way}")
            
            for need in way:
                find(need)

    else:
        print(f"Done! {toFind} = {way}")

        if toFind == GOAL:
            print(f"COMPLETED! Answer is {way}")
        else:
            find(prevGoal)


FIGURES = {}


class Segment():
    def __init__(self, label):
        self.label = label
        self.length = None

        FIGURES[label] = self

class Polygon():
    def __init__(self, label):
        self.label = label
        self.sides = []
        self.area = None

        FIGURES[label] = self


        for i in range(len(self.label)):
            for j in range(i+1, len(self.label)):
                char1 = self.label[i]
                char2 = self.label[j]
                Segment(char1+char2)
                self.sides.append(char1+char2)

        self.ways = {
            "Angle": [],
            "Segment": [],
            "Area": []
        }

    def findElementMethod(self, toFind):
        if(FIGURES[toFind] == self):
            for method in self.ways["Area"]:
                print(f"Using {method} in {self.label}")
                result = eval(f"self.{method}()")

        else:
            for method in self.ways[getClassNameByLabel(toFind)]:
                print(f"Using {method} in {self.label}")
                result = eval(f"self.{method}('{toFind}')")

        return result

class Triangle(Polygon):
    def __init__(self, label):
        super().__init__(label)

class isoscelesTriangle(Triangle):
    def __init__(self, label, baseSide):
        super().__init__(label)
        Segment(baseSide)
        self.baseSide = baseSide

class rightTriangle(Triangle):
    def __init__(self, label, rightVertex):
        super().__init__(label)
        self.rightVertex = rightVertex
        self.legs = []
        for side in self.sides:
            if self.rightVertex in side:
                self.legs.append(side)
            else:
                self.hypotenuse = side

        self.ways["Segment"].extend(["pythagorean"])
        self.ways["Area"].extend(["areaByLegs"])

    
    def areaByLegs(self):
        delegateFind = []
        for leg in self.legs:
            if type(FIGURES[leg].length).__name__ == "NoneType":
                delegateFind.append(leg)
        if delegateFind == []:
            self.Area = 0.5 * FIGURES[self.legs[0]].length * FIGURES[self.legs[1]].length
            return self.Area
        else:
            return delegateFind
    
    def pythagorean(self, toFind):
        delegateFind = []
        if toFind != self.hypotenuse:
            if not valueKnown(self.legs[self.legs.index(toFind) ^ 1], "length"):
                delegateFind.append(self.legs[self.legs.index(toFind) ^ 1])
            
            if not valueKnown(self.hypotenuse, "length"):
                delegateFind.append(self.hypotenuse)


            if delegateFind == []:
                FIGURES[toFind].length = math.sqrt(FIGURES[self.hypotenuse].length ** 2 - FIGURES[self.legs[self.legs.index(toFind) ^ 1]].length ** 2)
                return FIGURES[toFind].length
            else:
                return delegateFind
        else:
            delegateFind = []
            for leg in self.legs:
                if not valueKnown(leg, "length"):
                    delegateFind.append(leg)


            if delegateFind == []:
                FIGURES[toFind].length = math.sqrt(FIGURES[self.legs[0]].length ** 2 + FIGURES[self.legs[1]].length ** 2)
                return FIGURES[toFind].length
            else:
                return delegateFind


tri = rightTriangle("ABC", "C")
tri2 = rightTriangle("BCD", "C")

FIGURES["BD"].length = 5
FIGURES["AC"].length = 3
FIGURES["CD"].length = 3

find("ABC")
