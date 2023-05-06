from typing import Generator
from .point import Point
from .line import Line
from .line_state import LineState

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .slitherlink import Slitherlink


class Field():
    def __init__(self, pointlist: list[Point], linelist: list[Line]) -> None:
        self.pointlist = pointlist
        self.linelist = linelist
        self.number: int | None = None
        for line in linelist:
            line.registerField(self)
        self.slitherlink: Slitherlink | None = None

    def updateLabel(self, label: int | None) -> None:
        self.number = label
        if self.slitherlink.solver.isSolvable():
            lines = list(
                set(line for point in self.pointlist for line in point.lines))
            for line in lines:
                self.slitherlink.solver.solve(line)
            return
        self.number = None
        raise ValueError("Unsolvable")

    def update(self, depth=1):
        linesToSet: list[Line] = []
        linesToUnset: list[Line] = []
        visitedPoints: set[Point] = set()
        if self.number is None:
            return  # No information to be gained
        numSetLines = sum(1 for line in self.linelist if
                          line.state == LineState.SET)
        unknownLines = [line for line in self.linelist if line.state ==
                        LineState.UNKNOWN]
        numUnknownLines = len(unknownLines)
        if numSetLines == self.number:
            for line in self.linelist:
                if line.state == LineState.UNKNOWN:
                    linesToUnset += [line]
        elif numSetLines + numUnknownLines == self.number:
            for line in self.linelist:
                if line.state == LineState.UNKNOWN:
                    linesToSet += [line]
        i = (yield (linesToSet, linesToUnset))
