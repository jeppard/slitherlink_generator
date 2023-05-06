from .point import Point
from .line import Line
from .line_state import LineState


class Field():
    def __init__(self, pointlist: list[Point], linelist: list[Line]) -> None:
        self.pointlist = pointlist
        self.linelist = linelist
        self.number: int | None = None
        for line in linelist:
            line.registerField(self)

    def isSolved(self) -> bool:
        if self.number is None:
            return True
        numSetLines = sum(1 for line in self.linelist if
                          line.state == LineState.SET)
        return numSetLines == self.number

    def updateLabel(self, label: int | None) -> None:
        numSetLines = sum(1 for line in self.linelist if
                          line.state == LineState.SET)
        numUnknownLines = sum(1 for line in self.linelist if
                              line.state == LineState.UNKNOWN)
        if numSetLines > label:
            raise ValueError("Label is too low")
        if numSetLines + numUnknownLines < label:
            raise ValueError("Label is too high")
        if self.number is not None:
            raise RuntimeError("Label is already set")
        try:
            self.number = label
            self.update()
        except Exception as e:
            self.number = None
            raise e

    def update(self) -> None:
        if self.number is None:
            return  # No information to be gained
        numSetLines = sum(1 for line in self.linelist if
                          line.state == LineState.SET)
        numUnsetLines = sum(1 for line in self.linelist if
                            line.state == LineState.UNSET)
        numUnknownLines = sum(1 for line in self.linelist if
                              line.state == LineState.UNKNOWN)
        if numSetLines == self.number:
            for line in self.linelist:
                if line.state == LineState.UNKNOWN:
                    line.state = LineState.UNSET
        elif numSetLines + numUnknownLines == self.number:
            for line in self.linelist:
                if line.state == LineState.UNKNOWN:
                    line.state = LineState.SET
