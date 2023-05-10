from collections.abc import Iterable
from slitherlink.model.field import Field

from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point


def filterLineByState(iter: Iterable[Line], state: LineState):
    for line in iter:
        if line.state == state:
            yield line


def filterLineByPoint(iter: Iterable[Line], point: Point):
    for line in iter:
        if point in line.points:
            yield line


def filterFieldByLine(iter: Iterable[Field], line: Line):
    for field in iter:
        if line in field.linelist:
            yield field
