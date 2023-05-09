from typing import TYPE_CHECKING

from slitherlink.model.error import UnsolvableException

from .line_state import LineState

if TYPE_CHECKING:
    from .point import Point
    from .field import Field


class Line():
    fields: list['Field']

    def __init__(self, points: tuple['Point', 'Point']) -> None:
        if points[0] > points[1]:
            points = points[1], points[0]
        self.points = points
        for p in points:
            p.registerLine(self)
        self._state: LineState = LineState.UNKNOWN
        self.fields = []

    def __hash__(self) -> int:
        return hash(self.points)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Line):
            return NotImplemented
        return self.points == __value.points

    @property
    def state(self):
        return self._state

    def setState(self, state: LineState) -> list['Line']:
        updated: list['Line'] = [self]
        self._state = state
        if state == LineState.UNKNOWN:
            return updated
        try:
            for point in self.points:
                updated += point.update()
            for field in self.fields:
                updated += field.update()
        except UnsolvableException as e:
            for line in updated:
                line.setState(LineState.UNKNOWN)
            self._state = LineState.UNKNOWN
            raise e
        return updated

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)
