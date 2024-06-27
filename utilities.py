import yaml
from exceptions import *


def attrKnown(figure, attr: str):
    return figure.__dict__.get(attr) if figure.__dict__.get(attr) else False


def labelToPoints(label: str):
    buffer = label
    points = []
    while buffer:
        if len(buffer) > 1:
            if buffer[1].isdigit() and not buffer[0].isdigit():
                points.append(buffer[0] + buffer[1])
                buffer = buffer[2:]
            else:
                points.append(buffer[0])
                buffer = buffer[1:]

        elif not buffer[0].isdigit():
            points.append(buffer[0])
            buffer = buffer[1:]
    return points


def express(expression: str, variable: str):
    pass


class SingletonMeta(type):
    _instances = {}
    _logging = True

    def __call__(cls, label: str, *args, **kwargs):
        
        # sort label points in alphabetical order if Figure allows
        if cls.__name__ in ["Segment", "Triangle", "isoscelesTriangle", "rightTriangle"]:
            points = sorted(labelToPoints(label))
            label = "".join(points)
        
        if label not in cls._instances:
            instance = super().__call__(label, *args, **kwargs)
            cls._instances[label] = instance
            
            if cls.__name__ != "Point" and cls._logging:
                print(f"new {cls.__name__} '{label}'")
                
            return cls._instances[label]
        else:
            
            if cls.__name__ != "Point" and cls._logging:
                print(f"existing {cls.__name__} '{label}' returned")
                
            return cls._instances[label]

            