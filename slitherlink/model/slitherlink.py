
from slitherlink import solver
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from .field import Field
from collections import deque


class Slitherlink():
    paths: list[deque[Line]]
    patches: list[set[Point]]

    def __init__(self, fieldlist: list[Field]) -> None:
        self.fieldlist = fieldlist
        self.points = list(
            set([p for field in fieldlist for p in field.pointlist]))
        self.linelist = list(
            set([line for field in fieldlist for line in field.linelist]))
        self.paths = []
        self.patches = [set(self.points)]
        self.linesPerPoint: dict[Point, list[Line]] = {
            point: [] for point in self.points}
        for line in self.linelist:
            for point in line.points:
                self.linesPerPoint[point].append(line)

    def hasOnePath(self) -> bool:
        return len(self.paths) == 1
