import math
FIGURES = {}

def translateByLabels(lst):
    res = []
    for item in lst:
        res.append(item.label)
    return res


def attrKnown(label, attr):
    return type(getattr(FIGURES[label], attr)).__name__ != "NoneType"


def getClassNameByLabel(label: str):
    return FIGURES[label].__class__.__name__