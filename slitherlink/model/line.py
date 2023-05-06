from typing import TYPE_CHECKING
import z3

from .line_state import LineState

if TYPE_CHECKING:
    from .point import Point
    from .field import Field


class Line():
    fields: list['Field']

    def __init__(self, points: tuple['Point', 'Point']) -> None:
        if (points[0] > points[1]):
            points = (points[1], points[0])
        self.points = points
        for p in points:
            p.registerLine(self)
        self._state: LineState = LineState.UNKNOWN
        self.fields = []
        self.z3Var = z3.Bool(
            f"Line {points[0].x},{points[0].y} to {points[1].x},{points[1].y}")

    def __hash__(self) -> int:
        return hash(self.points)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Line):
            return NotImplemented
        return self.points == __value.points

    @property
    def state(self) -> LineState:
        return self._state

    @state.setter
    def state(self, state: LineState) -> None:
        self._state = state

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Line):
            return NotImplemented
        return self.points == __value.points
