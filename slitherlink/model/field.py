from slitherlink.util.filter import filterLineByState
from .point import Point
from .line import Line
from .line_state import LineState


class Field():
    def __init__(self, pointlist: list[Point], linelist: list[Line]) -> None:
        self.pointlist = pointlist
        self.linelist = linelist
        self.number: int | None = None

    def isSolved(self) -> bool:
        if self.number is None:
            return True
        numSetLines = sum(1 for _ in filterLineByState(
            self.linelist, LineState.SET))
        return numSetLines == self.number

    def isSolvable(self):
        if self.number is None:
            return True
        numSetLines = sum(1 for _ in filterLineByState(
            self.linelist, LineState.SET))
        numUnknownLines = sum(1 for _ in filterLineByState(
            self.linelist, LineState.UNKNOWN))
        return numSetLines + numUnknownLines >= self.number
