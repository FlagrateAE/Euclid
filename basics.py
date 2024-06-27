"""
Basic geometric figures all other are being created from:\n
`Line`, `Segment`, `Point`, `Polygon`
"""

from utilities import *


class Figure(metaclass=SingletonMeta):

    def __init__(self, label):
        self.label = label
        self.belongs = {}
        self.formulas = []

    def __str__(self) -> str:
        return str(self.__dict__)

    def find(self, target: object, attr: str):
        pass


class Line(Figure):
    """Basic class representing a line

    Parameters
    ==========
    `label`: string of one small letter OR two capital letters representing points laying on the line

    Example
    =========
    `Line("a")`\n
    `Line("A1B")`with points: A1, B
    """

    def __init__(self, label):
        super().__init__(label)

        # List of points laying on the line/segment ordered in their physical order
        self.points = []
        if len(labelToPoints(label)) > 1:
            for point in labelToPoints(label):
                self.points.append(Point(point))
                Point(point).belongs["laying"] = self


class Segment(Line):
    """Basic class representing a segment

    Parameters
    ==========
    `label`: string of two end-pointsꞋ names

    Example
    =========
    `Segment("AB")`with end-points: A, B\n
    `Segment("C1D")`with end-points: C1, D
    """

    def __init__(self, label):
        points = sorted(labelToPoints(label))
        label = "".join(points)
        super().__init__(label)
        self.length = None

        # set up the roles
        self.belongs["sides"] = []  # in polygons
        self.belongs["parts"] = []  # in segments laying one in the other

        # child segments
        self.parts = []

    def _initAllPartSegments(self):
        """
        Initializes all possible sub-segments created by points on this segment
        """

        reverses = set()
        reverses.add(self.label)
        reverses.add(self.label[::-1])

        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                seg = self.points[i].label + self.points[j].label
                if seg[::-1] not in reverses:
                    reverses.add(seg)
                    reverses.add(seg[::-1])

                    Segment(seg).belongs["parts"].append(self)

                    # insert all points in-between
                    lastPoint = Segment(seg).points[-1]
                    Segment(seg).points.remove(lastPoint)
                    Segment(seg).points.extend(self.points[i + 1 : j])
                    Segment(seg).points.append(lastPoint)

    def _recursiveFindMasterSegment(self):
        """
        In Euclid, to avoid initializing tons of sub-segments, so-called master segment only stores its points. So, on liesOn() function, target segment "searches" for its master if exists and delegates the point to it
        """

        pass


class Angle(Figure):
    """Basic class representing an angle

    Parameters
    ==========
    `label`: string of three verticesꞋ names, middle vertex is the host

    Example
    =========
    `Angle("ABC")`is an angle between AB and BC with B as a host vertex
    """

    def __init__(self, label):
        super().__init__(label)
        self.angle = None


class Point(Figure):
    """Basic class representing a point

    Parameters
    ==========
    `label`: string that represents a name of the point\n
    Points (vertices of polygons also) must be named with one capital letter that may be followed by a digit

    Example
    =========
    `Point("A")`\n
    `Point("B4")`
    """

    def __init__(self, label):
        super().__init__(label)
        self.belongs["laying"] = None

    def liesOn(self, target: Segment):
        """
        Function to assert that a point lies on a semgent

        Parameters
        ==========
        `target`: target segment a point lies on

        Returns
        =======
        `list` of points laying on the target segment including the just inserted one. Ordered starting from the alphabetically first segment end-point

        Example:

        [Point("A"), Point("C"), Point("D"), Point("B")] means segment AB as A--C--D--B
        """

        target.points.insert(-1, self)


class Polygon(Figure):
    """Basic class representing a polygon\n
    Creating a three-side polygon, use `Triangle` instead

    Parameters:
    ==========
    `label`: string of verticesꞋ names. Pass carefully as you wonꞋt be able to access the instance if label vertces are not in the order they were passed at initialization

    Example
    =======
    `Polygon("ABC")`with vertices: A, B, C\n
    `Polygon("M1NPQ2")`with vertices: M1, N, P, Q2
    """

    def __init__(self, label):
        super().__init__(label)
        self.sides = []

        # initializing all sides
        for i in range(len(labelToPoints(label))):
            point1 = labelToPoints(label)[i]
            point2 = labelToPoints(label)[(i + 1) % len(labelToPoints(label))]
            side_label = point1 + point2
            self.sides.append(Segment(side_label))
            # give a side role
            Segment(side_label).belongs["sides"].append(self)
