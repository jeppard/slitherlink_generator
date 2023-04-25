from .point import Point
from .line_state import LineState


class Line():
    def __init__(self, points: tuple[Point, Point]) -> None:
        self.points = points
        self.state: LineState = LineState.UNKNOWN

    def toggleState(self) -> None:
        if self.state == LineState.UNKNOWN:
            self.state = LineState.SET
        elif self.state == LineState.SET:
            self.state = LineState.UNSET
        elif self.state == LineState.UNSET:
            self.state = LineState.UNKNOWN
