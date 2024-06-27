from basics import *
from utilities import *


class Triangle(Polygon):
    """Class representing a triangle

    Parameters
    ==========
    `label`: string of three verticesꞋ names. Pass carefully as you wonꞋt be able to access the instance if label vertices are not in the order they were passed at initialization
    """

    def __init__(self, label):
        super().__init__(label)


class isoscelesTriangle(Triangle):
    """Class representing an isosceles triangle - a triangle with two equal sides

    Parameters:
    ==========
    `label`: string of three verticesꞋ names. Pass carefully as you wonꞋt be able to access the instance if label vertices are not in the order they were passed at initialization
    `baseSide`: string label of the base side of the triangle (that one that does not equal to two others)

    Example
    =======
    isoscelesTriangle("ABC", baseSide="AC") means AB = BC
    """

    def __init__(self, label, baseSide: str):
        super().__init__(label)
        
        self.baseSide = Segment(baseSide)
        
        # base side is always the last in the list
        self.sides.remove(self.baseSide)
        self.sides.append(self.baseSide)
        
        # formulas
        self.formulas.append("self.sides[0], self.sides[1]")
        
        

class rightTriangle(Polygon):
    """Class representing a right triangle - a triangle with one angle that equals 90°

    Parameters:
    ==========
    `label`: string of three verticesꞋ names. Pass carefully as you wonꞋt be able to access the instance if label vertices are not in the order they were passed at initialization
    `rightVertex`: name of the vertice hosting the right angle

    Example
    =======
    rightTriangle("ABC", rightVertex="C") means angle C = 90°
    """

    def __init__(self, label: str, rightVertex: str):
        super().__init__(label)
        self.rightVertex = Point(rightVertex)
        self.legs = []
        for side in self.sides:
            if rightVertex in side.label:
                self.legs.append(Segment(side.label))
            else:
                self.hypotenuse = Segment(side.label)
