import copy
from typing import TYPE_CHECKING

from slitherlink.model.error import StateError, UnsolvableError

from .line_state import LineState

if TYPE_CHECKING:
    from .point import Point
    from .field import Field
    from .slitherlink import Slitherlink


class Line():
    def __init__(self, points: tuple['Point', 'Point']) -> None:
        if points[0] > points[1]:
            points = points[1], points[0]
        self.points = points
        self.state: LineState = LineState.UNKNOWN

    def __hash__(self) -> int:
        return hash(self.points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self.points == other.points

    def __repr__(self) -> str:
        return f'Line: {self.points} is {self.state}'
