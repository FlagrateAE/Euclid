from utilities import *
from basics import *
from triangles import *

def FIND(figure: Figure, target, attr: str = None):
    """
    Main function for this project. Starts a recursive search for the target of the geometric problem
    
    Parameters
    ==========
    `figure`: target figure
    `attr`: attribute of the target figure to find
    """
    match type(figure).__name__:
        case "Segment":
            attr = "length"
        case "Angle": 
            attr = "angle"
    
    if attrKnown(figure, attr):
        return attrKnown(figure, attr)
    else:
        if type(figure).__name__ == "Segment":
            # each segment can be found in 3 ways: either as sum of subs, or as difference of other, or by a ratio
            pass
                       
Segment("AB")
print(Point("A"))
