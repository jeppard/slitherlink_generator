import dataclasses
from typing import TYPE_CHECKING
from slitherlink.model.error import UnsolvableException

from slitherlink.model.line_state import LineState
if TYPE_CHECKING:
    from slitherlink.model.line import Line


@dataclasses.dataclass(order=True, frozen=True)
class Point():
    x: int
    y: int
    lines: list['Line'] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False)

    def isSolved(self) -> bool:
        numSetLines = sum(1 for line in self.lines if
                          line.state == LineState.SET)
        return numSetLines == 2 or numSetLines == 0

    def isSolvable(self) -> bool:
        numSetLines = sum(
            1 for line in self.lines if line.state == LineState.SET)
        if numSetLines > 2:
            return False
        numUnknownLines = sum(
            1 for line in self.lines if line.state == LineState.UNKNOWN)
        return not (numSetLines == 1 and numUnknownLines == 0)

    def registerLine(self, line: 'Line') -> None:
        self.lines.append(line)

    def update(self):
        updated: list[Line] = []
        numSet = sum(1 for line in self.lines if line.state == LineState.SET)
        numUnknown = sum(
            1 for line in self.lines if line.state == LineState.UNKNOWN)
        if numSet > 2:
            raise UnsolvableException(
                f"To many Lines set at Point ({self.x},{self.y})")
        if numSet == 1 and numUnknown == 0:
            raise UnsolvableException(
                f"Not enough Lines set at Point ({self.x},{self.y})")
        if numSet == 2:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    updated += line.setState(LineState.UNSET)
        if numUnknown != 1:
            return updated
        if numSet == 1:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    updated += line.setState(LineState.SET)
        else:
            for line in self.lines:
                if line.state == LineState.UNKNOWN:
                    updated += line.setState(LineState.UNSET)
        return updated
