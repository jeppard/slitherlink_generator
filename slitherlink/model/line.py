from typing import TYPE_CHECKING

from .line_state import LineState

if TYPE_CHECKING:
    from .point import Point
    from .field import Field


class Line():
    fields: list['Field']

    def __init__(self, points: tuple['Point', 'Point']) -> None:
        self.points = points
        for p in points:
            p.registerLine(self)
        self._state: LineState = LineState.UNKNOWN
        self.fields = []

    @property
    def state(self) -> LineState:
        return self._state

    @state.setter
    def state(self, state: LineState) -> None:
        self._state = state
        for point in self.points:
            point.update()
        for field in self.fields:
            field.update()

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)

    def toggleState(self) -> None:
        if self.state == LineState.UNKNOWN:
            self.state = LineState.SET
        elif self.state == LineState.SET:
            self.state = LineState.UNSET
        elif self.state == LineState.UNSET:
            self.state = LineState.UNKNOWN
