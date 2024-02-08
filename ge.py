import math
import inspect as ins

def translateByLabels(lst):
    res = []
    for item in lst:
        res.append(item.label)
    return res

def attrKnown(label, attr):
    return type(getattr(FIGURES[label], attr)).__name__ != "NoneType"

def getClassNameByLabel(label: str):
    return FIGURES[label].__class__.__name__




def find(target: str, attr: str = ""):

    print("Finding ", target)
    targetType = getClassNameByLabel(target)
    parentFigures = []
    
    if attr == "area":
        parentFigures.append(target)

    # в каких фигурах искать
    match targetType:
        case "Segment":
            attr = "sideLength"

            for figure in FIGURES:
                if isinstance(FIGURES[figure], Polygon) and set(target).issubset(set(figure)):
                    parentFigures.append(figure)
        
        case "Angle":
            attr = "vertexAngle"
            pass

        case _:
            pass
    
    print(parentFigures)

    # все отцовские фигуры
    for parentFigure in parentFigures:
        print("Searching in ", parentFigure)
        # все методы
        for method in FIGURES[parentFigure].ways[attr]:
            print(f"Using {method} in {parentFigure}")
            resOfFind = eval(f"FIGURES[parentFigure].{method}('{target}')")
            
    match type(resOfFind).__name__:
        case "float":
            print(f"Done! Answer is {resOfFind}")
        case "list":
            print(f"Need to find: {resOfFind}")

                    


        
    
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
            "vertexAngle": [],
            "sideLength": [],
            "area": []
        }

class Triangle(Polygon):
    def __init__(self, label):
        super().__init__(label)

        self.ways["sideLength"].extend(["sinTheorem"])

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

        self.ways["sideLength"].extend(["pythagorean"])
        self.ways["area"].extend(["areaByLegs"])

    
    def areaByLegs(self, any):
        """
        Calculate the area based on the lengths of the legs.

        This method iterates through the legs of the figure and checks for any NoneType lengths. If all lengths are valid, it calculates the area using the lengths of the first two legs. If any leg has a NoneType length, it returns a list of the legs that need further processing.
        Returns:
            If all lengths are valid, returns the calculated area.
            If any leg has a NoneType length, returns a list of legs that need further processing.
        """
        delegateFind = []
        for leg in self.legs:
            if type(FIGURES[leg].length).__name__ == "NoneType":
                delegateFind.append(leg)
        if delegateFind == []:
            self.area = 0.5 * FIGURES[self.legs[0]].length * FIGURES[self.legs[1]].length
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
        delegateFind = []
        if targetSide != self.hypotenuse:
            if not attrKnown(self.legs[self.legs.index(targetSide) ^ 1], "length"):
                delegateFind.append(self.legs[self.legs.index(targetSide) ^ 1])
            
            if not attrKnown(self.hypotenuse, "length"):
                delegateFind.append(self.hypotenuse)


            if delegateFind == []:
                FIGURES[targetSide].length = math.sqrt(FIGURES[self.hypotenuse].length ** 2 - FIGURES[self.legs[self.legs.index(targetSide) ^ 1]].length ** 2)
                return FIGURES[targetSide].length
            else:
                return delegateFind
        else:
            delegateFind = []
            for leg in self.legs:
                if not attrKnown(leg, "length"):
                    delegateFind.append(leg)


            if delegateFind == []:
                FIGURES[targetSide].length = math.sqrt(FIGURES[self.legs[0]].length ** 2 + FIGURES[self.legs[1]].length ** 2)
                return FIGURES[targetSide].length
            else:
                return delegateFind


abc = rightTriangle("ABC", "C")
FIGURES["AC"].length = 4
FIGURES["BC"].length = 3

# abd = Triangle("ABD")

find("AB")