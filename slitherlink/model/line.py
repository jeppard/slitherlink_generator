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
        self.state: LineState = LineState.UNKNOWN
        self.fields = []

    def registerField(self, field: 'Field') -> None:
        self.fields.append(field)
