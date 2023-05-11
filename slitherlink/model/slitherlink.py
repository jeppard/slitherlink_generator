
from slitherlink import solver
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from .field import Field
from collections import deque


class Slitherlink():
    paths: list[deque[Line]]

    def __init__(self, fieldlist: list[Field]) -> None:
        self.fieldlist = fieldlist
        self.points = list(
            set([p for field in fieldlist for p in field.pointlist]))
        self.linelist = list(
            set([line for field in fieldlist for line in field.linelist]))
        self.paths = []

    def hasOnePath(self) -> bool:
        return len(self.paths) == 1
