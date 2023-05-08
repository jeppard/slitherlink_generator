from typing import TYPE_CHECKING

from slitherlink.model.error import UnsolvableException

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
    def state(self):
        return self._state

    @state.setter
    def state(self, state: LineState):
        prev = self._state
        self._state = state
        try:
            for point in self.points:
                point.update()
            for field in self.fields:
                field.update()
        except UnsolvableException as e:
            self._state = prev
            raise e

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)
