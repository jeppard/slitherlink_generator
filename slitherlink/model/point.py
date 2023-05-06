from typing import TYPE_CHECKING

from slitherlink.model.line_state import LineState
if TYPE_CHECKING:
    from slitherlink.model.line import Line


class Point():
    lines: list['Line']

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.lines = []

    def isSolved(self) -> bool:
        numSetLines = sum(1 for line in self.lines if
                          line.state == LineState.SET)
        return numSetLines == 2 or numSetLines == 0

    def registerLine(self, line: 'Line') -> None:
        self.lines.append(line)

    def update(self) -> None:
        numSet = sum(1 for line in self.lines if line.state == LineState.SET)
        numUnknown = sum(
            1 for line in self.lines if line.state == LineState.UNKNOWN)
        if numSet > 2:
            raise ValueError("Too many lines set")
        if numSet == 2:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    line.state = LineState.UNSET
        if numUnknown != 1:
            # No information to be gained
            return
        if numSet == 1:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    line.state = LineState.SET
        else:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    line.state = LineState.UNSET
