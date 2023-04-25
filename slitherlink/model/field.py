from .point import Point
from .line import Line


class Field():
    def __init__(self, pointlist: list[Point], linelist: list[Line]) -> None:
        self.pointlist = pointlist
        self.linelist = linelist
        self.number: int | None = None

    def updateLabel(self, label: int | None) -> None:
        if self.number is not None:
            raise RuntimeError("Label is already set")
        if label > len(self.linelist):
            raise ValueError("Label is too high")
        self.number = label
