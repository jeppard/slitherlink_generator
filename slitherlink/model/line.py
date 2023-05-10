import copy
from typing import TYPE_CHECKING

from slitherlink.model.error import StateError, UnsolvableError

from .line_state import LineState

if TYPE_CHECKING:
    from .point import Point
    from .field import Field
    from .slitherlink import Slitherlink


class Line():
    fields: list['Field']

    def __init__(self, points: tuple['Point', 'Point']) -> None:
        if points[0] > points[1]:
            points = points[1], points[0]
        self.points = points
        self._state: LineState = LineState.UNKNOWN
        self.fields = []

    def __hash__(self) -> int:
        return hash(self.points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self.points == other.points

    def __repr__(self) -> str:
        return f'Line: {self.points} is {self._state}'

    @property
    def state(self):
        return self._state

    def getNeighbors(self):
        for point in self.points:
            yield from point.lines

    def setState(self, state: LineState) -> list['Line']:
        updated: list['Line'] = [self]
        if self._state != LineState.UNKNOWN:
            if state != LineState.UNKNOWN:
                raise StateError("Line is allready set")
            self._state = LineState.UNKNOWN
            return updated
        self._state = state
        if state == LineState.UNKNOWN:
            return updated
        try:
            for point in self.points:
                updated += point.update()
            for field in self.fields:
                updated += field.update()
        except UnsolvableError as e:
            for line in updated:
                line.setState(LineState.UNKNOWN)
            self._state = LineState.UNKNOWN
            raise e
        return updated

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)
